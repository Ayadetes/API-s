import requests
import random
import html

EDUCATION_CATEGORY_ID = 9

API_URL = f"https://opentdb.com/api.php?amount=10&category={EDUCATION_CATEGORY_ID}&type=multiple"

def get_question():
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        if data["response_code"] == 0 and data['results']:
            return data['results']
    return None

def run_quiz():
    questions = get_question()
    
    if not questions:
        print("Failed to get questions")
        return
    
    score = 0

    print("Dr. Binocs Triva Time!")

    for i,q in enumerate(questions, 1):

        questions = html.unescape(q['question'])
        correct = html.unescape(q['correct_answer'])
        incorrects = [html.unescape(a) for a in q['incorrect_answers']]


        options = incorrects + [correct]
        random.shuffle(options)

        print(f"Question {i}: {questions}")
        for idx,option in enumerate(options,1):
            print(f"    {idx}.  {option}")

        while True:
            try:
                choice = int(input("\nYour answer(1-4)\n"))
                if 1<= choice <= 4:
                    break
            except ValueError:
                pass
            print("Invalid input; try again")
        
        if options[choice-1] == correct:
            print("Correct")
        else:
            print(f"Incorrect the correct answer is {correct}\n")
    
    print(f"Final Score: {score}/{len(questions)}")
    print(f"Percentage: {score/len(questions)*100:.1f}%")

if __name__ == "__main__":
    run_quiz()