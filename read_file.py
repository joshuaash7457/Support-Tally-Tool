file = open("data/raw/email1.txt", "r")
content = file.read()
file.close()

text = content.lower()

if "onvif" in text:
    print("Found ONVIF issue")

if "vlan" in text:
    print("Found VLAN issue")

