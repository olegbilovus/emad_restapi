import string
from abc import ABC, abstractmethod

from google import genai
from openai import OpenAI

from app.models.images import Language


class FixSentence(ABC):
    it_prefix = "correggi questa frase, non aggiungere altro, non aggiungere punteggiatura. "
    en_prefix = "fix this sentence, do not add anything, do not add punctuation. "

    @abstractmethod
    def fix(self, sentence: str, language: Language) -> str:
        pass

    def prefix(self, language: Language) -> str:
        return self.it_prefix if language == Language.it else self.en_prefix

    @staticmethod
    def clear_response(response: str) -> str:
        return response.rstrip().rstrip(string.punctuation)

    def is_working(self):
        try:
            self.fix("andiamo a mangare in montana", Language.it)
            return True
        except Exception:
            return False


class FixSentenceOpenAI(FixSentence):

    def __init__(self, base_url: str, api_key: str, model: str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def fix(self, sentence: str, language: Language) -> str:
        prefix = self.prefix(language)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prefix + sentence.capitalize()}]
        )

        return self.clear_response(completion.choices[0].message.content)


class FixSentenceGoogle(FixSentence):
    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def fix(self, sentence: str, language: Language) -> str:
        prefix = self.prefix(language)
        response = self.client.models.generate_content(
            model=self.model, contents=f"{prefix}{sentence.capitalize()}"
        )

        return self.clear_response(response.text)
