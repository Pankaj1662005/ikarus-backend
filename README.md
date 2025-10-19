# ⚡ Ikarus Product Recommendation Backend

A FastAPI backend that provides AI-powered product recommendations using semantic embeddings stored in Pinecone.

---

## Features

* Generate embeddings for products (title + description + optional metadata)
* Store embeddings in Pinecone vector database
* Query Pinecone for top-K similar products
* FastAPI endpoint to return recommendations

---

## Folder Structure

```
backend/
├── app/
│   ├── main.py                # FastAPI entry point
│   ├── api/
│   │   ├── routes.py          # API endpoints
│   │   └── recommender_raw.py # Recommendation logic
│   └── services/
│       ├── embeddings.py      # Embedding generation
│       └── pinecone_client.py # Pinecone integration
├── data_ingest.py             # Upload embeddings to Pinecone
├── requirements.txt
└── .env                       # API keys & secrets
```

---

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
# Activate virtual environment
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Create `.env` File

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_env
PINECONE_INDEX=ikarus-products
OPENAI_API_KEY=your_openai_key
```

### 3. Prepare Data

* CSV file: `data/cleaned_products.csv`
* Required columns: `title`, `description`, `price`, `images`, `uniq_id`

---

## Running the App

### 1. Ingest Data into Pinecone

```bash
python data_ingest.py
```

### 2. Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

* Access docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Usage

**POST** `/recommend/raw`

**Request Body:**

```json
{
  "prompt": "comfortable wooden chair"
}
```

**Response:**

```json
{
  "results": [
    {"score": 0.95, "product": {...}},
    {"score": 0.92, "product": {...}},
    {"score": 0.88, "product": {...}}
  ]
}
```

---

## How It Works

1. **Data Cleaning:** Remove nulls; keep title/description; optional metadata (color, material, manufacturer).
2. **Embedding:** Combine title + description + optional metadata → convert to vector using `sentence-transformers`.
3. **Store in Pinecone:** Each product has an ID, vector, and metadata.
4. **Query:** Convert user prompt to vector → search Pinecone → return top-K similar products.

---

## Quick Notes

* Each product has **one embedding** enriched with optional metadata.
* Pinecone uses **cosine similarity** for vector search.
* Default top-K recommendations: 5.
* Embeddings use `all-MiniLM-L6-v2` (512 dimensions).

---

## License

MIT License – Free for personal and commercial use

---

## Author

Built with ❤️ using FastAPI & Pinecone


Do you want me to do that?
