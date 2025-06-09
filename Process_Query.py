import google.generativeai as genai
import pandas as pd
import numpy as np
import os


GOOGLE_API_KEY = 'Enter your API key'
genai.configure(api_key=GOOGLE_API_KEY)

def process_query_and_generate_response(query, filepath, top_n=5):
    """
    Given a query and the filepath to a dataframe, find the top_n passages
    and generate a response based on those passages.
    """
  
    dataframe = pd.read_pickle(filepath)

    model_embedding = 'models/embedding-001'
    query_embedding = genai.embed_content(model=model_embedding,
                                          content=query,
                                          task_type="retrieval_query")["embedding"]

    embeddings = np.array(dataframe['Embeddings'].tolist())

    dot_products = np.dot(embeddings, query_embedding)
    top_indices = np.argsort(dot_products)[-top_n:][::-1]
    passages = dataframe.iloc[top_indices]['Text'].tolist()

    model_response = 'models/gemini-1.5-flash'
    model = genai.GenerativeModel(model_response)
    passage_text = "\n".join(passages)
    prompt = f"{query} + {'build your answer based on exact references to the following passage text'} + {passage_text}"
    response = model.generate_content(prompt)

    return response.text
