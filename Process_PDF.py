import google.generativeai as genai
import pandas as pd
import numpy as np
import fitz  # PyMuPDF
import os

GOOGLE_API_KEY = 'Enter your APIKey here'
genai.configure(api_key=GOOGLE_API_KEY)

def process_pdf(file_path):
    # Step 1: Extract text from PDF
    def extract_text_from_pdf(file_path):
        doc = fitz.open(file_path)
        text_content = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            text_content += text
        doc.close()
        return text_content

    extracted_text = extract_text_from_pdf(file_path)

    
    def suggest_chunks(text):
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        prompt = f"Divide the following text into semantically meaningful paragraphs using headline themes as a guide and do not provide an explanation for this separate each of these chunks with a colon: {text}"
        response = model.generate_content(prompt)

     
        chunks = response.text.split(':')

      
        df = pd.DataFrame(chunks, columns=['Text'])

       
        df['Title'] = 'COI advice'
        return df

    chunk_df = suggest_chunks(extracted_text)

  
    def embed_fn(title, text):
        model = 'models/embedding-001'
        return genai.embed_content(model=model,
                                   content=text,
                                   task_type="retrieval_document",
                                   title=title)["embedding"]

    chunk_df['Embeddings'] = chunk_df.apply(lambda row: embed_fn(row['Title'], row['Text']), axis=1)

   
    filename = os.path.basename(file_path)
    name, _ = os.path.splitext(filename)


    output_filepath = os.path.join(os.path.dirname(file_path), f"{name}_chunks.pkl")  # Use .pkl for pickle

 
    chunk_df.to_pickle(output_filepath)
