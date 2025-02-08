import string

from openai import OpenAI

from app.models.images import Language


class FixSentence:
    it_prefix = "correggi questa frase, non aggiungere altro, non aggiungere punteggiatura. "
    en_prefix = "fix this sentence, do not add anything, do not add punctuation. "

    def __init__(self, base_url: str, api_key: str, model: str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def fix(self, sentence: str, language: Language) -> str:
        prefix = self.it_prefix if language == Language.it else self.en_prefix
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prefix + sentence}]
        )

        return completion.choices[0].message.content.rstrip().rstrip(string.punctuation)
