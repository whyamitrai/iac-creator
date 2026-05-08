import streamlit as st
import requests

st.title("IaC Generator")

query = st.text_area("Describe your infrastructure:")

if st.button("Generate Terraform Code"):
    if query:
        response = requests.post(
            "http://localhost:8000/generate",
            json={"query": query}
        )
        st.code(response.json()["output"], language="hcl")
    else:
        st.warning("Please enter a query first.")
