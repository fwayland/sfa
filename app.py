
import streamlit as st
from core.loaders import load_draft
from core.matcher import ClauseMatcher
from core.storage import PersistentStore

st.title("📄 Facility Agreement Reviewer — ML Upgradable (Offline)")

store = PersistentStore()
matcher = ClauseMatcher(store)

# Upload Precedents
st.header("📁 Upload New Precedent Agreements")
precedents = st.file_uploader("Upload PDF precedents", type=["pdf"], accept_multiple_files=True)
if precedents:
    for file in precedents:
        matcher.ingest_precedent(file)
    st.success("Precedents uploaded, clauses stored and embedded!")

# Upload Draft
st.header("📝 Review a Draft Agreement")
draft_file = st.file_uploader("Upload a draft facility agreement (PDF)", type=["pdf"], key="draft")
if draft_file and matcher.has_precedents():
    draft_clauses = load_draft(draft_file)
    st.subheader("📊 Clause-by-Clause Comparison")

    for i, clause in enumerate(draft_clauses):
        similar, score = matcher.find_most_similar(clause)
        st.markdown(f"**Clause {i+1}**")
        st.text(clause)
        st.markdown(f"📄 Closest Precedent Clause:")
        st.code(similar)
        st.markdown(f"🧠 Similarity Score: `{score:.2f}`")
        if score < 0.5:
            st.warning("⚠️ Low similarity — this clause may be significantly different from precedent.")
        st.markdown("---")
elif draft_file:
    st.warning("Please upload precedents first.")
