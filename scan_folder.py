import os

counts = {
    "DNR": 0,
}

folder = "data/raw"

total = 0

for filename in os.listdir(folder):
    path = folder + "/" + filename
    file = open(path, "r")
    content = file.read()
    file.close()

    text = content.lower()
    total += 1

    
    if "Can you please provide me with a link?" in text:
        counts["DNR"] += 1


print("\nWeekly summary:")
print("Total emails:", total)

for category in counts:
    print(category, counts[category])

