import random


# CORPUS DE DESCRIPCIONES

descripciones_balatro = [

    "Otorga mas cuatro Multiplicador si la mano jugada contiene un Par.",
    "Otorga mas cien fichas si la mano jugada es un Color.",
    "Cada carta con figura jugada otorga mas treinta fichas.",
    "Otorga mas doce Multiplicador si te queda un descarte al final de la ronda.",
    "Los de tipo Color y Full de reyes otorgan el doble de fichas.",
    "Otorga mas ocho Multiplicador por cada carta de Corazones en tu mano.",
    "Esta carta otorga mas doscientos fichas si la mano contiene una Escalera.",
    "Esta carta otorga dos descartes si jugaste una Escalera Real.",
    "Si la carta jugada es Holografica otorga mas diez Multiplicador.",
    "Si la carta jugada es Policromatica otorga por uno punto cinco Multiplicador.",
    "Cada As jugado otorga mas cincuenta fichas.",
    "Cada carta de Picas otorga mas tres Multiplicador.",
    "Otorga mas veinte fichas por cada Par presente.",
    "Cada carta de Trebol otorga mas diez fichas.",
    "Otorga mas ciento cincuenta fichas si la mano jugada es Poker.",
    "Otorga mas cinco Multiplicador si la mano contiene Trio.",
    "Otorga mas quince Multiplicador si jugaste Full House.",
    "Esta carta otorga un descarte adicional al inicio de cada ronda.",
    "Cada carta impar jugada otorga mas dos Multiplicador.",
    "Las figuras de Diamantes otorgan el doble de fichas."

]


# PREPROCESAMIENTO
texto = " ".join(descripciones_balatro)
palabras = texto.split()

# MODELO ORDEN 1

cadena_markov_1 = {}

for i in range(len(palabras)-1):

    actual = palabras[i]
    siguiente = palabras[i+1]

    if actual not in cadena_markov_1:
        cadena_markov_1[actual] = []

    cadena_markov_1[actual].append(siguiente)


# MODELO ORDEN 2

cadena_markov_2 = {}

for i in range(len(palabras)-2):

    estado = (palabras[i], palabras[i+1])
    siguiente = palabras[i+2]

    if estado not in cadena_markov_2:
        cadena_markov_2[estado] = []

    cadena_markov_2[estado].append(siguiente)


#generar orden 1

def generar_orden1(inicio="Otorga", max_palabras=15):

    if inicio not in cadena_markov_1:
        inicio = random.choice(list(cadena_markov_1.keys()))

    texto = [inicio]

    for _ in range(max_palabras-1):

        actual = texto[-1]

        if actual not in cadena_markov_1:
            break

        siguiente = random.choice(cadena_markov_1[actual])

        texto.append(siguiente)

        if siguiente.endswith("."):
            break

    return " ".join(texto)


# GENERADOR ORDEN 2

def generar_orden2(inicio=("Otorga","mas"), max_palabras=15):

    posibles = [k for k in cadena_markov_2 if k[0] == inicio[0]]

    if len(posibles)==0:
        estado = random.choice(list(cadena_markov_2.keys()))
    else:
        estado = random.choice(posibles)

    texto = list(estado)

    for _ in range(max_palabras-2):

        if estado not in cadena_markov_2:
            break

        siguiente = random.choice(cadena_markov_2[estado])

        texto.append(siguiente)

        estado = (estado[1], siguiente)

        if siguiente.endswith("."):
            break

    return " ".join(texto)

# (Preparado para ORDEN 3)

'''
cadena_markov_3 = {}
estado = (p1,p2,p3)
...
def generar_orden3(...)
'''

def main():

    print("========== ORDEN 1 ==========\n")

    for i in range(5):
        print(f"Joker {i+1}: {generar_orden1()}")

    print("\n========== ORDEN 2 ==========\n")

    for i in range(5):
        print(f"Joker {i+1}: {generar_orden2()}")

main()

print("\nFin del programa")