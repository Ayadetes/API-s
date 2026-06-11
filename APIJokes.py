import requests

def get_joke():
    url = "https://official-joke-api.appspot.com/jokes/random"
    response = requests.get(url)


    if response.status_code == 200:
        print(f"Full JSON Response: {response.json()}")  
        joke_data = response.json()
        return f"{joke_data['setup']} - {joke_data['punchline']}"
    else:
        return "Failed To Retrieve Joke"
    
def main():
    print("Hello")

    while True:
        input_user = input("Get a random joke by pressing enter or press q to quit")
        
        if input_user == "q":
            break
        else:
            joke = get_joke()
            print(joke)

if __name__ == "__main__":
    main()
