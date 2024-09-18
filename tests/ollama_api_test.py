from openai import OpenAI

client = OpenAI(
    # local host ollama  base_url='http://localhost:11434/v1',
    # model list is  llamafamily/llama3-chinese-8b-instruct:latest
    base_url='http://localhost:11434/v1',
    # base_url='http://125.69.16.175:11434/v1',
    # required, but unused
    api_key='ollama',
)

response = client.chat.completions.create(
    # model="Llama3-8B-Chinese-Chat:latest",
    model="llamafamily/llama3-chinese-8b-instruct:latest",
    messages=[
        {"role": "system", "content": "中文回复"},
        {"role": "assistant", "content": "你是一个ai助手"},
        {"role": "user", "content": "你好"},
        # {"role": "assistant", "content": ""},
        {"role": "user", "content": "如何理解复里叶变换"}
    ]
)
print(response.choices[0].message.content)
