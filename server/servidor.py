from socket import AF_INET, socket, SOCK_DGRAM, gethostname
from pickle import dump, dumps, loads, load
import json
import os

DIRNAME = os.path.dirname(__file__)
HOST = gethostname()																														# Define o host como sistema local
PORT = 3333																																			# Define a porta
BUFSIZ = 65535																																	# Define o tamanho das mensagens
ADDR = (HOST, PORT)																															# Monta o endereço
server = socket(AF_INET, SOCK_DGRAM)																						# Configura para utilizar IV4 e conexão UDP
server.bind(ADDR)																																# Inicia o servidor
print('Listening at {}'.format(server.getsockname()))														# Mostrar o endereço de alocação

def refresh():																																	# Função para ler os filmes registrados no arquivo
	conteudo = open('{}/databases/Filmes.json'.format(DIRNAME)).read()																# Lê os dados do arquivo
	filmes = json.loads(conteudo)																									# Decodifica o objeto JSON

	return filmes																																	# Retorna a lista de filmes

def cadastrarFilme(filme):																											# Função para cadastrar novo filme
	recover = filmes = refresh()																									# Define duas variaveis com a lista de filmes, uma para operação e outra para tentar recuperar o arquivo em caso de erro
	new_filme = {}																																# Cria um dictionary
	new_filme["titulo"] = filme["titulo"]																					# Copia os dados para o dictionary
	new_filme["diretores"] = filme["diretores"].split(",")
	new_filme["atores"] = filme["atores"].split(",")
	new_filme["roteiristas"] = filme["roteiristas"].split(",")
	new_filme["likes"] = "0"
	new_filme["dislikes"] = "0"
	filmes.append(new_filme)																											# Adiciona o novo filme na lista
	try:																																					# Tenta gravar a nova lista no arquivo
		with open('{}/databases/Filmes.json'.format(DIRNAME),"w") as file:
			json.dump(filmes,file)
		return True																																	# Em caso de sucesso retorna true
	except:																																				# Caso dê erro grava a lista antiga
		with open('{}/databases/Filmes.json'.format(DIRNAME),"w") as file:
			json.dumps(recover,file)
		return False																																# Por conta do erro retorna false

def cadastrarUsuario(user):																										
	conteudo = open('{}/databases/Usuarios.json'.format(DIRNAME)).read()
	recover = users = json.loads(conteudo)
	new_user = {}																																
	new_user["username"] = user["username"]
	new_user["password"] = user["password"]

	try:																																					
		with open('{}/databases/Usuarios.json'.format(DIRNAME),"w") as file:
			json.dump(users,file)
		return True																																	
	except:																																				
		with open('{}/databases/Usuarios.json'.format(DIRNAME),"w") as file:
			json.dumps(recover,file)
		return False																																

while True:
	req, address = server.recvfrom(BUFSIZ)																				# Recebe a requisição e guarda os dados e o endereço do solicitante
	req = loads(req)																															# Decodifica o objeto JSON
	data = {}																																			# Cria um dictionary

	try:
		if(req["rota"] == "getFilmes"):																							# Caso a rota da requisição seja getFilmes
			data["response"] = refresh()																							# Armazena a lista de filmes na resposta
			server.sendto(dumps(data), address)																				# Envia a resposta para o solicitante
		
		elif(req["rota"] == "pushFilmes"):																					# Caso a rota da requisição seja pushFilmes
			data["response"] = cadastrarFilme(req)																		# Chama a função de cadastro passando os dados da requisição e armazena o retorno
			server.sendto(dumps(data), address)																				# Envia o retorno da função de cadastro ao solicitante

		else:																																				# Caso a rota não seja encontrada
			data["response"] = "Error 404 - Route Not Found"													# Armazena uma mensagem de erro
			print("request of {} result {}".format(address,data["response"]))					# Mostra o endereço e o erro no console
			server.sendto(dumps(data), address)																				# Envia a mensagem de erro ao solicitante
	
	except:																																				# Caso a requisição não tenha o campo rota
		print("request of {} without Route".format(address))												# Mostra responsavel pela requisição sem rota no console