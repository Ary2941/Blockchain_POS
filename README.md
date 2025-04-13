# Protótipo de sistema de pontos utilizando blockchain
## [x] - **Estrutura da Transação**
```sh
"transaction": {
	"sender_public_key":  "**INSERT PUBLIC KEY**",
	"amount":             "1707680000", 
	"type":               "ENTRADA",
	"employee_id":        "12345", 
	"location":           "37.235000,-115.811111",
	"replacing_id":       "XXXXXXXXXXXXXXXXXXXXXXXX",
	"replacement_reason": "Logou atrasado",
	"adjusted_by":        "employee_id", # futuramente será removida
	"id":"8d545cdde7ee11ef81308cb0e9c2871b",
	"signature":"1121481898640eece4c22c548b9aadd..."
  #"CH": int    #futuramente será adicionada
}
```

_Se "replacing_id" é None: a transação é tratada como não sendo ajuste_

## [x] - Passos para Calcular a Hora do Ponto
1. **mandar request para [timeapi](https://timeapi.io/api/Time/current/zone?timeZone=America/Sao_Paulo) e para [httpbin](https://httpbin.org/get) simultaneamente**
2. **pegar a hora atual do computador**
3. **fazer uma média entre os "datetimes"**
4. **retornar o timestamp**
## [x] - Passos para mandar a Localização Atual
1. **pegar posição atual do aparelho (via autorização do browser)** 
2. **retornar latitude e longitude**
## [x] - Passos para Calcular as Horas Trabalhadas
1. **Filtrar transações por funcionário (`employee_id`)**
2. **Identificar marcações de entrada (`ENTRADA`) e saída (`SAÍDA`)**
3. **Considerar apenas os registros mais recentes de cada período**
4. **Calcular o total de tempo trabalhado (somando os intervalos de entrada e saída)**.

Exemplo:

```sh
{
  "type": "ENTRADA",
  "employee_id": "EMP12345",
  "amount": 1707650000,
  "id": "txn_001"
}
```

```sh
{
  "type": "SAÍDA",
  "employee_id": "EMP12345",
  "amount": 1707680000,
  "id": "txn_002"
}
```

```sh
{
  "type": "ENTRADA",
  "employee_id": "EMP12345",
  "amount": 1707654321,
  "id": "txn_003"
  "adjustment" {
	  "id": "txn_001",
  }
}
```

__(1707680000−1707645000)/3600 = 9.5 horas__

## Executando

### Instalando dependências
```sh
pip install -r requirements/dev.txt
```

### Executando nós
```sh
# Terminal 1
cd blockchain ; python run_node.py --ip=localhost --node_port=8010 --api_port=8050 --key_file=./keys/genesis_private_key.pem ; cd ..
# Terminal 2
cd blockchain ; python run_node.py --ip=localhost --node_port=8011 --api_port=8051 --key_file=./keys/node1_private_key.pem ; cd ..
# Terminal 3
cd blockchain ; python run_node.py --ip=localhost --node_port=8012 --api_port=8052 --key_file=./keys/node2_private_key.pem ; cd ..
```
### OU rode pelo docker 

```sh
docker-compose up -d
```

### populate with seeds
```sh
cd blockchain ; python sample_transactions.py ; cd ..
```

### test routes
```sh
cd frontend ; python app.py ; cd ..
```

### test relatory
http://127.0.0.1:5000/relatory?employee_id={employee_id}&architects={employee_id,...}start={dd/mm/YYYY}&end={dd/mm/YYYY}


__Visualizar a blockchain pelo nó com a node_port fornecida__

```sh
http://localhost:8050/api/v1/blockchain/
```
__Visualizar todas as transações válidas__

```sh
http://localhost:8051/api/v1/transaction/
http://localhost:8051/api/v1/transaction?employee_id=123

```
__Visualizar carga horária__

```sh
http://localhost:8050/api/v1/transaction/CH?employee_id=123
```



__Através de [http://localhost:8010/transaction/CH/?employee_id=<employee_id>] consegue-se visualizar a blockchain pelo nó com a node_port fornecida__

## Testando transações

```sh
cd blockchain ; python app.py
```

## Adicões

geração do id de empregado pela chave que assina (caso arquivo pem inserido)



## TODO:
  [ ] - generate updated requirements.txt - 5/3/2025
  [ ] - generate more screens - 6/3/2025
  [ ] - understand the structure of the algorithm
  [ ] - add a way to gather personal information
  [ ] - add CH to the transaction
  [ ] - define a block size
  [ ] - test fork attack
  [ ] - optimize blockchain sharing/validation
  [ ] - update main page to get from route CH
  [ ] - create cryptify message e decryptify in wallet
  [ ] - create merkle root


  # OBS:
    a chave genesis é usada em proof_of _stake


  
15-03-2025 TODO:
  levando em conta que account_model é herdado em handle_blockchain
  no momento a blockchain está levando em consideração as chaves privadas que estão sendo 

  . quando um nó ser iniciado ele cria uma blockchain
  + blockchain.account_model.add_account(chave em hex do nó)
  + blockchain.account_model.update_balance(chave em hex do nó, quantidade)
  + quando nó ser conectado ele rode add_account
  .. daí quando o novo nó herdar a blockchain ele também vai herdar os balanços
  - retirar modificações de balanç e contas em blockchain (excepto quando identificar fraude)
  - não levar em consideração a chave pública do bloco e sim do bloco
  .. provavelmente vou usar a função discovery para criar uma inocação gêmea, ao mesmo temo que vai enviar o socket ela vai enviar os balanços