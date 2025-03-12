import json
import os

import dill

from blockchain.block import Block
from blockchain.transaction.transaction import Transaction

class Hippocampus:
    def __init__(self,arg):
        self.caminho_arquivo = "./memory/"+str(arg) + "memory" 
        diretorio = os.path.dirname(self.caminho_arquivo)
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                self.dados = dill.load(arquivo)

                # Verifica se o JSON tem o formato correto
                if not isinstance(self.dados, list):
                    raise ValueError("Formato inválido de memória. Criando nova...")
                
        except (FileNotFoundError, json.decoder.JSONDecodeError, ValueError):
            print("Creating memory...")
            self.dados = [Block.genesis()]
            self.salvar_memoria()

    def salvar_memoria(self):
        with open(self.caminho_arquivo, 'wb') as arquivo:
            dill.dump(self.dados, arquivo)

    
    def update_memory(self, block):
        if "blocks" not in self.dados:
            self.dados = []  # Corrige a estrutura caso esteja errada

        self.dados.append(dill.dumps(block))
        self.salvar_memoria()
        print("Bloco adicionado com sucesso!")

    def dejavu(self):
        blocks = []
        for block in self.dados:
            blocks.append(block)
        return [Block.genesis()]
        
