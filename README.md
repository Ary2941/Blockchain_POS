# Protótipo de sistema de pontos utilizando blockchain
## **[ ] - Estrutura da Transação**
```sh
"transaction": {
	"sender_public_key":"**INSERT PUBLIC KEY**",
	"amount": "1707680000", 
	"type":"ENTRADA",
	"employee_id": "12345", 
	"supervisor_id": "67890",
	"location": { 
		"latitude": "37.235000", 
		"longitude": "-115.811111"
	}, 
	"adjustement": {
		"id":"XXXXXXXXXXXXXXXXXXXXXXXX",
		"reason":"Logou atrasado",
		"adjusted_by":(employee_id do supervisor)
	},
	"id":"8d545cdde7ee11ef81308cb0e9c2871b",
	"signature":"1121481898640eece4c22c548b9aadd..."
}
```
_Se "adjustement" é {}: a transação é tratada como não sendo ajuste_
## [x] - Passos para Calcular a Hora do Ponto
1. **mandar request para [timeapi](https://timeapi.io/api/Time/current/zone?timeZone=America/Sao_Paulo) e para [httpbin](#https://httpbin.org/get) simultaneamente**
2. **pegar a hora atual do computador**
3. **fazer uma média entre os "datetimes"**
4. **retornar o timestamp**
## [x] - Passos para mandar a Localização Atual
1. **pegar posição atual do aparelho (via autorização do browser)** 
2. **retornar latitude e longitude**
## [ ] - Passos para Calcular as Horas Trabalhadas
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


## Instalando dependências
```sh
pip install -r requirements/dev.txt
```

## Executando nós
```sh
# Terminal 1
python run_node.py --ip=localhost --node_port=8010 --api_port=8050 --key_file=./keys/genesis_private_key.pem
# Terminal 2
python run_node.py --ip=localhost --node_port=8011 --api_port=8051 --key_file=./keys/staker_private_key.pem
# Terminal 3
python run_node.py --ip=localhost --node_port=8012 --api_port=8052
```
__Através de [http://localhost:{node_port}/api/v1/blockchain/] consegue-se visualizar a blockchain pelo nó com a node_port fornecida__

## Testando transações

```sh
python app.py
```