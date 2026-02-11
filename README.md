# HUST Student Regulation Chatbot 🎓🤖

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Model](https://img.shields.io/badge/Model-Qwen2.5--7B-violet)
![Tech](https://img.shields.io/badge/RAG-Fine--Tuning-green)
![Library](https://img.shields.io/badge/Library-Unsloth-orange)
![Status](https://img.shields.io/badge/Status-Graduation_Project-red)

> **An intelligent Question-Answering system designed to assist students of Hanoi University of Science and Technology (HUST) in navigating complex academic regulations using Retrieval-Augmented Generation (RAG) and Supervised Fine-Tuning (SFT).**

---

## 📖 Project Overview

Navigating university regulations (Training Regulations, Student Affairs) often involves searching through lengthy, unstructured PDF documents. Keyword-based search engines frequently fail to capture context, while standard LLMs often hallucinate answers due to a lack of domain-specific knowledge.

**This solution addresses these issues by:**
1.  **Digitizing Knowledge:** Extracting and structuring official regulations into a vector database.
2.  **Fine-Tuning:** Training a Large Language Model (LLM) to adopt the persona of a helpful academic assistant that strictly adheres to provided context.
3.  **RAG Implementation:** Retrieving relevant legal clauses to ground the model's answers, ensuring high faithfulness and citing specific articles.

---

## 🗄️ Knowledge Base (RAG Pipeline)

The backbone of the system is a high-quality vector database derived from official HUST PDF documents.

### 1. ETL Process
* **Extraction:** Raw text is extracted from official PDF regulations (e.g., *Quy chế Công tác sinh viên*, *Quy chế Đào tạo*).
* **Cleaning:** Preprocessing scripts remove non-semantic elements such as headers, footers, page numbers, and redundant line breaks to ensure clean context for the LLM.

### 2. Chunking Strategy
To preserve the semantic integrity of legal clauses while fitting within the context window, the text is split using a Recursive Character strategy:
* **Chunk Size:** 1024 tokens
* **Overlap:** 256 tokens

### 3. Embedding & Storage
* **Embedding Model:** `alibaba-nlp/gte-multilingual-base` (Chosen for its superior performance in Vietnamese semantic retrieval).
* **Vector Database:** **ChromaDB** is used to store and index vectors for low-latency retrieval.

---

## 🧠 Training Dataset (SFT)

To improve the model's tone, reasoning, and adherence to instructions, a custom dataset was curated.

* **Generator:** **Gemini 3 Pro** was utilized to generate **1,000 synthetic Q&A pairs** based on the extracted regulation chunks.
* **Logic:** The dataset includes positive examples (answering with citations) and negative examples (refusing out-of-scope questions).
* **Schema:**
    ```json
    {
      "instruction": "Bạn là trợ lý ảo của Phòng Đào tạo ĐHBK Hà Nội...",
      "input": "Bối cảnh: [Legal Text Context]... Câu hỏi: [Student Question]",
      "output": "Theo Điều X Khoản Y... [Answer]"
    }
    ```

---

## 🚀 Model Selection & Fine-Tuning

### Base Model
**Qwen2.5-7B-Instruct** was selected after benchmarking against PhoGPT and Vistral. It demonstrated the highest capability in Vietnamese language understanding and logical reasoning required for legal interpretation.

### Fine-Tuning Configuration
The model was fine-tuned using **QLoRA** (Quantized Low-Rank Adaptation) via the **Unsloth** library for optimization.

| Parameter | Configuration |
| :--- | :--- |
| **Quantization** | 4-bit (NF4) |
| **LoRA Rank (r)** | 16 |
| **LoRA Alpha** | 16 |
| **Target Modules** | q_proj, k_proj, v_proj, o_proj, etc. |
| **Framework** | Unsloth (PyTorch) |

---

## 📊 Evaluation Results

The system was evaluated using the **RAGAS** framework. The Fine-tuned model (SFT) showed significant improvement over the Base model in handling domain-specific queries.

| Metric | Base Model (Zero-shot) | Fine-Tuned Model (SFT) |
| :--- | :---: | :---: |
| **Faithfulness** | 0.82 | **0.95** |
| **Answer Relevancy** | 0.78 | **0.92** |
| **Context Precision** | 0.85 | **0.89** |

> *The SFT process significantly reduced hallucinations and improved the directness of answers.*

---

## 💻 System Demo

The application interface is built using **Gradio**, offering a clean and accessible user experience.

1.  **Input:** Students ask natural language questions (e.g., *"Điều kiện để được học bổng KKHT là gì?"*).
2.  **Process:** The system retrieves top-k relevant chunks from ChromaDB and feeds them into the Qwen2.5 model.
3.  **Output:** The bot provides an answer citing specific regulations (e.g., *Theo Điều 12...*).
4.  **Verification:** A "Reference" section displays the actual text of the cited regulations for verification.


https://github.com/user-attachments/assets/886cc4b0-9efe-4efc-bbe0-f6de0188ce8f


---

## 🛠️ Tech Stack

* **LLM Backbone:** Qwen2.5-7B-Instruct
* **Fine-tuning:** Unsloth, QLoRA, PyTorch, Hugging Face
* **RAG Engine:** LangChain, ChromaDB
* **Embeddings:** Alibaba GTE Multilingual
* **Data Generation:** Gemini 3 Pro
* **UI/UX:** Gradio

---

## 📜 License & Acknowledgements

This project is a Graduation Thesis (Đồ án II) at the School of Applied Mathematics and Informatics, Hanoi University of Science and Technology (HUST).

* **Author:** Lê Quang Đức (20227221)
* **Supervisor:** TS. Ngô Thị Hiền

---
[Link model](https://huggingface.co/wanduc0701/hust_chatbot_qwen2.5_finetuned)
[Link dataset](https://huggingface.co/datasets/wanduc0701/Sft_dataset_hust_regulation)
