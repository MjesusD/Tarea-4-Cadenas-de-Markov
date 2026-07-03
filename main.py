import time
import sys

from corpus import CorpusLoader
from markov import MarkovChain


def guardar_resultados(resultados, archivo="resultados.txt"):
    with open(archivo, "w", encoding="utf-8") as f:

        f.write("=" * 50 + "\n")
        f.write("DESCRIPCIONES GENERADAS\n")
        f.write("=" * 50 + "\n\n")

        for i, descripcion in enumerate(resultados, start=1):
            f.write(f"{i:02d}. {descripcion}\n")


def memoria_modelo(modelo):
    total = sys.getsizeof(modelo.model)

    for state, transitions in modelo.model.items():
        total += sys.getsizeof(state)
        total += sys.getsizeof(transitions)

        for k, v in transitions.items():
            total += sys.getsizeof(k) + sys.getsizeof(v)

    return total


def generar_cartas(modelo):

    cantidad = int(input("\n¿Cuántas cartas desea generar?: "))

    resultados = []

    print("\n" + "=" * 50)
    print("CARTAS GENERADAS")
    print("=" * 50)

    for i in range(cantidad):
        descripcion = modelo.generate()
        resultados.append(descripcion)
        print(f"{i+1:02d}. {descripcion}")

    guardar_resultados(resultados)
    print("\nResultados guardados en resultados.txt")


def menu():
    print("\n" + "=" * 50)
    print("MENÚ")
    print("=" * 50)
    print("1. Mostrar estadísticas")
    print("2. Mostrar estados del modelo")
    print("3. Generar nuevas cartas")
    print("4. Demostración paso a paso")
    print("5. Salir")


def main():

    print("=" * 50)
    print("GENERACIÓN PROCEDURAL DE CONTENIDO")
    print("Cadena de Markov para cartas tipo Balatro")
    print("=" * 50)

  
    # PEDIR ORDEN 
    
    while True:
        try:
            orden = int(input("Seleccione el orden de la cadena (1-3): "))
            if orden in (1, 2, 3):
                break
            print("El orden debe ser 1, 2 o 3.")
        except ValueError:
            print("Ingrese un número válido.")

    print("\nCargando corpus...")

    loader = CorpusLoader()
    corpus = loader.load("cartas.txt")

    print(f"\nDescripciones : {loader.number_of_sentences()}")
    print(f"Palabras      : {loader.total_words()}")
    print(f"Vocabulario   : {loader.vocabulary_size()}")

    print("\nEntrenando modelo...")

  
    # MEDICIÓN REAL
    
    inicio = time.perf_counter()

    modelo = MarkovChain(order=orden)
    modelo.train(corpus)

    fin = time.perf_counter()

    tiempo_entrenamiento = fin - inicio
    memoria = memoria_modelo(modelo)

    print("\n" + "=" * 50)
    print("MEDICIÓN DEL MODELO")
    print("=" * 50)
    print(f"Tiempo de entrenamiento: {tiempo_entrenamiento:.6f} s")
    print(f"Memoria del modelo     : {memoria / 1024:.2f} KB")
    print("=" * 50)

  
    # MENÚ

    while True:

        menu()

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            modelo.print_statistics()

        elif opcion == "2":
            modelo.print_example_states()

        elif opcion == "3":
            generar_cartas(modelo)

        elif opcion == "4":
            modelo.generate_demo()

        elif opcion == "5":
            print("\nPrograma finalizado.")
            break

        else:
            print("\nOpción inválida.")


if __name__ == "__main__":
    main()