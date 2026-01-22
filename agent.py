from langchain_ollama import ChatOllama
from langchain_core.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

def build_agent(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

    search_tool = create_retriever_tool(
        retriever,
        name="search_ddrm",
        description="Recherche dans le DDRM (documents Docling)."
    )

    SYSTEM_PROMPT = (
        "Tu es un assistant d'analyse documentaire (DDRM / risques). "
        "RÈGLE ABSOLUE : tu dois répondre UNIQUEMENT à partir du CONTEXTE "
        "fourni par l'outil search_ddrm. "
        "Si le contexte ne contient pas l'information, réponds exactement : "
        "'Information non trouvée dans les documents fournis.' "
        "Réponds en français, clair, structuré."
    )

    llm = ChatOllama(
        model="ministral-3",
        base_url="http://127.0.0.1:11434",
        temperature=0,
    )

    checkpointer = InMemorySaver()

    agent_executor = create_react_agent(
        model=llm,
        tools=[search_tool],
        prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )

    return agent_executor
