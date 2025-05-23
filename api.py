# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import uvicorn

app = FastAPI(title="Programming Q&A API")

model = OllamaLLM(model="llama3:instruct")

template = """
You are a senior programming assistant helping users understand StackOverflow questions and answers.

Here are some related programming Q&A examples:\n{reviews}

User's question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    question = query.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews": reviews, "question": question})

    return {"answer": result}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
