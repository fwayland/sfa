
# Facility Reviewer AI (Offline, ML-Upgradable)

This offline-capable Streamlit app:
- Uploads many precedents over time
- Stores & reuses precedent clauses persistently
- Uses ML embeddings (sentence-transformers) to compare clauses
- Can scale and evolve with more data

## Run Locally

1. Install:
```
pip install -r requirements.txt
```

2. Start:
```
streamlit run app.py
```

Stored data is saved in `precedent_data.json`.
