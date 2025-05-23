# vector.py
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
import ast

df = pd.read_csv("cleaned_stackoverflow.csv")

df = df[["Title", "Body_Question", "Body_Answer", "Tag"]].dropna()

def safe_eval_tags(tag_str):
    try:
        return ast.literal_eval(tag_str)
    except:
        return []

df["tags_list"] = df["Tag"].apply(safe_eval_tags)

df["content"] = df.apply(lambda row: f"Question: {row['Title']}\n\n{row['Body_Question']}\n\nAnswer: {row['Body_Answer']}\n\nTags: {', '.join(row['tags_list'])}", axis=1)

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_stackoverflow_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []

    for i, row in df.iterrows():
        doc = Document(
            page_content=row["content"],
            metadata={"tags": row["tags_list"]},
            id=str(i)
        )
        documents.append(doc)
        ids.append(str(i))

vector_store = Chroma(
    collection_name="stackoverflow_qa",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})
