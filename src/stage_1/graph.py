"""LangGraph chatbot graph using Mistral AI with Langfuse observability."""

import atexit

from langchain_core.messages import SystemMessage
from langchain_mistralai import ChatMistralAI
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from langgraph.graph import START, END, StateGraph, MessagesState

from stage_1.config import get_settings

SYSTEM_PROMPT = """You are a helpful, friendly assistant. Be concise and helpful.
If you don't know something, say so. Keep responses brief unless asked for detail."""


def get_langfuse_client() -> Langfuse:
    """Get Langfuse client instance."""
    settings = get_settings()
    return Langfuse(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        host=settings.langfuse_base_url,
    )


def get_langfuse_handler(
    session_id: str | None = None,
    user_id: str | None = None,
) -> CallbackHandler:
    """Get Langfuse callback handler for tracing."""
    settings = get_settings()
    return CallbackHandler(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        host=settings.langfuse_base_url,
        session_id=session_id,
        user_id=user_id,
    )


def create_chat_model() -> ChatMistralAI:
    """Create Mistral chat model."""
    settings = get_settings()
    return ChatMistralAI(
        model="mistral-small-latest",
        api_key=settings.mistral_api_key,
        temperature=0.7,
    )


def chatbot(state: MessagesState) -> dict:
    """Process messages and generate response.

    Returns partial state update (dict), not full MessagesState.
    """
    llm = create_chat_model()

    # Prepend system message if not present
    messages = state["messages"]
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)

    response = llm.invoke(messages)
    return {"messages": [response]}


def create_graph() -> StateGraph:
    """Create the chatbot graph."""
    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    return graph_builder.compile()


# Export compiled graph for LangGraph Platform
graph = create_graph()

# Register flush on shutdown
_langfuse = get_langfuse_client()
atexit.register(_langfuse.flush)
