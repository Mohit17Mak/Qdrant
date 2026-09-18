from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
import os

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

collections = client.get_collections()

print("Connected to Qdrant Cloud!")
print(collections)

# Define the collection name
collection_name = "my_first_collection"

# Create the collection with specified vector parameters
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=4,  # Dimensionality of the vectors
            distance=models.Distance.COSINE  # Distance metric for similarity search
        )
    )

points = [
    models.PointStruct(
        id=1,
        vector=[0.1, 0.2, 0.3, 0.4],
        payload={
            "category": "example",
            "name": "Vector One"
        }
    ),

    models.PointStruct(
        id=2,
        vector=[0.9, 0.8, 0.7, 0.6],
        payload={
            "category": "demo",
            "name": "Vector Two"
        }
    ),

    models.PointStruct(
        id=3,
        vector=[0.2, 0.3, 0.4, 0.5],
        payload={
            "category": "test",
            "name": "Vector Three"
        }
    )
]

client.upsert(
    collection_name=collection_name,
    points=points
)

print("Vectors inserted!")

# collection_info = client.get_collection(collection_name)

# print(collection_info)

# Define the query vector
query_vector = [0.08, 0.14, 0.33, 0.28]

# Search for the most similar vectors
search_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=2
)

print("\nSearch Results:")

for result in search_results.points:
    print(
        f"ID: {result.id} | "
        f"Score: {result.score:.4f} | "
        f"Payload: {result.payload}"
    )