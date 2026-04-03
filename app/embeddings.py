from app.config import openai_client

class CustomEmbeddings:
    def embed_documents(self, texts):
        response = openai_client.embeddings.create(
            model="azure/genailab-maas-text-embedding-3-large",
            input=texts
        )
        return [x.embedding for x in response.data]

    def embed_query(self, text):
        response = openai_client.embeddings.create(
            model="azure/genailab-maas-text-embedding-3-large",
            input=[text]
        )
        return response.data[0].embedding