import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
import pandas as pd
import csv
import json

csv_file = "ipc_dataset_nlp.csv"

data = []
id = []
meta = []

with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
    lines = csv.reader(file)
    for idx,row in enumerate(lines):
        if idx == 0:
            continue
        
        data.append(" ".join(row))
        id.append(str(idx))
        meta.append({"section": row[0] })


sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")

client = chromadb.PersistentClient(path="C:\\Users\\reube\\OneDrive\\Desktop\\Mini Project\\test\\db")

collection = client.get_or_create_collection(name="ipc_database", embedding_function=sentence_transformer_ef,metadata={"hnsw:space": "cosine"})

def add_data():
    collection.add(
                    documents=data,
                    metadatas=meta,
                    ids=id
                    )
    print("Data Added to Collection")
    print(collection.count())

def retrieve_section(query):
    results = collection.query(query_texts = query,
                               n_results=2,
                                include=["documents", "distances"])
    
    return results



def call_db(query):
    results = retrieve_section(query)
    op = ""
    result = results["documents"]

    for inner_result in result:
        for ir in inner_result:
            op = op +"\n"+ ir 
    return op


query="A situation where impure substance are mixed with medicinal drugs"
# query="An offense related to falsification of documents for monetary gain"
# query="Jack tells Sarah that he will hurt her family if she doesn't give him a lot of money. Sarah is scared for her family, so she does what Jack asks."
# add_data()

    

if __name__ == "__main__":
    op=""
    results = retrieve_section(query)

    for result in results["documents"]:
        # print(result)
        print(json.dumps(result, indent=4))

    print("main")
