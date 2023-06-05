import openai

enter1 = "olá"


def chat2(enter2):
    try:
        openai.api_key = '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'
        responseOpenai = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[
                {"role": "system", "content":enter2}
            ],
            max_tokens=200
        )
        response = responseOpenai['choices'][0]['message']['content']
        print(response)
        chat1(response)
    except openai.APIError as e:
        response = "Erro... Openai não respondendo..."



def chat1(enter1):
    try:
        openai.api_key = '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'
        responseOpenai = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[
                {"role": "system", "content":enter1}
            ],
            max_tokens=200
        )
        response = responseOpenai['choices'][0]['message']['content']
        print(response)
        chat2(response)
    except openai.APIError as e:
        response = "Erro... Openai não respondendo..."


chat1(enter1)