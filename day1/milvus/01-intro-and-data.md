# Milvus — Step 1: What it is, and our sample data

## What is Milvus?

Milvus is a **vector database**. It is built for one job and does it at massive scale: **find the items most similar to a given item**, where "items" are stored as **vectors** (lists of numbers).

We met vectors in the PostgreSQL lesson: AI turns text, images, or audio into vectors so that **similar things have nearby numbers**. PostgreSQL can do a little vector search; **Milvus is built to do it over millions or billions of vectors, fast.**

We use a vector database when:
- We need **semantic / similarity search** — "find products like this", "find similar images", "find documents about this topic".
- The number of vectors is **large** and queries must stay fast.
- This powers recommendations, image search, and the "retrieval" in AI assistants (RAG).

## Vector words (easy version)

- **Embedding / vector** — a list of numbers describing an item, e.g. 128 numbers.
- **Dimension** — how many numbers in the vector (here we use 128).
- **Similarity / distance** — how close two vectors are. Close = similar.
- **K-NN** — "k nearest neighbours": find the k closest vectors to a query.
- **Index** — a clever structure that finds near vectors without checking all of them.
- **Collection** — Milvus's version of a table: it holds vectors plus some metadata.

## Our Day 1 data: Pixel Quest item vectors

For Milvus we pretend each **game item** has a 128-number vector describing it (its "embedding"). In the lab we generate **50,000** random vectors to feel real scale, then search for the items most similar to a query vector.

> We make the vectors with random numbers using `numpy`. In a real system these numbers would come from an AI model, but random vectors are perfect for learning how Milvus stores, indexes, and searches them.

## Connect to Milvus

> **First time with the terminal?** Read **[../00-setup/02-how-to-run-queries.md](../00-setup/02-how-to-run-queries.md)** — how to open a terminal, run scripts step by step, and where settings live. In short: open the VS Code terminal (**Ctrl + `**), make sure the stack is up with `docker compose up -d`, then **activate the Python virtual environment** before running any script:
> ```bash
> # Windows PowerShell:
> .venv\Scripts\Activate.ps1
> # WSL / Linux / macOS:
> source .venv/bin/activate
> ```

Milvus has **no command-line shell** like the others; we talk to it from Python using `pymilvus` (installed in setup). Save this as a `.py` file and run it with `python file.py`, or paste it into a Python prompt. Quick connection test:

```python
from pymilvus import connections, utility
connections.connect(host="localhost", port="19530")
print("collections:", utility.list_collections())
```

If that prints a list (even an empty one `[]`), you are connected.

➡️ Next: **[02-collections-and-indexing.md](02-collections-and-indexing.md)**

---

## ⭐ Must-learn from this topic

- **Vector vocabulary** — embedding, dimension, distance/similarity, K-NN, collection.
- **When to use a vector DB** — semantic search, recommendations, image search, RAG.
- **pymilvus connect** — `connections.connect(host, port)` and `utility.list_collections()`.

### 📚 Official docs
- [Milvus docs](https://milvus.io/docs) — start here.
- [Milvus Quickstart](https://milvus.io/docs/quickstart.md) — first collection & search.
- [PyMilvus reference](https://milvus.io/api-reference/pymilvus/v2.4.x/About.md) — the Python SDK.
