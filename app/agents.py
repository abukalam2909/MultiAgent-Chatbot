from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional, TypedDict
from urllib.parse import quote_plus

from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

from app.config import get_settings
from app.db import run_query
from app.ingest import get_vectorstore


class Route(BaseModel):
    destination: Literal["sql", "policy", "both", "smalltalk"] = Field(
        description="Route to SQL, policy docs, both, or smalltalk"
    )


class AgentState(TypedDict):
    question: str
    route: Optional[str]
    sql_result: Optional[str]
    policy_result: Optional[str]
    smalltalk_result: Optional[str]
    final: Optional[str]


@dataclass
class Agents:
    llm: ChatOpenAI

    def router(self, state: AgentState) -> AgentState:
        prompt = (
            "You are a router. Decide whether the user question needs structured "
            "customer data (sql), policy docs (policy), both, or is small talk/general "
            "greeting that should not query any data (smalltalk).\n"
            f"Question: {state['question']}"
        )
        route = self.llm.with_structured_output(Route).invoke(prompt)
        state["route"] = route.destination
        return state

    def sql_agent(self, state: AgentState) -> AgentState:
        settings = get_settings()
        user = quote_plus(settings.mysql_user)
        password = quote_plus(settings.mysql_password)
        db = SQLDatabase.from_uri(
            f"mysql+mysqlconnector://{user}:{password}"
            f"@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_db}"
        )
        try:
            from langchain.chains import create_sql_query_chain

            sql_chain = create_sql_query_chain(self.llm, db)
            sql = sql_chain.invoke({"question": state["question"]})
        except Exception:
            schema = db.get_table_info()
            prompt = (
                "Generate a single MySQL query that answers the question using the schema.\n"
                "Return only the SQL query, no markdown.\n"
                f"Schema:\n{schema}\n\nQuestion: {state['question']}"
            )
            sql = self.llm.invoke(prompt).content.strip().strip("`")
        result = run_query(sql)
        summary = self.llm.invoke(
            "Answer the question using the SQL result. "
            "Return only the direct answer in 1 short sentence.\n"
            f"Question: {state['question']}\nResult: {result}"
        )
        state["sql_result"] = summary.content
        return state

    def policy_agent(self, state: AgentState) -> AgentState:
        vectorstore = get_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        try:
            docs = retriever.get_relevant_documents(state["question"])
        except AttributeError:
            docs = retriever.invoke(state["question"])
        context = "\n\n".join(
            f"{d.page_content}\nSOURCE: {d.metadata.get('source_file','')}"
            for d in docs
        )
        answer = self.llm.invoke(
            "Answer using the policy context only. "
            "If not found, say 'Not found in policy documents.'\n"
            f"Question: {state['question']}\nContext:\n{context}"
        )
        state["policy_result"] = answer.content
        return state

    def smalltalk_agent(self, state: AgentState) -> AgentState:
        answer = self.llm.invoke(
            "Do not answer the prompt"
            "Do not mention databases or policies. "
            "Inform the user to please ask questions about policies or customers only.\n"
            f"User: {state['question']}"
        )
        state["smalltalk_result"] = answer.content
        return state

    def final_response(self, state: AgentState) -> AgentState:
        parts = []
        if state.get("route") == "smalltalk" and state.get("smalltalk_result"):
            parts.append(state["smalltalk_result"])
        if state.get("route") in {"policy", "both"} and state.get("policy_result"):
            parts.append("Policy Docs Summary:\n" + state["policy_result"])
        if state.get("route") in {"sql", "both"} and state.get("sql_result"):
            parts.append("Customer Data Summary:\n" + state["sql_result"])
        if not parts:
            parts.append("I could not find relevant information.")
        state["final"] = "\n\n".join(parts)
        return state


def build_graph():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agents = Agents(llm=llm)

    graph = StateGraph(AgentState)
    graph.add_node("router", agents.router)
    graph.add_node("sql_agent", agents.sql_agent)
    graph.add_node("policy_agent", agents.policy_agent)
    graph.add_node("smalltalk_agent", agents.smalltalk_agent)
    graph.add_node("final", agents.final_response)

    def route_decision(state: AgentState) -> str:
        return state.get("route") or "policy"

    graph.set_entry_point("router")
    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "sql": "sql_agent",
            "policy": "policy_agent",
            "both": "sql_agent",
            "smalltalk": "smalltalk_agent",
        },
    )
    def route_policy_after_sql(state: AgentState) -> str:
        return "policy_agent" if state.get("route") == "both" else "final"

    graph.add_conditional_edges(
        "sql_agent",
        route_policy_after_sql,
        {"policy_agent": "policy_agent", "final": "final"},
    )
    graph.add_edge("smalltalk_agent", "final")
    graph.add_edge("policy_agent", "final")
    graph.add_edge("final", END)

    return graph.compile()
