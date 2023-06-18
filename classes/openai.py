import openai


def chat(enter):
    try:
        openai.api_key = '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'
        print(enter)
        responseOpenai = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[
                {"role": "system", "content":enter}
            ],
            max_tokens=500
        )
        response = responseOpenai['choices'][0]['message']['content']
        print(response)
        return response
    except openai.APIError as e:
        response = "Erro... Openai não respondendo..."
        print(e)
        return e