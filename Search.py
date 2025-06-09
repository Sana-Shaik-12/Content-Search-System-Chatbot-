import streamlit as st
import os
from Process_PDF import process_pdf  
from Process_Query import process_query_and_generate_response 

st.title("Content Search AI")

uploads_dir = "uploads"
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    file_path = os.path.join(uploads_dir, uploaded_file.name)  
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Uploaded file: {uploaded_file.name}")

    if st.button('Process PDF'):
        process_pdf(file_path)  # Process the PDF
        st.success("PDF processed successfully.")

query = st.text_input("Type your question here:")

if st.button("Search"):
    chunks_file = os.path.join(uploads_dir, uploaded_file.name.replace(".pdf", "_chunks.pkl")) 
    
    if os.path.exists(chunks_file):
        response = process_query_and_generate_response(query, chunks_file, top_n=5)
        st.write("Response:")
        st.write(response)
    else:
        st.error("Please process the PDF file before searching.")
