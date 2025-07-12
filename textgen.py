import openai

async def generate_article(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Write an article about: {prompt}"}
        ]
    )
    return response.choices[0].message["content"]
