import requests, re, random
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("Token")
print("Imported T0KEN")

title = "This took so long"
Model = "sentence-transformers/all-MiniLM-L6-v2"
API = f"https://router.huggingface.co/hf-inference/models/{Model}"
Head = {"Authorization":f"Bearer {API_KEY}"}
TH = 0.75
#Input1 = str(input("Enter sentence #1:\n"))
Input1 = "I love ice-cream sundaes and theyre amazing"
#Input2 = str(input("Enter sentence #2:\n"))
Input2 = "Sushi with soy sauce is amazing"
Data = (Input1,Input2)

TOK = lambda s:" | ".join(s.split())
bar = lambda s:"█"*int(s*10)+"░"*(10-int(s*10))
clean = lambda t:[w for w in (re.sub(r"[^a-z0-9']+","",x.lower()) for x in t.split()) if w]
nums = lambda t:set(re.findall(r"\d+(?:\.\d+)?"), t)
has_any = lambda t,arr:any(a in set(clean(t)) for a in arr)

def hf(q1,q2):
    r=requests.post(API, headers=Head, json={"inputs":{"source_sentence":q1,"sentences":[q2]}})
    if not r.status_code == 200:
        print(f"Error {r.status_code}")
    else:
        data = r.json()
        if isinstance(data, dict):
            print("Error: Data is in a dictionary", str(data))
        else:
            return float(data[0])
        
def score(base,q1,q2,confidence):
    w1 = {w for w in clean(q1) if len(w)>=4}
    w2 = {w for w in clean(q2) if len(w)>=4}
    jac = len(w1&w2)/max(1, len(w1|w2))
    boost = (0.04 if len(confidence)>=2 else 0) + (0.03 if jac>=0.20 else 0)
    negA=["not","no","never","without","can't","cant","cannot","don't","dont","won't","wont","n't"]
    oppA=[("increase","decrease"),("bigger","smaller"),("more","less"),("add","remove"),("open","close"),("enable","disable")]
    num_pen = 0.1 if (nums(q1) and nums(q2) and nums(q1)!=nums(q2)) else 0
    neg_pen = 0.12 if has_any(q1, negA)!=has_any(q2, negA) else 0
    opp_pen = 0.12 if any((has_any(q1,[a]) and has_any(q2,[b]) or has_any(q1,[b]) and has_any(q2,[a])) for a,b in oppA) else 0
    return max(0.0, min(1.0, base+boost-num_pen-neg_pen-opp_pen))

def label(s): return "✅ DUPLICATE" if s>=TH else ("🤔 CLOSE MATCH" if s>=TH-0.05 else "❌ DIFFERENT")
def show_result(s):
    print(f"\n🎯 Result of Similarity: {round(s*100,1)}% [{bar(s)}]  →  {label(s)}")
    print(f"Rule: score ≥ {TH} means DUPLICATE")

def show_flow(q1,q2):
    a,b=clean(q1),clean(q2); raw=set(a+b)
    w1={w for w in a if len(w)>=4}; w2={w for w in b if len(w)>=4}
    shared=sorted(w1&w2)
    helpers=sorted({w for w in raw if 2<=len(w)<=3})
    conn={"a","an","the","to","of","in","on","is","am","are","do","did","does","my","me","it"}
    least=sorted({w for w in raw if len(w)<=2 or w in conn})
    print("\nFLOW (sentence -> strongest/helper/least -> similarity %)")
    print("\n1) Input sentences \n")
    print(f"Q1:{q1}\n Q2:{q2}")
    print("\n2) Split words into tokens")
    print("\nQ1 ->", TOK(q1),"  Q2 ->", TOK(q2))
    print("\n3) Pick the key words from input")
    print(" Strongest:",", ".join(shared) if shared else "No Key Words Found")
    print(" Helper:",", ".join(helpers) if helpers else "No helpers found")
    print(" Least:",", ".join(least) if least else "None")
    print("\n4) Why similarity is high or low for this pair")
    print(" - Direct matches:",", ".join(shared)) if shared else  print(" - The model used overall meaning patterns, not exact word matches.")

def run(q1,q2,title):
    print(f"\n--- {title} ---")
    base=hf(q1,q2)
    strong=sorted({w for w in clean(q1) if len(w)>=4} & {w for w in clean(q2) if len(w)>=4})
    s=score(base,q1,q2,strong)
    show_result(s); show_flow(q1,q2)

def main():
    print("Type Question 1 → Question 2. Then you’ll see 2 RANDOM demo pairs.")
    print("Type 'exit' anytime to quit.\n")
    while True:
        q1=input("Question 1: ").strip()
        if q1.lower()=="exit": break
        q2=input("Question 2: ").strip()
        if q2.lower()=="exit": break
        if not q1 or not q2: continue
        try:
            run(q1,q2,"YOUR QUESTIONS")
            run(Input1,Input1,f"RANDOM DEMO {title}")
            print("\n(Next round → Question 1 or 'exit')\n")
        except Exception as e:
            print("Oops!",e,"\n")

if __name__=="__main__": main()