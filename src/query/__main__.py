from src.query.doc_retriever import DocumentRetriever

if __name__ == "__main__":
    dr = DocumentRetriever()
    print(dr.retrieve_relevant_documents(["another", "first"]))
