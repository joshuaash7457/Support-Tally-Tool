import os

counts = {
    "discovery": 0,
    "streaming": 0
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

    if "onvif" in text:
        counts["discovery"] += 1

    if "rtsp" in text:
        counts["streaming"] += 1

    if "poe" in text:
        counts[power] += 1

     

print("\nWeekly summary:")
print("Total emails:", total)

for category in counts:
    print(category, counts[category])

