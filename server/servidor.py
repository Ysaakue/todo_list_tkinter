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
	#conteudo = open('{}/databases/Filmes.json'.format(DIRNAME)).read()																# Lê os dados do arquivo
	conteudo = open('Filmes.json').read()
	filmes = json.loads(conteudo)																									# Decodifica o objeto JSON

	return filmes																																	# Retorna a lista de filmes

def cadastrarFilme(filme):																											# Função para cadastrar novo filme
	recover = filmes = refresh()																									# Define duas variaveis com a lista de filmes, uma para operação e outra para tentar recuperar o arquivo em caso de erro
	
	if len(filmes) > 0:
		for und in filmes:
			if filme["titulo"] == und["titulo"]:
				retorno = {}
				retorno["return"] = False
				retorno["msg"] = "Filme já cadastrado"
				return retorno

	new_filme = {}																																# Cria um dictionary
	new_filme["titulo"] = filme["titulo"]																					# Copia os dados para o dictionary
	new_filme["diretores"] = filme["diretores"].split(",")
	new_filme["atores"] = filme["atores"].split(",")
	new_filme["roteiristas"] = filme["roteiristas"].split(",")
	new_filme["avalicoes"] = {}
	filmes.append(new_filme)																											# Adiciona o novo filme na lista
	try:																																					# Tenta gravar a nova lista no arquivo
		#with open('{}/databases/Filmes.json'.format(DIRNAME),"w") as file:
		with open('Filmes.json',"w") as file:
			json.dump(filmes,file)
		retorno = {}
		retorno["return"] = True
		return retorno																															# Em caso de sucesso retorna true
	except:																																				# Caso dê erro grava a lista antiga
		#with open('{}/databases/Filmes.json'.format(DIRNAME),"w") as file:
		with open('Filmes.json',"w") as file:
			json.dumps(recover,file)
		retorno = {}
		retorno["return"] = False
		retorno["msg"] = "Erro ao tentar cadastrar Filme"
		return retorno																														# Por conta do erro retorna false

def cadastrarUsuario(user):																										
	#conteudo = open('{}/databases/Usuarios.json'.format(DIRNAME)).read()
	conteudo = open('Usuarios.json').read()
	recover = users = json.loads(conteudo)
	if len(users) > 0:
		for und in users:
			if user["username"] == und["username"]:
				retorno = {}
				retorno["return"] = False
				retorno["msg"] = "Username já cadastrado"
				return retorno
	new_user = {}																																
	new_user["username"] = user["username"]
	new_user["password"] = user["password"]
	users.append(new_user)

	try:																																					
		#with open('{}/databases/Usuarios.json'.format(DIRNAME),"w") as file:
		with open('Usuarios.json',"w") as file:
			json.dump(users,file)
			retorno = {}
		retorno["return"] = True
		return retorno																															
	except:																																				
		#with open('{}/databases/Usuarios.json'.format(DIRNAME),"w") as file:
		with open('Usuarios.json',"w") as file:
			json.dumps(recover,file)
		retorno = {}
		retorno["return"] = False
		retorno["msg"] = "Erro ao tentar cadastrar usuário"
		return retorno																															

def fazerLogin(user):
	conteudo = open('Usuarios.json').read()
	users = json.loads(conteudo)
	if len(users) > 0:
		for und in users:
			if user["username"] == und["username"]:
				if user["password"] == und["password"]:
					retorno = {}
					retorno["return"] = True
					retorno["user"] = und
					return retorno
				else:
					retorno = {}
					retorno["return"] = False
					retorno["msg"] = "Senha incorreta"
					return retorno

	retorno = {}
	retorno["return"] = False
	retorno["msg"] = "Usuario não encontrado"
	return retorno

def like(filme, user):
	filmes = refresh()
	for filme2 in filmes:
		if filme2["titulo"] == filme:
			filme2["avaliacao"][user] = "like"
			with open('Filmes.json',"w") as file:
				json.dump(filmes,file)
			return True
	return False

def dislike(filme, user):
	filmes = refresh()
	for filme2 in filmes:
		if filme2["titulo"] == filme:
			filme2["avaliacao"][user] = "dislike"
			with open('Filmes.json',"w") as file:
				json.dump(filmes,file)
			return True
	return False

while True:
	req, address = server.recvfrom(BUFSIZ)																				# Recebe a requisição e guarda os dados e o endereço do solicitante
	req = loads(req)																															# Decodifica o objeto JSON
	data = {}																																			# Cria um dictionary

	if(req["rota"] == "getFilmes"):																							# Caso a rota da requisição seja getFilmes
		data["response"] = refresh()																							# Armazena a lista de filmes na resposta
	
	elif(req["rota"] == "pushFilmes"):																					# Caso a rota da requisição seja pushFilmes
		data["response"] = cadastrarFilme(req)																		# Chama a função de cadastro passando os dados da requisição e armazena o retorno

	elif(req["rota"] == "pushUsuarios"):
		data["response"] = cadastrarUsuario(req)

	elif(req["rota"] == "getUsuarios"):
		data["response"] = fazerLogin(req)

	elif(req["rota"] == "pushLike"):
		data["response"] = like(req["filme"], req["user"])

	elif(req["rota"] == "pushDislike"):
		data["response"] = dislike(req["filme"], req["user"])

	else:																																				# Caso a rota não seja encontrada
		data["response"] = "Error 404 - Route Not Found"													# Armazena uma mensagem de erro
		print("request of {} result {}".format(address,data["response"]))					# Mostra o endereço e o erro no console
		
	server.sendto(dumps(data), address)																				# Envia a mensagem de erro ao solicitante