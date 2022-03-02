import json

i = 0
dict = {}
fields = ["overall", "reviewerID", "asin"]

with open("electronics_cleaned.json", "w") as f:
    with open("Electronics.json") as file:
        for line in file:
            record = json.loads(line)
            if record["verified"] == False:
                continue
            for key in json.loads(line).keys():
                if key not in fields:
                    record.pop(key)

            f.write(json.dumps(record))
            f.write("\n")
            i += 1
            if i % 100000 == 0:
                print(i)
