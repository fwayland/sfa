
import streamlit as st
from PyPDF2 import PdfReader
import openai
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os

# Setup
openai.api_key = os.getenv("OPENAI_API_KEY")
model = SentenceTransformer('all-MiniLM-L6-v2')

st.title("📄 Facility Agreement Reviewer (AI-Powered)")

# Memory for precedents
if "precedent_texts" not in st.session_state:
    st.session_state.precedent_texts = []
if "precedent_embeddings" not in st.session_state:
    st.session_state.precedent_embeddings = []

# --- Upload Precedents ---
st.header("Upload Precedent Facility Agreements")
precedents = st.file_uploader("Upload PDF precedents", type=["pdf"], accept_multiple_files=True)

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

if precedents:
    for file in precedents:
        text = extract_text_from_pdf(file)
        st.session_state.precedent_texts.append(text)
        embeddings = model.encode(text.split('\n'), convert_to_tensor=False)
        st.session_state.precedent_embeddings.extend(embeddings)

    st.success("Precedents uploaded and embedded!")

# --- Upload Draft for Review ---
st.header("Upload Draft Facility Agreement")
draft_file = st.file_uploader("Upload the draft document (PDF)", type=["pdf"])

if draft_file and st.session_state.precedent_embeddings:
    draft_text = extract_text_from_pdf(draft_file)
    draft_clauses = [clause.strip() for clause in draft_text.split('\n') if len(clause.strip()) > 30]
    draft_embeddings = model.encode(draft_clauses, convert_to_tensor=False)

    st.subheader("🧠 Reviewing Draft Clauses...")

    index = faiss.IndexFlatL2(len(draft_embeddings[0]))
    index.add(np.array(st.session_state.precedent_embeddings))

    for i, clause in enumerate(draft_clauses):
        D, I = index.search(np.array([draft_embeddings[i]]), k=1)
        most_similar = st.session_state.precedent_texts[0].split('\n')[I[0][0]]

        prompt = f"""You are a legal assistant. Compare the following DRAFT clause to the PRECEDENT clause. Add a helpful legal comment.

        DRAFT CLAUSE:
        {clause}

        PRECEDENT CLAUSE:
        {most_similar}

        COMMENT:"""

        from openai import OpenAI

        client = OpenAI()  # uses OPENAI_API_KEY env var
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            comment = response.choices[0].message.content

        except Exception as e:
            st.error(f"💥 Error from OpenAI: {e}")
            comment = "⚠️ Could not fetch comment from GPT. See error above."
        st.markdown(f"**Clause {i+1}:**")
        st.text(clause)
        st.markdown(f"💬 *{comment}*")
        st.markdown("---")

elif draft_file:
    st.warning("Please upload at least one precedent first.")
