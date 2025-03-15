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
            print(self.caminho_arquivo)
            with open(self.caminho_arquivo, 'rb') as arquivo:
                data = []
                self.dados = dill.load(arquivo)
                for n in self.dados:
                    data.append(dill.loads(n))
                self.dados = data
                # Verifica se o JSON tem o formato correto
                if not isinstance(self.dados, list):
                    raise ValueError("Formato inválido de memória. Criando nova...")
                
        except Exception as e:
            print(f"{e}Creating memory...")
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
        print(f"Bloco {len(self.dados)} adicionado com sucesso!")

    def dejavu(self):
        print("DEJAVU BLOCKS")
        blocks = []
        for block in self.dados:
            blocks.append(block)
        print(blocks)
        return blocks
        
