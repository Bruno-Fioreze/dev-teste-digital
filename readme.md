
### Dependências

- Python
- Django
- Django-Rest
- Docker
- Pip


## Passos para executar a aplicação.
Caso esteja utilizando windows troque o python3 por python.

- Execute o seguinte comando:
- sudo docker run -p 3306:3306 --name db_digital -e MYSQL_ROOT_PASSWORD=db_digital -d mysql:latest
- Entre na pasta do projeto.
- Execute o comando python3 -m venv venv
- No caso do linux, ative a venv com source venv/bin/activate
- No caso do windows, ative a venv com venv/Scripts/Activate
- Execute o comando pip install -r requirements.txt
- Execute o comando python3 manage.py runserver

## End-Poins - Users :
- End-Point

	> http://127.0.0.1:8000/users/

- Verbo HTTP
	> POST

- Entrada
	> CPF Campo Obrigatório.
	> first_name = Obrigatório.
	> last_name= Obrigatório.
- Saída
    	
		{
			user": {
        	"id": 1,
        	"first_name": "Bruno",
        	"last_name": "Fioreze",
        	"cpf": 47949295893
		},
			"pk_account": 1
		}

- End-Point

	> http://127.0.0.1:8000/users/

- Verbo HTTP
	> GET

- Entrada
	> Sem Obrigatório.

- Saída

	[
    	{
        	"id": 1,
        	"first_name": "Bruno",
        	"last_name": "Fioreze",
        	"cpf": 47949295899
    	},
	]

## End-Poins - Transaction :

- End-Point

	> http://127.0.0.1:8000/transaction/

- Verbo HTTP
	> GET

- Entrada
	 Sem Campo Obrigatório

- Saída

		[
			{
				"id": 21,
 			   "value": 2000.00,
 			   "account_shipping": 192,
 			   "account_received": 192,
 		 	  "type_operation": 1
		   }
	   ]

- End-Point

	> http://127.0.0.1:8000/transaction/

- Verbo HTTP
	> POST

- Entrada
	> value Obrigatório.
	> account_shipping Obrigatório.
	> account_shipping Obrigatório.
	> type_operation Obrigatório.

- Saída

		{
			"id": 21,
			"value": "2000.00",
			"account_shipping": 192,
			"account_received": 192,
			"type_operation": 1
		}


## End-Poins - Account :

- End-Point

	> http://127.0.0.1:8000/account/balance/

- Verbo HTTP
	> GET

- Entrada
	> CPF Obrigatório.

- Saída

		{
			"balance": 2000.0
		}


## Comandos para executar os testes.
	> python3 manage.py test bank.tests.TestUserBank
	> python3 manage.py test bank.tests.TransactionBank
	> python3 manage.py test bank.tests.TransactionBank.test_transaction_bank_get_200
	
## Um pouco sobre a aplicação.
A aplicação foi feita utilizando Python, Django, Django-Rest, Docker e UnitTest
Ela é bem simples e todo o código desenvolvido se encontra no app bank.

## Observações
- Password
Eu não tratei a geração de password, pois é um teste.
- Relacionamento User e Account
Eu coloquei a chave estrangeira em Account, pois futuramente se for necessário adicionar outro tipo de conta o sistema aceitará facilmente.