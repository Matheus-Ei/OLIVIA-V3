from googletrans import Translator

def translation(text, lang):
    translator = Translator()
    
    traducao = translator.translate(text, dest=lang)

    return(traducao.text)
