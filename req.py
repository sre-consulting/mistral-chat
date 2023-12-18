import requests
import os

def get_response(prompt, model):
    url = "https://api.mistral.ai/v1/chat/completions"
    token = os.environ.get("MISTRAL_API_KEY")

    headers = {
        'Authorization': f'Bearer {token}'
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        return content
    else:
        return f"Error: Received status code {response.status_code}\n{response.text}"

def main():
    model = "mistral-medium"  # Default model
    while True:
        # User input for the prompt
        prompt = input("Enter your prompt (or 'exit' to quit, 'change model' to switch models): ")
        if prompt.lower() == 'exit':
            break
        elif prompt.lower() == 'change model':
            new_model = input("Enter the model name ('mistral-medium', 'mistral-small', 'mistral-tiny'): ")
            model = new_model
            print(f"Model changed to {model}")
            continue

        response = get_response(prompt, model)
        print(response)

if __name__ == "__main__":
    main()
