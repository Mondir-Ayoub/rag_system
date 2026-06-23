from vectorstore.qdrant_store import client

client.delete_collection("documents")

print("Collection supprimée")