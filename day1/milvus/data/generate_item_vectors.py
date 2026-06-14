"""
Optional: pre-generate fixed item vectors so everyone uses the SAME data
(handy for comparing benchmark numbers across machines).

Usage:
    python generate_item_vectors.py 50000

Saves item_vectors.npy (vectors) and item_meta.csv (id,category).
The lab script generates random vectors on the fly, so this is only
needed if you want repeatable data. Load it with:
    import numpy as np
    vecs = np.load("item_vectors.npy")
"""
import csv
import sys
import numpy as np

CATS = ["weapon", "potion", "armor", "spell"]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000
    dim = 128
    rng = np.random.default_rng(42)        # fixed seed = same data every time
    vecs = rng.random((n, dim)).astype("float32")
    np.save("item_vectors.npy", vecs)

    with open("item_meta.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "category"])
        for i in range(n):
            w.writerow([i, CATS[i % len(CATS)]])

    print(f"Saved item_vectors.npy ({n}x{dim}) and item_meta.csv")


if __name__ == "__main__":
    main()
