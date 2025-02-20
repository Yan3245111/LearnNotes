import json


data = {
    "1": 1,
    "2": 2,
    "3": [1, 2, 3],
}

with open("1.json", "w") as fp:
    json.dump(data, fp, indent=len(data))


with open("1.json", "r") as fp:
    data1 = json.load(fp)

print(data1["3"])
