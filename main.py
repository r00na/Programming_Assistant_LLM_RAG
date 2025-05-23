# main.py
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import time

model = OllamaLLM(model="llama3:instruct")

template = """
You are a senior programming assistant helping users understand StackOverflow questions and answers.

Here are some related programming Q&A examples:\n{reviews}

User's question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n===============================")
    question = input("Ask your programming question (or q to quit): ")
    print("\n")
    if question.lower() == "q":
        break

    print("[DEBUG] Start retrieving relevant reviews...")
    start_time = time.time()
    reviews = retriever.invoke(question)
    print(f"[DEBUG] Retrieved reviews in {time.time() - start_time:.2f} seconds.")

    print("[DEBUG] Start generating answer from model...")
    start_time = time.time()
    result = chain.invoke({"reviews": reviews, "question": question})
    print(f"[DEBUG] Model responded in {time.time() - start_time:.2f} seconds.")

    print("\nAnswer:\n", result)
