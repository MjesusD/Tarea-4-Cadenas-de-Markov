
from collections import defaultdict, Counter
import random
import math



class MarkovChain:
    """
    Implementa una cadena de Markov de orden configurable.

    """

    def __init__(self, order=2, seed=None):

        self.order = order
        self.vocabulary = set()

        # Estado -> Counter(siguientes palabras)
        self.model = defaultdict(Counter)

        # Estadísticas
        self.num_states = 0
        self.num_transitions = 0

        if seed is not None:
            random.seed(seed)


    def train(self, corpus):
        """
        Entrena la cadena de Markov.

        """

        self.model.clear()

        for sentence in corpus:
            
            self.vocabulary.update(sentence)

            # <START> <START> palabra1 palabra2 ...
            tokens = ["<START>"] * self.order
            tokens.extend(sentence)
            tokens.append("<END>")

            for i in range(len(tokens) - self.order):

                state = tuple(tokens[i:i+self.order])

                next_word = tokens[i+self.order]

                self.model[state][next_word] += 1

        self.num_states = len(self.model)

        self.num_transitions = sum(
            sum(counter.values())
            for counter in self.model.values()
        )

  

    def generate(self, max_words=30):
        """
        Genera una nueva descripción.
        """

        state = ("<START>",) * self.order

        sentence = []

        while len(sentence) < max_words:

            if state not in self.model:
                break

            possible_words = list(self.model[state].keys())

            weights = list(self.model[state].values())

            next_word = random.choices(
                possible_words,
                weights=weights,
                k=1
            )[0]

            if next_word == "<END>":
                break

            sentence.append(next_word)

            state = state[1:] + (next_word,)

        return " ".join(sentence)


    def transition_probability(self, state, word):
        """
        Devuelve la probabilidad P(word/state).
        """

        if state not in self.model:
            return 0.0

        total = sum(self.model[state].values())

        if total == 0:
            return 0.0

        return self.model[state][word] / total


    def perplexity(self, sentence):
        """
        Calcula la perplexity de una descripción utilizando el modelo
        entrenado de Markov.

        Parámetros
        ----------
        sentence : str | list
            Descripción a evaluar.

        Retorna
        -------
        float
            Perplexity de la descripción.
        """

        if isinstance(sentence, str):
            sentence = sentence.split()

        tokens = ["<START>"] * self.order
        tokens.extend(sentence)
        tokens.append("<END>")

        vocab_size = len(self.vocabulary)

        log_probability = 0.0
        total_words = 0

        for i in range(len(tokens) - self.order):

            state = tuple(tokens[i:i+self.order])
            next_word = tokens[i+self.order]

            transitions = self.model.get(state, Counter())

            total = sum(transitions.values())

            # Suavizado de Laplace
            probability = (
                transitions[next_word] + 1
            ) / (
                total + vocab_size
            )

            log_probability += math.log2(probability)

            total_words += 1

        return 2 ** (-log_probability / total_words)


    def average_perplexity(self, descriptions):
        """
        Calcula la perplexity promedio de varias descripciones.
        """

        if len(descriptions) == 0:
            return 0

        total = 0

        for description in descriptions:

            total += self.perplexity(description)

        return total / len(descriptions)


    def print_statistics(self):

        print("\n" + "=" * 45)
        print("ESTADÍSTICAS DEL MODELO")
        print("=" * 45)

        print(f"Orden de la cadena        : {self.order}")
        print(f"Número de estados         : {self.num_states}")
        print(f"Número de transiciones    : {self.num_transitions}")
        print(f"Tamaño del vocabulario    : {len(self.vocabulary)}")

        promedio = self.num_transitions / self.num_states

        print(f"Transiciones por estado   : {promedio:.2f}")

        print("=" * 45)


    def generate_demo(self, max_words=30):

        print("\n")
        print("=" * 50)
        print("DEMOSTRACIÓN PASO A PASO")
        print("=" * 50)

        state = ("<START>",) * self.order

        sentence = []

        paso = 1

        while len(sentence) < max_words:

            if state not in self.model:
                break

            print(f"\nPaso {paso}")
            print("-" * 40)

            print("Estado actual:")
            print(state)

            possible_words = list(self.model[state].keys())

            weights = list(self.model[state].values())

            total = sum(weights)

            print("\nTransiciones posibles:")

            for word, weight in zip(possible_words, weights):

                porcentaje = weight / total * 100

                print(f"{word:15} {weight:3d} veces ({porcentaje:5.1f}%)")

            next_word = random.choices(
                possible_words,
                weights=weights,
                k=1
            )[0]

            print("\nPalabra elegida:")
            print(next_word)

            if next_word == "<END>":

                print("\nSe alcanzó el estado final.")
                break

            sentence.append(next_word)

            state = state[1:] + (next_word,)

            paso += 1

            print("\n" + "=" * 50)
            print("DESCRIPCIÓN GENERADA")
            print("=" * 50)

            print(" ".join(sentence))

            print("=" * 50)


    def print_example_states(self, limit=10):
    
        print("\nEJEMPLOS DE ESTADOS\n")

        shown = 0

        for state, transitions in self.model.items():

            print("=" * 40)
            print("Estado:", state)

            total = sum(transitions.values())

            for word, count in transitions.items():

                prob = count / total

                print(
                    f"  -> {word:15}"
                    f" Frecuencia={count:3d}"
                    f" Prob={prob:.2%}"
                )

            shown += 1

            if shown >= limit:
                break