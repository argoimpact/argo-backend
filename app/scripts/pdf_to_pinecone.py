import os
from app.utils.langchain import DocPath, generate_text_from_path, generate_chunks
from app.utils.embeddings import EmbeddingRequest, UpsertRequest, generate_embedding, upsert_embedding
from app.config import app_config
from app.utils.openai import openai_client
from app.utils.pinecone import pinecone_client
from app.models.vectordb import Vector, VectorMetaData

directory = '../_AI Input Proposals'

def list_rfp_files(directory):
    rfp_files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename == "RFP.pdf":
                rfp_files.append(os.path.join(dirpath, filename))
    return rfp_files

directory += '/Known'
rfp_paths = list_rfp_files(directory)
chunk_id = 0

for path in rfp_paths:
    # pdfs to chunks
    input = DocPath(doc_path=path)
    text = generate_text_from_path(request=input)
    chunks = generate_chunks(request=text).texts
    # chunks to pinecone
    rfp_name = path.split('/')[-2]
    embed_request = EmbeddingRequest(text=chunks, model=app_config.embedding_model_small)
    embeds = generate_embedding(request=embed_request, client=openai_client).embeddings

    vectors = []
    for embed, chunk in zip(embeds, chunks):
        metadata = VectorMetaData(
            text=chunk,
            title=rfp_name
        )
        vector = Vector(
            id=str(chunk_id),
            values=embed.embedding,
            metadata=metadata
        )
        vectors.append(vector)
    upsert_request = UpsertRequest(vectors=vectors, index="test-index",namespace="")
    print(upsert_embedding(request=upsert_request, client=pinecone_client))
    chunk_id += 1
