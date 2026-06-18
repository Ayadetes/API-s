import requests

url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"

def getfact():
    response = requests.get(url)
    if response.status_code == 200:
        fact_data = response.json()
        print(f"did you know {fact_data['text']}")
    else:
        print("error")

while True:
    control = input("Enter for a fact and q to quit")
    if control.lower() == "q":
        break
    getfact()