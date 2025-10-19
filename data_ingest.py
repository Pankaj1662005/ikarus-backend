# import pandas as pd
# from app.services.embeddings import generate_text_embedding
# from app.services.pinecone_client import upsert_to_pinecone

# # Load cleaned dataset with: title, description, price, images, uniq_id
# df = pd.read_csv("data/cleaned_products.csv")

# # Fill NaNs in text columns to avoid type errors
# df["title"] = df["title"].fillna("")
# df["description"] = df["description"].fillna("")

# records = []

# for idx, row in df.iterrows():
#     text = row["title"] + " " + row["description"]
#     vector = generate_text_embedding(text)

#     metadata = {
#         "title": row["title"],
#         "description": row["description"],
#         "price": row["price"],
#         "images": row["images"],
#         "uniq_id": row["uniq_id"]
#     }

#     records.append((str(row["uniq_id"]), vector, metadata))

# print("Uploading to Pinecone...")
# upsert_to_pinecone(records)
# print("✅ Done!")
import pandas as pd
from app.services.embeddings import generate_text_embedding
from app.services.pinecone_client import upsert_to_pinecone

# Load cleaned dataset with all available columns
df = pd.read_csv("data/priority_cleaned_products.csv")

# Fill and clean text columns
df["title"] = df["title"].fillna("").astype(str).str.strip()
df["description"] = df["description"].fillna("").astype(str).str.strip()

# Optional: Clean other useful metadata fields
for col in ["material", "color", "manufacturer", "country_of_origin"]:
    if col in df.columns:
        df[col] = df[col].fillna("").astype(str).str.strip()

# Filter: Remove rows where both title and description are empty
df = df[(df["title"] != "") | (df["description"] != "")]

# Add 'available' flag based on price
df["available"] = df["price"].notna()

# Fill NaNs in price with 0.0 for safety (won’t be shown to user if unavailable)
df["price"] = df["price"].fillna(0.0).astype(float)

# Begin preparing records for Pinecone
records = []

for idx, row in df.iterrows():
    # Build enriched input text for embedding
    parts = [row["title"], row["description"]]
    if row.get("material"): parts.append(f"Material: {row['material']}")
    if row.get("color"): parts.append(f"Color: {row['color']}")
    if row.get("country_of_origin"): parts.append(f"Made in {row['country_of_origin']}")
    if row.get("manufacturer"): parts.append(f"Manufacturer: {row['manufacturer']}")
    
    text = " - ".join([p for p in parts if p.strip()])  # Safe join

    # Generate embedding
    vector = generate_text_embedding(text)

    # Create metadata
    metadata = {
        "title": row["title"],
        "description": row["description"],
        "price": row["price"],
        "available": row["available"],
        "images": row["images"],
        "uniq_id": row["uniq_id"],
        "material": row.get("material", ""),
        "color": row.get("color", ""),
        "country_of_origin": row.get("country_of_origin", ""),
        "manufacturer": row.get("manufacturer", "")
    }

    records.append((str(row["uniq_id"]), vector, metadata))

# Upload to Pinecone
print(f"Uploading {len(records)} product vectors to Pinecone...")
upsert_to_pinecone(records)
print("✅ Done!")
