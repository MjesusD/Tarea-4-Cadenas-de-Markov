import csv
import spacy
from collections import Counter


def cargar_modelos(idioma):
    """
    Carga el modelo spaCy según el idioma.

    idioma = 1 -> Español
    idioma = 2 -> Inglés
    """

    if idioma == 1:
        return spacy.load("es_core_news_sm")
    else:
        return spacy.load("en_core_web_sm")



def calcular_ttr(tokens):
    """
    Calcula la diversidad léxica
    Type-Token Ratio (TTR)
    """

    if len(tokens) == 0:
        return 0

    return len(set(tokens)) / len(tokens)



def analizar_gramatica(texto, nlp):
    """
    Analiza estructura gramatical usando spaCy.
    """

    doc = nlp(texto)


    pos = Counter(
        token.pos_
        for token in doc
        if not token.is_punct
    )


    dependencias = Counter(
        token.dep_
        for token in doc
        if not token.is_punct
    )


    tiene_verbo = any(
        token.pos_ == "VERB"
        for token in doc
    )


    tiene_root = any(
        token.dep_ == "ROOT"
        for token in doc
    )


    return {

        "verbos_pos": pos["VERB"],

        "sustantivos_pos": pos["NOUN"],

        "adjetivos_pos": pos["ADJ"],

        "adverbios_pos": pos["ADV"],

        "preposiciones_pos": pos["ADP"],

        "tiene_verbo": tiene_verbo,

        "tiene_root": tiene_root,

        "dependencias": dependencias

    }



def evaluar_oracion(oracion, nlp, modelo):
    """
    Evalúa una descripción generada.
    """

    doc = nlp(oracion)


    palabras = [
        token.text.lower()
        for token in doc
        if not token.is_punct and not token.is_space
    ]


    verbos = sum(
        1 for token in doc
        if token.pos_ == "VERB"
    )


    sustantivos = sum(
        1 for token in doc
        if token.pos_ == "NOUN"
    )


    adjetivos = sum(
        1 for token in doc
        if token.pos_ == "ADJ"
    )


    diversidad = calcular_ttr(palabras)


    gramatica = analizar_gramatica(
        oracion,
        nlp
    )


    perplexity = modelo.perplexity(
        oracion
    )


    return {

        "palabras": len(palabras),

        "verbos": verbos,

        "sustantivos": sustantivos,

        "adjetivos": adjetivos,

        "diversidad": diversidad,

        "perplexity": perplexity,

        "tiene_verbo": gramatica["tiene_verbo"],

        "tiene_root": gramatica["tiene_root"],

        "dependencias": str(
            gramatica["dependencias"]
        )

    }


def guardar_csv(nombre_csv, resultados):

    campos = [

        "descripcion",

        "palabras",

        "verbos",

        "sustantivos",

        "adjetivos",

        "diversidad",

        "perplexity",

        "tiene_verbo",

        "tiene_root",

        "dependencias"

    ]


    with open(
        nombre_csv,
        "w",
        newline="",
        encoding="utf8"
    ) as archivo:


        writer = csv.DictWriter(
            archivo,
            fieldnames=campos
        )


        writer.writeheader()

        writer.writerows(resultados)



def mostrar_resumen(resultados):

    total = len(resultados)


    if total == 0:

        print(
            "No se encontraron descripciones."
        )

        return



    promedio_palabras = sum(
        r["palabras"]
        for r in resultados
    ) / total


    promedio_verbos = sum(
        r["verbos"]
        for r in resultados
    ) / total


    promedio_sustantivos = sum(
        r["sustantivos"]
        for r in resultados
    ) / total


    promedio_adjetivos = sum(
        r["adjetivos"]
        for r in resultados
    ) / total


    promedio_ttr = sum(
        r["diversidad"]
        for r in resultados
    ) / total


    promedio_perplexity = sum(
        r["perplexity"]
        for r in resultados
    ) / total



    con_verbo = sum(
        1
        for r in resultados
        if r["tiene_verbo"]
    )


    porcentaje_verbo = (
        con_verbo / total
    ) * 100



    print("\n" + "=" * 55)

    print("EVALUACIÓN LINGÜÍSTICA")

    print("=" * 55)


    print(
        f"Descripciones analizadas : {total}"
    )

    print(
        f"Promedio palabras        : {promedio_palabras:.2f}"
    )

    print(
        f"Promedio verbos          : {promedio_verbos:.2f}"
    )

    print(
        f"Promedio sustantivos     : {promedio_sustantivos:.2f}"
    )

    print(
        f"Promedio adjetivos       : {promedio_adjetivos:.2f}"
    )

    print()

    print(
        f"Diversidad léxica TTR    : {promedio_ttr:.3f}"
    )

    print(
        f"Perplexity promedio      : {promedio_perplexity:.3f}"
    )

    print()

    print(
        f"Descripciones con verbo  : {porcentaje_verbo:.2f}%"
    )


    print("=" * 55)



def evaluar_archivo(nombre_archivo, idioma, modelo):
    """
    Evalúa todas las descripciones generadas.
    """

    print(
        "\nAnalizando descripciones..."
    )


    nlp = cargar_modelos(
        idioma
    )


    resultados = []


    with open(
        nombre_archivo,
        encoding="utf8"
    ) as archivo:


        for linea in archivo:


            linea = linea.strip()


            if not linea:
                continue


            if not linea[:2].isdigit():
                continue



            try:

                descripcion = linea.split(
                    ". ",
                    1
                )[1]


            except IndexError:

                continue



            datos = evaluar_oracion(
                descripcion,
                nlp,
                modelo
            )


            resultados.append({

                "descripcion": descripcion,

                "palabras": datos["palabras"],

                "verbos": datos["verbos"],

                "sustantivos": datos["sustantivos"],

                "adjetivos": datos["adjetivos"],

                "diversidad": datos["diversidad"],

                "perplexity": datos["perplexity"],

                "tiene_verbo": datos["tiene_verbo"],

                "tiene_root": datos["tiene_root"],

                "dependencias": datos["dependencias"]

            })



    nombre_csv = nombre_archivo.replace(
        ".txt",
        "_evaluacion.csv"
    )


    guardar_csv(
        nombre_csv,
        resultados
    )


    mostrar_resumen(
        resultados
    )


    print(
        f"\nArchivo CSV generado: {nombre_csv}"
    )