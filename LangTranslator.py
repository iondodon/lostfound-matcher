from googletrans import Translator


class LangTranslator:
    def __init__(self, to_lang):
        self.to_lang = to_lang
        self.translator = Translator()

    def translate(self, text):
        return self.translator.translate(text, dest=self.to_lang).text