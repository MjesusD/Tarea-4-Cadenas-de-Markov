import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class GPT2Perplexity:

    def __init__(self):

        print("Cargando GPT-2...")

        self.tokenizer = GPT2Tokenizer.from_pretrained(
            "gpt2"
        )

        self.model = GPT2LMHeadModel.from_pretrained(
            "gpt2"
        )

        self.model.eval()

        print("GPT-2 cargado correctamente")


    def calcular(self, texto):

        tokens = self.tokenizer(
            texto,
            return_tensors="pt"
        )


        with torch.no_grad():

            salida = self.model(
                **tokens,
                labels=tokens["input_ids"]
            )


        loss = salida.loss


        perplexity = torch.exp(
            loss
        )


        return perplexity.item()