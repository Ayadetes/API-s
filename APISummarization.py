from config import HF_API_KEY_READ
import requests
from colorama import *

DefaultModel = "google/pegasus-xsum"
init(autoreset=True)

def build_model(name):
    return f"https://api-inference.huggingface.co/models/{name}"

def query(payload, model=DefaultModel):
    """
    Sends a request to Hugging Face API for pegasus
    """
    
    APIURL = build_model(model)
    headers = {"Authorization": f"Bearer {HF_API_KEY_READ}"}
    response = requests.post(APIURL, headers=headers, json=payload)

    return response.json()

def Summarize(text,min,max,model=DefaultModel):
    payload = {
        "input": text,
        "parameters": {"min_length": min, "max_length": max}
    }

    print(Fore.BLUE + f"\n???? Summarizing with {model}")

    result = query(payload, model=model)

    if isinstance(result, list) and result and "summary_text" in result[0]:
        return result[0]["summary_text"]
    else:
        print(Fore.RED + f"Error Response: {result}")
        return None
    
if __name__ == "__main__":
    print(Fore.YELLOW + "Hi whats your name:")
    user = input("")
    if not user:
        user = "Eraser"
    print(Fore.GREEN + f"Welcome {user}. We can summarize your text")
    print(Fore.YELLOW + Style.BRIGHT +"\nEnter your text down here:")
    user_input = input("> ").strip()
    if not user_input:
        print(Fore.Red + "No input")
    else:
        MODEL = input("Enter the LLM you would like to summarize your text:\n")
        if not MODEL:
            MODEL = DefaultModel
        print(Fore.YELLOW + "\nChoose summary style:")
        print("\n1. Standard Summarization (Quick and Consice)")
        print("2. Enhanced Summary (More Detailed and Refined)")
        Style = input("Enter your answer (1 or 2)").strip()
        if Style == 2:
            min = 80
            max = 200
            print(Fore.BLUE + "You inputted choice 2")
        elif Style == 1:
            min = 50
            max = 150
            print(Fore.BLUE + "You chose choice 1")

        summary = Summarize(user_input, min, max, model=MODEL)

        if summary:
            print("Summary successfully created for", user,"\n")
            print(Fore.GREEN + summary)
        else:
            print(Fore.RED + "Failed to generate")
            
