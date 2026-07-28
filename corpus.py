"""
Este módulo se encarga únicamente de leer el archivo de texto y
convertir cada descripción en una lista de tokens.
"""

import re

"""
Esta clase se encarga de cargar al corpus desde un txt y tokenizar cada 
descripción en una lista de palabras.
"""
class CorpusLoader:

    def __init__(self):
        self.sentences = []
        self.vocabulary = set()

    def tokenize(self, text):
        """
        Tokeniza el texto conservando valores como X0.25 o +3.5 como un solo token.
        """
        pattern = r"\+\d+(?:[.,]\d+)?|X\d+(?:[.,]\d+)?|[^\W\d_]+|\d+(?:[.,]\d+)?"
        tokens = re.findall(pattern, text, flags=re.UNICODE)
        return tokens

    def load(self, filename):
        """
        Retorna una lista de listas de palabras.
        """
        
        self.sentences.clear()
        self.vocabulary.clear()

        with open(filename, "r", encoding="utf-8") as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                tokens = self.tokenize(line)

                self.sentences.append(tokens)

                self.vocabulary.update(tokens)

        return self.sentences

    def vocabulary_size(self):
        """
        Número de palabras distintas del corpus.
        """
        return len(self.vocabulary)

    def number_of_sentences(self):
        """
        Número de descripciones.
        """
        return len(self.sentences)

    def total_words(self):
        """
        Cantidad total de palabras.
        """
        return sum(len(sentence) for sentence in self.sentences)