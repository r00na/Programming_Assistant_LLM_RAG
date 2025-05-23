# 🤖 Programming Assistant (LLM + RAG + FastAPI + Streamlit)

This project is an AI-powered programming assistant designed to help users understand StackOverflow questions and answers more effectively.

## 💡 Project Idea
The core idea is to build an intelligent assistant that can answer programming questions. Instead of just relying on a general-purpose LLM, this project enhances the model's responses by first retrieving similar questions and answers from the preprocessed StackOverflow dataset. This Retrieval-Augmented Generation (RAG) approach provides more specific and relevant context to the LLM, leading to better quality answers.

##  Features
- **AI-Powered Answers:** Uses `llama3:instruct` to provide high-quality, context-aware responses.
- **RAG Architecture:** Retrieves related StackOverflow Q&A from ChromaDB before LLM response generation.
- **Interactive Interfaces:** Includes both a Streamlit web app and a FastAPI backend.

## 📊 Data Source & Preprocessing

### Dataset
This project uses the [StackSample dataset on Kaggle](https://www.kaggle.com/datasets/stackoverflow/stacksample?select=Questions.csv), which contains:
- Questions.csv
- Answers.csv
- Tags.csv

### Preprocessing Steps
1. **HTML Cleaning:** Removed HTML tags using BeautifulSoup.
2. **Dropping Nulls:** Removed rows with missing body or title.
3. **Filtering by Score:** Retained only items with score > 5.
4. **Merging Data:** Linked questions with their answers using IDs.
5. **Tag Grouping:** Grouped and merged tags with questions.
6. **Final Selection:** Chose top high-quality Q&A pairs for embedding.

## 🛠️ Technologies Used
- **Python** as the main programming language.
- **LangChain** for building the RAG pipeline.
- **Ollama (llama3:instruct)** as the LLM.
- **ChromaDB** for vector search and retrieval.
- **FastAPI** for the backend API.
- **Streamlit** for the web interface.
- **Embeddings:** `mxbai-embed-large` via Ollama.

##  Architecture
1. User submits a programming question.
2. The system retrieves related questions and answers from ChromaDB.
3. The LLM uses this context to generate a rich, helpful response.


## 📺 Deployment & Results

- **Streamlit App:** [Live App Link](#)
- **Example Results:**

###  Example 1: User Question Input
![User Question Screenshot](images/Q.png)  
*A screenshot showing the question input interface.*

###  Example 2: Generated Answer Output
![Answer Screenshot](images/result.png)  
*A screenshot showing the AI-generated answer based on retrieved context.*

-
