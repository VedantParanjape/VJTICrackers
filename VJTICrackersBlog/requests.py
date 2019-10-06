import requests
import csv

# get location somehow

f = open('pm_data.csv', 'r')
reader = csv.reader(f)

pm = {}
for row in reader:
    pm[row[0]] = row[1]

exp = pm[location]

# URL
url = 'http://localhost:5000/api'

# Change the value of experience that you want to test
r = requests.post(url,json={'exp':exp,})
print(r.json())