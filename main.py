import difflib
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
# username:apikey 
# api key from https://id.atlassian.com/manage-profile/security/api-tokens
username = os.getenv("EMAIL_USERNAME")
print(username)
api_key = os.getenv("API_KEY")
print(api_key)
labels_first = requests.get('https://apiit.atlassian.net/rest/api/3/label', auth=(username, api_key))
labels_second = requests.get('https://apiit.atlassian.net/rest/api/3/label?startAt=1000&maxResults=1137', auth=(username, api_key))
api_labels = {
    "results": [
        json.loads(labels_first.text),
        json.loads(labels_second.text)
    ]
}

with open("labels.json", "w") as labels_json:
    json.dump(api_labels, labels_json)

# labels_file = open("labels.json")
# labels_data = json.load(labels_file)["results"]
labels_data = api_labels["results"]
print(labels_data)

labels_list = []

for labels in labels_data:
    labels_list.extend(labels["values"])

similarity = list()
for label in labels_list:
    matching = difflib.get_close_matches(label, labels_list)
    if len(matching) > 1:
        similarity.append(matching)

with open('similar.csv', 'a') as similar_csv:
    for similar in similarity:
        for word in similar:   
                similar_csv.write(word + ", ")
        similar_csv.write("\n")
    similar_csv.close()
