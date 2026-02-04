import os

folder = "data/raw"

counts = {
    "DNR": 0,
}

total = 0
needle = "didn't recieve link"

for filename in os.listdir(folder):
    path = os.path.join(folder, filename)

    if not os.path.isfile(path):
        continue

    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    total += 1
    text = content.lower()

    if needle in text:
        counts["DNR"] += 1

print("\nWeekly summary:")
print("Total emails:", total)

for category, count in counts.items():
    print(category, count)

