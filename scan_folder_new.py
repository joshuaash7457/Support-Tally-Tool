import os

folder = "data/raw"

needle = "did not receive"
counts = {"DNR": 0}
total = 0

import os

folder = "data/raw"

needle = "CMP"
counts = {"CMP": 0}
total = 0

CHUNK_SIZE = 1024 * 1024  # 1MB

for filename in os.listdir(folder):
    path = os.path.join(folder, filename)

    if not os.path.isfile(path):
        continue

    total += 1
    found = False

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            if needle in chunk.lower():
                found = True
                break

    if found:
        counts["DNR"] += 1

print("\nWeekly summary:")
print("Total emails:", total)
for k, v in counts.items():
    print(k, v)


CHUNK_SIZE = 1024 * 1024  # 1MB

for filename in os.listdir(folder):
    path = os.path.join(folder, filename)

    if not os.path.isfile(path):
        continue

    total += 1
    found = False

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            if needle in chunk.lower():
                found = True
                break

    if found:
        counts["DNR"] += 1

print("\nWeekly summary:")
print("Total emails:", total)
for k, v in counts.items():
    print(k, v)

