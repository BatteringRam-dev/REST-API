import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 78, "name": "Joe", "views": 10000},
        {"likes": 10000, "name": "How to make REST API", "views": 10000},
        {"likes": 35, "name": "Sriram", "views": 10000}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

#VideoId 1 is the first video id which is generated itselft a get request below that asks for id 1
response = requests.patch(BASE + "video/2", {"views": 99, "likes": 101})
print(response.json())