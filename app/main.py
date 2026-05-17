from fastapi import FastAPI

from app.models import (
    ChatRequest,
    ChatResponse
)

from app.agent import SHLAgent
from app.retriever import SHLRetriever


app = FastAPI()


retriever = SHLRetriever(
    catalog_path="data/shl_catalog.csv",
    index_path="data/faiss.index",
    embeddings_path="data/embeddings.npy"
)

agent = SHLAgent(retriever)


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    messages = [
        m.model_dump()
        for m in request.messages
    ]

    response = agent.chat(
        messages
    )

    return response
