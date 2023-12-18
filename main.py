import os
import asyncio
import sys
from dotenv import load_dotenv
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage
from colorama import Fore, Style, init

load_dotenv()
init(autoreset=True)

async def change_model():
    print(f"{Fore.YELLOW}Available models: mistral-medium, mistral-small, mistral-tiny")
    return input(f"{Fore.YELLOW}Enter model name: {Style.RESET_ALL}")

async def get_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line == 'END': break
        if line == '/exit': sys.exit(0)
        lines.append(line)
    return "\n".join(lines)

async def perform_chat(client, model, system_msg ,message):
    async for chunk in client.chat_stream(
        model=model,
        messages=[
            ChatMessage(role="system", content=system_msg),
            ChatMessage(role="user", content=message)
        ]
    ):
        if chunk.choices[0].delta.content is not None:
            print(f"{Fore.GREEN}{chunk.choices[0].delta.content}{Style.RESET_ALL}", end="")

async def main():
    api_key = os.getenv("MISTRAL_API_KEY")
    system_msg = os.getenv("MISTRAL_SYS_SMG", "Reply concisely, in an extremely concise manner.")
    model = "mistral-medium"
    client = MistralAsyncClient(api_key=api_key)

    try:
        while True:
            message = await get_input(f"{Fore.BLUE}Enter question (type 'END' to finish):{Style.RESET_ALL}")
            if message.lower() == 'change model':
                model = await change_model()
                print(f"{Fore.GREEN}Model changed to {model}{Style.RESET_ALL}")
            elif message.lower() == 'exit':
                break
            else:
                print("--------")
                await perform_chat(client, model, system_msg, message)
                print("\n--------")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
