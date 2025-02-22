import json
import os

class Hippocampus:
    def __init__(self,arg):
        self.caminho_arquivo = "./memory/"+str(arg) + "memory.json" 
        diretorio = os.path.dirname(self.caminho_arquivo)
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                self.dados = json.load(arquivo)

                # Verifica se o JSON tem o formato correto
                if not isinstance(self.dados, dict) or "blocks" not in self.dados:
                    raise ValueError("Formato inválido de memória. Criando nova...")
                
                print(f"DONE DONE {self.dados}\n{self.caminho_arquivo}")

        except (FileNotFoundError, json.decoder.JSONDecodeError, ValueError):
            print("Creating memory...")
            self.dados = {
                "blocks": [{
                    "transactions": [],
                    "last_hash": "genesis_hash",
                    "forger": "genesis",
                    "block_count": 0,
                    "timestamp": 0,
                    "signature": ""
                }]
            }
            self.salvar_memoria()
            print("DONE")

    def salvar_memoria(self):
        """Garante que o JSON seja salvo corretamente, evitando corrupção."""
        with open(self.caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(self.dados, arquivo, ensure_ascii=False, indent=4)

    def update_memory(self, block):
        """Adiciona um bloco à memória e salva no arquivo."""
        if "blocks" not in self.dados:
            self.dados["blocks"] = []  # Corrige a estrutura caso esteja errada

        self.dados["blocks"].append(block)
        self.salvar_memoria()
        print("Bloco adicionado com sucesso!")
