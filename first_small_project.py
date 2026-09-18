from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
import os

load_dotenv()

client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

# For Colab:
# from google.colab import userdata
# client = QdrantClient(url=userdata.get("QDRANT_URL"), api_key=userdata.get("QDRANT_API_KEY"))

collection_name = "day0_first_system"
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE),
    )

# Create payload index right after creating the collection and before uploading any data to enable filtering.
# If you add it later, HNSW won't rebuild automatically—bump ef_construct (e.g., 100→101) to trigger a safe rebuild.
client.create_payload_index(
    collection_name=collection_name,
    field_name="category",
    field_schema=models.PayloadSchemaType.KEYWORD,
)

points=[
    models.PointStruct(
        id=1,
        vector=[0.9, 0.1, 0.1, 0.8], # High affordability, high innovation
        payload={
            "name": "Budget Smartphone", 
            "category": "electronics", 
            "price": 299
            }
    ),
    models.PointStruct(
        id=2,
        vector=[0.2, 0.9, 0.8, 0.5], # High quality, high popularity
        payload={
            "name": "Bestselling Novel", 
            "category": "books", 
            "price": 19
        }
    ),
    models.PointStruct(
        id=3,
        vector=[0.8, 0.3, 0.2, 0.9], # High affordability, high innovation (similar to ID 1)
        payload={
            "name": "Smart Home Hub", 
            "category": "electronics", 
            "price": 289
        }
    ),
    models.PointStruct(
        id=4,
        vector=[0.7, 0.2, 0.3, 0.8],
        payload={
            "name": "Smart Wall Clock",
            "category": "electronics",
            "price": 349
        }
    ),

    models.PointStruct(
        id=5,
        vector=[0.3, 0.8, 0.7, 0.1],
        payload={
            "name": "Psychology of Money",
            "category": "books",
            "price": 99
        }
    ),

    models.PointStruct(
        id=6,
        vector=[0.4, 0.8, 0.2, 0.9],
        payload={
            "name": "Smart Speaker",
            "category": "electronics",
            "price": 89
        }
    ),

    models.PointStruct(
        id=7,
        vector=[0.25, 0.85, 0.75, 0.15],
        payload={
            "name": "Atomic Habits",
            "category": "books",
            "price": 299
        }
    ),

    models.PointStruct(
        id=8,
        vector=[0.85, 0.25, 0.15, 0.85],
        payload={
            "name": "Wireless Earbuds",
            "category": "electronics",
            "price": 149
        }
    )
]

client.upsert(collection_name=collection_name, points=points)

# Define a query vector for "affordable and innovative"
query_vector = [0.85, 0.2, 0.1, 0.9]

# 1. Basic similarity search
basic_results = client.query_points(collection_name, query=query_vector)

# print("Basic search results:", basic_results)
# 2. Filtered search (only find electronics)
filtered_results = client.query_points(
    collection_name,
    query=query_vector,
    query_filter=models.Filter(
        must=[models.FieldCondition(key="category", match=models.MatchValue(value="electronics"))]
    ),
)
print("Filtered search results:", filtered_results)