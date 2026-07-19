# Generación Procedural de Descripciones mediante Cadenas de Markov

## Descripción

Proyecto desarrollado en Python para generar descripciones de cartas inspiradas en el juego Balatro utilizando cadenas de Markov.

## Requisitos

- Python 3.11 o superior

## Archivos
- main.py
- markov.py
- cartas.txt

## Ejecución

```bash
python main.py
```

o

```bash
py main.py
```

## Salida

El programa genera nuevas descripciones siguiendo el estilo aprendido del corpus de entrenamiento.


## Funcionamiento Paso a Paso

El sistema genera nuevas descripciones de cartas mediante el siguiente flujo secuencial:

1. **Carga y Tokenización del Corpus:** Se lee el archivo de texto y se extraen las palabras y símbolos clave (como `+4` o `X2`) utilizando expresiones regulares en `corpus.py`.

2. **Construcción de Estados y Transiciones:** En `markov.py`, se añaden marcadores especiales de inicio y fin (`<START>` y `<END>`) a cada descripción y se asocia cada ventana de $k$ palabras consecutivas (estado) con la palabra que le sigue inmediatamente, contabilizando su frecuencia.

3. **Generación Estocástica:** Se inicializa la frase en el estado de inicio. Mediante una selección aleatoria ponderada por la frecuencia de las transiciones aprendidas, se va eligiendo la siguiente palabra más probable.

4. **Desplazamiento y Unión:** En cada paso de generación, la ventana del estado se desliza para incorporar la palabra elegida. El proceso se detiene al seleccionar `"<END>"` o alcanzar el límite de palabras, tras lo cual se unen los tokens con espacios para formar la frase final.
