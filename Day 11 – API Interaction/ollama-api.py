import requests
import json
def ollama_test(prompt,model='qwen3:4b',timeout=120,stream=False):
    url="http://localhost:11434/api/generate"
    payload={
        'model':model,
        'stream':stream,
        'prompt':prompt,
        'timeout':timeout
    }
    headers={"Content-Type":"application/json"}
    response=requests.post(url,json=payload,headers=headers)
    try:
        if response.status_code!=200:
            print(f"response code is {response.status_code}")
            return
        if not stream:
            data=response.json()
            print(data['response'])
            return
        full_text=[]
        for line in response.iter_lines():
            if line:
                data=json.loads(line.decode('utf-8'))
                token=data.get("response","")
                full_text.append(token)
        print("".join(full_text))
    except Exception as e:
        print(f"Error: {e}")

if __name__=="__main__":
    ollama_test("about Ai",stream=True)
