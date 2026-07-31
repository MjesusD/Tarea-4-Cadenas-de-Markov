from gpt2_perplexity import GPT2Perplexity


modelo = GPT2Perplexity()


texto = """
This Joker gains X0.25 Mult for every hand played without playing your most played poker hand has a 1 in 4 chance for played cards with Club suit give +3
 
"""


resultado = modelo.calcular(texto)


print(
    "Perplexity GPT-2:",
    resultado
)