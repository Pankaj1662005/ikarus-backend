from app.services.embeddings import generate_text_embedding
from app.services.pinecone_client import query_pinecone

def get_raw_recommendations(user_prompt: str):
    vector = generate_text_embedding(user_prompt)
    results = query_pinecone(vector, top_k=5)

    output = []
    for match in results:
        output.append({
            "score": match["score"],
            "product": match["metadata"]
        })

    return output
