from tkinter import Tk, Button, PhotoImage, Label, Menu, Entry, Frame, Scrollbar, DISABLED, ttk
from socket import AF_INET, socket, SOCK_DGRAM, gethostname
from pickle import loads, dumps
from datetime import date

HOST = gethostname()																														# Define o host como sistema local
PORT = 3333																																			# Define a porta como 33343
BUFSIZ = 65535																																	# Define o tamanho das mensagens
ADDR = (HOST, PORT)																															# Monta o endereço
server = socket(AF_INET, SOCK_DGRAM)																						# Define a familia de endereços como IPV4 e coneção como UDP

class Interface(Tk):
	def __init__(self,parent):																										# Método construtor
		Tk.__init__(self,parent)																										# Chama init da classe Tk
		self.parent = parent																												# Define a conexão com parent
		
		self.attributes('-fullscreen',True)																					# Inicia janela em tela cheia
		self.currentScreem = ""																											# Variavel de controle para gerar telas
		self.currentUser = {}
		self.currentUser["logado"] = False
		self.titulos_treeview = ["Titulo", "Diretores", "Roteiristas","Atores"]			# Cabeçario para treeview

		self.menu()																																	# Chama o metodo para criar menu
		self.Home()																																	# Chama o método para criar a estrutura da janela

	def menu(self):																																# Método para criar menu
		topo = self.winfo_toplevel()																								# Cria widget na parte superior para o menu
		self.menuBar = Menu(topo)																										# Cria uma barra de menus nesta janela
			
		mnuOpcoes = Menu(self.menuBar, tearoff=0)																		# Cria o menu Opções
		mnuOpcoes.add_command(label="Sobre", command=self.processaSobre)						# Adiciona a função "Sobre" que mostra uma explicação sobre a janela
		mnuOpcoes.add_command(label="Sair", command=self.processaSair)							# Adiciona a função "Sair" que destroi a janela suas janelas filhas
		self.menuBar.add_cascade(label="Opções", menu=mnuOpcoes)										# Adiciona as funções no menu Opções

		topo.config(menu=self.menuBar)																							# Posiciona o menu no topo da janela
		
	def toobar(self,screem):																											# Método para criar a barra de funcionalidades
		self.toobarFrame = Frame(self)																							# Cria o Frame onde irão ficar os botões
		self.toobarFrame.pack(side="top",pady=5,fill="x")														# Posiciona o Frame no topo da janela
		
		# Button de home
		self.homeB=Button(self.toobarFrame,justify = "left", command=self.Home)
		self.photoHome=PhotoImage(file="img/home.png")
		self.homeB.config(image=self.photoHome,width="20",height="20")
		self.homeB.pack(side="left", padx=5)
		if screem == "home":																												# Verifica se é a tela de cadastro para gerar botão home
			self.homeB.config(state="disabled")
		
		# Button de recarregar
		self.refreshB=Button(self.toobarFrame,justify = "left",											# Cria o botão para recarregar lista
													command=self.handleRefresh)
		self.photoRefresh=PhotoImage(file="img/refresh.png")												# Cria uma imagem com referencia a um Refresh Icon
		self.refreshB.config(image=self.photoRefresh,width="20",height="20")				# Associa a imagem ao botão
		self.refreshB.pack(side="left")																							# Posiciona o botão ao lado esquerdo do Frame
		if screem != "home":
			self.refreshB.config(state="disabled")

		# Entry de busca
		self.searchE = Entry(self.toobarFrame)																			# Cria um Entry para digitar busca
		self.searchE.pack(side="left",padx=5)																				# Posiciona o Entry ao lado esquerdo do Frame com espaçamento lateral
		self.searchE.bind("<Return>",lambda x: self.handleSearch())									# Faz busca com enter
		if screem != "home":
			self.searchE.config(state="disabled")

		# Button de busca
		self.searchB=Button(self.toobarFrame,justify = "left",											# Cria o botão para realizar busca lista
													command=self.handleSearch)
		self.photoSearch=PhotoImage(file="img/search.png")													# Cria uma imagem com referencia a um Search Icon
		self.searchB.config(image=self.photoSearch,width="20",height="20")					# Associa a imagem ao botão
		self.searchB.pack(side="left")																							# Posiciona o botão ao lado esquerdo do Frame
		if screem != "home":
			self.searchB.config(state="disabled")

		# Button de adicionar filme
		self.addB=Button(self.toobarFrame,justify = "left",												# Cria o botão para adicionar um filme a lista
											command=self.SubscribeMovie)
		self.photoAdd=PhotoImage(file="img/add.png")															# Cria uma imagem com referencia a um Add Icon
		self.addB.config(image=self.photoAdd,width="20",height="20")							# Associa a imagem ao botão
		self.addB.pack(side="left", padx=5)																				# Posiciona o botão ao lado esquerdo do Frame
		if screem == "subscribe":																										# Verifica se é a home e gera botão para tela de cadastro
			self.addB.config(state="disabled")
		
		if screem != "sign":
			if self.currentUser["logado"] == True:
				# Button de logout
				self.logoutB=Button(self.toobarFrame,justify = "left",
													command=self.handleLogout)
				self.photoLogout=PhotoImage(file="img/logout.png")
				self.logoutB.config(image=self.photoLogout,width="20",height="20")
				self.logoutB.pack(side="right", padx=5)
				self.lblUser = Label(self.toobarFrame, text="{}".format(self.currentUser),
															bg='gray25', fg = 'white smoke')
				self.lblUser.pack(side="right",padx=5)
			else:
				# Button de signin
				self.signinB=Button(self.toobarFrame,justify = "left",
													command=self.SignIn)
				self.photoLogin=PhotoImage(file="img/login.png")
				self.signinB.config(image=self.photoLogin,width="20",height="20")
				self.signinB.pack(side="right", padx=5)

	def Home(self):																																# Método para gerar tela inicial
		if self.currentScreem == "signIn":																					# Verifica de estava na tela de login
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas da tela inicial
			self.SigninScreem.pack_forget()																									# Apaga tela de login
		elif self.currentScreem == "subscribeMovie":																# Verifica se estava na tela de cadastro de filmes
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas
			self.subscribeMovieScreem.pack_forget()																		# Apaga tela de cadastro de filmes
		elif self.currentScreem == "signUp":																				# Verifica de estava na tela de login
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas da tela inicial
			self.SignupScreem.pack_forget()																						# Apaga tela de login

		self.toobar("home")																													# Cria barra de ferramentas para home
		
		self.homeScreem = Frame(None)																								# Cria frame para tela de login
		self.homeScreem.pack(fill="both")

		self.tree = ttk.Treeview(	self.homeScreem,columns=self.titulos_treeview,		# Cria TreeView para exibir os filmes
															show="headings")
		self.scbar = Scrollbar(self.homeScreem,orient="vertical",										# Cria ScrollBar para lista de filmes
														command=self.tree.yview)
		self.tree.configure(yscrollcommand=self.scbar.set)													# Configura para TreeView usar a ScrollBar
		
		self.scbar.pack(side="right", fill="y")																			# Posiciona ScrollBar no lado direito para preencher a altura
		self.tree.pack(side="top", fill='x')																				# Posiciona a lista no top preenchendo lateralmente
		
		self.handleRefresh()																												# Recarrega para renderizar a lista de filmes

		self.currentScreem = "home"																									# Define que a tela atual é a home, por conta de referencia

	def SubscribeMovie(self):																											# Método para gerar tela de cadastro de filmes
		if self.currentScreem == "signIn":																					# Verifica de estava na tela de login
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas da tela inicial
			self.SigninScreem.pack_forget()																									# Apaga tela de login
		elif self.currentScreem == "home":																					# Verifica se estava na tela inicial
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas da tela inicial
			self.homeScreem.pack_forget()																							# Apaga tela tela inicial
		elif self.currentScreem == "signUp":																				# Verifica de estava na tela de login
			self.SignupScreem.pack_forget()																						# Apaga tela de login
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas da tela inicial

		self.toobar("subscribe")																										# Cria barra de ferramentas para tela de cadastro de filmes

		self.subscribeMovieScreem = Frame(None)																			# Cria frame para tela de cadastro de filmes
		self.subscribeMovieScreem.pack()

		# Titulo
		self.lblTitulo = Label(self.subscribeMovieScreem, text="Título")						# Cria label para título
		self.lblTitulo.pack()																												# Pocisiona na interface
		self.entryTitulo = Entry(self.subscribeMovieScreem)													# Cria input para título
		self.entryTitulo.pack()																											# Pocisiona na interface

		# Atores
		self.lblAtores= Label(self.subscribeMovieScreem,														# Cria label para atores
														text="Atores(separar por virgula)")
		self.lblAtores.pack()																												# Posiciona na interface
		self.entryAtores = Entry(self.subscribeMovieScreem)													# Cria input para atores
		self.entryAtores.pack()																											# Posiciona na interface

		#Diretores
		self.lblDiretores= Label(self.subscribeMovieScreem,													# Cria label para diretores
															text="Diretores(separar por virgula)")
		self.lblDiretores.pack()																										# Posiciona na interface
		self.entryDiretores = Entry(self.subscribeMovieScreem)											# Cria input para diretores
		self.entryDiretores.pack()																									# Posiciona na interface

		# Roteiristas
		self.lblRoteiristas= Label(self.subscribeMovieScreem,												# Cria label para roteiristas
																text="Roteiristas(separar por virgula)")
		self.lblRoteiristas.pack()																									# Posiciona na interface
		self.entryRoteiristas = Entry(self.subscribeMovieScreem)										# Cria input para roteiristas
		self.entryRoteiristas.pack(pady=5)																					# Posiciona na interface com espaçamento vertical

		self.btnCadastrar = Button(	self.subscribeMovieScreem,text=u"Cadastrar",		# Cria botão para enviar formulario de cadastro
																command=self.handleCadastroFilme)
		self.btnCadastrar.pack(pady=10,side="bottom")																# Posiciona botão na parte inferior da janela com espaçamento vertical

		self.lblres= Label(self.subscribeMovieScreem, text="")											# Cria campo para mensagens ao usuario, inicialmente em branco
		self.lblres.pack()																													# Posiciona na interface

		self.currentScreem = "subscribeMovie"																				# Define que a tela atual é a subscribeMovie, por conta de referencia
		
	def SignIn(self):
		if self.currentScreem == "subscribeMovie":																	# Verifica se estava na tela de cadastro de filmes
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas
			self.subscribeMovieScreem.pack_forget()																		# Apaga tela de cadastro de filmes
		elif self.currentScreem == "home":																					# Verifica se estava na tela inicial
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas da tela inicial
			self.homeScreem.pack_forget()																							# Apaga tela tela inicial
		elif self.currentScreem == "signUp":																				# Verifica de estava na tela de login
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas da tela inicial
			self.SignupScreem.pack_forget()																						# Apaga tela de login
		
		self.toobar("sign")
		self.SigninScreem = Frame(None)
		self.SigninScreem.pack()

		# Username
		user = Frame(self.SigninScreem)
		self.lblUsername = Label(user, text="Username")
		self.lblUsername.pack(side="left")
		self.entryUsername = Entry(user)
		self.entryUsername.pack(side="left")
		user.pack()

		# Password
		passw = Frame(self.SigninScreem)
		self.lblPassword = Label(passw, text="Password")
		self.lblPassword.pack(side="left")
		self.entryPassword = Entry(passw, show="*")
		self.entryPassword.pack(side="left")
		passw.pack()

		# Button de signup
		self.signupB=Button(self.SigninScreem,
											command=self.SignUp)
		self.photoSignup=PhotoImage(file="img/ncadastrado.png")
		self.signupB.config(image=self.photoSignup)
		self.signupB.pack(side="bottom")
		
		self.btnCadastrar = Button(	self.SigninScreem,text=u"Login",
																command=self.handleLogin)
		self.btnCadastrar.pack(pady=10,side="bottom")

		self.lblres= Label(self.SigninScreem, text="")
		self.lblres.pack()

		self.currentScreem = "signIn"

	def SignUp(self):
		if self.currentScreem == "subscribeMovie":																	# Verifica se estava na tela de cadastro de filmes
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas
			self.subscribeMovieScreem.pack_forget()																		# Apaga tela de cadastro de filmes
		elif self.currentScreem == "home":																					# Verifica se estava na tela inicial
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas da tela inicial
			self.homeScreem.pack_forget()																							# Apaga tela tela inicial
		elif self.currentScreem == "signIn":																				# Verifica de estava na tela de login
			self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas da tela inicial
			self.SigninScreem.pack_forget()																						# Apaga tela de login

		self.toobar("sign")
		
		self.SignupScreem = Frame(None)
		self.SignupScreem.pack()

		# Username
		user = Frame(self.SignupScreem)
		self.lblUsername = Label(user, text="Username")
		self.lblUsername.pack(side="left")
		self.entryUsername = Entry(user)
		self.entryUsername.pack(side="right",pady=3)
		user.pack()

		# Password
		passw = Frame(self.SignupScreem)
		self.lblPassword = Label(passw, text="Password")
		self.lblPassword.pack(side="left",padx=2)
		self.entryPassword = Entry(passw,show="*")
		self.entryPassword.pack(side="right",pady=3)
		passw.pack()

		# Confirm Password
		passw = Frame(self.SignupScreem)
		self.lblPassword = Label(passw, text="Confirm \nPassword")
		self.lblPassword.pack(side="left",padx=2)
		self.entryCPassword = Entry(passw,show="*")
		self.entryCPassword.pack(side="right")
		passw.pack()

		# Button de signin
		self.signinB=Button(self.SignupScreem,justify = "left",
											command=self.SignIn)
		self.photoLogin=PhotoImage(file="img/cadastrado.png")
		self.signinB.config(image=self.photoLogin)
		self.signinB.pack(side="bottom")
		
		self.btnSignup = Button(	self.SignupScreem,text=u"SignUp",
																command=self.handleSignUp)
		self.btnSignup.pack(pady=10,side="bottom")

		self.lblres= Label(self.SignupScreem, text="")
		self.lblres.pack()

		self.currentScreem = "signUp"

	def OnDoubleClick(self, event):																								# Método para identificar item clicado na lista
		item = self.tree.selection()																								# Identifica item clicado
		for i in item:
			self.info(self.tree.item(i, "values")[0])																	# Chama método para mostrar os dados do filme

	def info(self, titulo):																												# Método para mostrar informações do filme
		for filme in self.filmes:																										# Percorre os filmes
			if titulo == filme['titulo']:																							# Busca o filme com titulo correspondente para mostrar as informações
				info=filme
				break
		try: 																																				# Tenta destruir as informações e mostra as informações do filme
			self.lblTituloFilme.destroy()
			self.lblAtoresFilme.destroy()
			self.lblDiretoresFilme.destroy()
			self.lblRoteiristasFilme.destroy()
			#titulo
			self.lblTituloFilme = Label(self.homeScreem,
				text="TITULO:\n {}".format(info["titulo"]))
			self.lblTituloFilme.pack()
			#atores
			self.lblAtoresFilme = Label(self.homeScreem, 
				text="ATORES:\n {}".format("\n".join(info["atores"])))
			self.lblAtoresFilme.pack()
			#diretores
			self.lblDiretoresFilme = Label(self.homeScreem,
				text="DIRETORES:\n {}".format("\n".join(info["diretores"])))
			self.lblDiretoresFilme.pack()
			#roteiristas
			self.lblRoteiristasFilme = Label(self.homeScreem,
				text="ROTEIRISTAS:\n {}".format("\n".join(info["roteiristas"])))
			self.lblRoteiristasFilme.pack()
		except:																																			# Caso não existam entra em exeção e somente mostra as informações
			#titulo
			self.lblTituloFilme = Label(self.homeScreem,
				text="TITULO:\n {}".format(info["titulo"]))
			self.lblTituloFilme.pack()
			#atores
			self.lblAtoresFilme = Label(self.homeScreem,
				text="ATORES:\n {}".format("\n".join(info["atores"])))
			self.lblAtoresFilme.pack()
			#diretores
			self.lblDiretoresFilme = Label(self.homeScreem,
				text="DIRETORES:\n {}".format("\n".join(info["diretores"])))
			self.lblDiretoresFilme.pack()
			#roteiristas
			self.lblRoteiristasFilme = Label(self.homeScreem,
				text="ROTEIRISTAS:\n {}".format("\n".join(info["roteiristas"])))
			self.lblRoteiristasFilme.pack()

	def onlyRefresh(self):																												# Método para buscar filmes no servidor
		data = {}																																		# Cria dictionary
		data["rota"] = "getFilmes"																									# Define a rota para pegar os filmes no servidor
		server.sendto(dumps(data), ADDR)																						# Envia o dictionary
		
		response, address = server.recvfrom(BUFSIZ)																	# Recebe uma mensagem do servidor
		response = loads(response)																									# Decodifica a mensagem
		self.filmes = response["response"]																					# Atribui os filmes a um atributo da classe

	def handleRefresh(self):																											# Método para receber os filmes do servidor e renderizar na tela
		self.onlyRefresh()																													# Chama método para atualizar os filmes
		self.renderFilmes(self.filmes)																							# Chama o método para renderizar os filmes

	def handleSearch(self):																												# Método para fazer buscas nos filmes que já estão
		busca = self.searchE.get()																									# Recebe string para fazer busca
		filmes_busca = []																														# Cria lista
		self.onlyRefresh()																													# Chama método para atualizar lista de filmes
		
		for filme in self.filmes:																										# Faz busca nos filmes
			if busca.lower() in filme['titulo'].lower():
				filmes_busca.append(filme)

		self.renderFilmes(filmes_busca)																							# Chama método para renderizar filmes que batem com a busca

	def renderFilmes(self, filmes):																								# Método para renderizar filmes na tela
		for i in self.tree.get_children():																					# Apaga todos os filmes já na tela
			self.tree.delete(i)
		
		for col in self.titulos_treeview:																						# Monta cabeçario da treeview
			self.tree.heading(col, text=col.title())

		for filme in filmes:																												# Percorre filmes e inseri na treeview
			item = (filme['titulo'], ", ".join(filme['diretores']),
							", ".join(filme['roteiristas']),", ".join(filme['atores']))
			self.tree.insert('', 'end', values=item)
		
		self.tree.pack(side="top", fill='x')																				# Posiciona a treeview na tela preenchendo 
		self.tree.bind("<Double-1>", self.OnDoubleClick)														# Espera evento de click

	def handleCadastroFilme(self):																								# Método que envia requisição para o cadastro de um filme
		titulo = self.entryTitulo.get()																							# Pega os dados do input
		atores = self.entryAtores.get()
		diretores = self.entryDiretores.get()
		roteiristas = self.entryRoteiristas.get()

		if len(titulo)<1 or len(atores)<1 or len(diretores)<1 or len(roteiristas)<1:# Caso todos os inputs estejam vazios
			self.changeMSG("Todos os campos devem ser preenchidos",'red',"subscribe")	# Mostra mensagem de erro com cor vermelha
		
		else:
			data = {}																																	# Cria dictionary
			data["rota"] = "pushFilmes"																								# Atribui os dados para o dictionary com os dados do filme
			data["titulo"] = titulo
			data["atores"] = atores
			data["diretores"] = diretores
			data["roteiristas"] = roteiristas
			server.sendto(dumps(data), ADDR)																					# Envia a reuisição e os dados para o servidor
			response, address = server.recvfrom(BUFSIZ)																# Recebe a resposta da requisição
			response = loads(response)																								# Decodifica o objeto JSON
			if(response["response"]):																									# Caso a resposta seja true
				self.changeMSG("Cadastrado com sucesso","green","subscribe")						# Mostra mensagem de sucesso com cor verde
			else:																																			# Caso a resposta seja false
				self.changeMSG("Erro ao cadastrar","blue","subscribe")									# Mostra mensagem de erro com cor azul

	def handleLogin(self):
		user = self.entryUsername.get()
		passw = self.entryPassword.get()
		cpassw = self.entryCPassword.get()

		if len(user)<1 or len(passw)<1:
			self.changeMSG("Todos os campos devem ser preenchidos",'red',"login")

	def handleLogout(self):
		print("")

	def handleSignUp(self):
		user = self.entryUsername.get()
		passw = self.entryPassword.get()
		cpass = self.entryCPassword.get()

		if len(user)<1 or len(passw)<1 or len(cpass)<1:
			self.changeMSG("Todos os campos devem ser preenchidos",'red',"signup")
		elif passw != cpass:
			self.changeMSG("A senhas não são iguais",'red',"signup")
		else:
			data = {}

	def changeMSG(self,texto,color,screem):																							# Método para mudar a mensagem
		self.lblres.destroy()																												# Destroi a antiga mensagem
		if screem == "sbscribe":
			self.lblres= Label(self.subscribeMovieScreem, text=texto,										# Cria novo label com o texto e cor de fundo passada
													bg='{}'.format(color))
		elif screem == "login":
			self.lblres= Label(self.SigninScreem, text=texto,bg='{}'.format(color))
		
		elif screem == "signup":
			self.lblres= Label(self.SignupScreem, text=texto,bg='{}'.format(color))

		self.lblres.pack(pady=5, side="bottom")																			# Posiciona na parte de baixo da janela com espaçamento vertical

	def processaSobre(self):																											# Método para mostrar uma janela para mostrar mais sobre o programa
		root = Tk()																																	# Cria a janela de ajuda
		root.title('Sobre cliente')																									# Especifica o título da janela
		root.geometry('600x200')																										# Define as dimenssões da janela

		text = Label(root, text=	'Essa é uma interface para vizualização de filmes'# Define o texto para ser exibido
															' registrados em nosso servidor.\n\n'
															
															'TUTORIAL(HOME):\n'
															'- O primeiro botão é para recarregar a lista, '
															'ele vai solicitar novamente todos os filmes '
															'cadastrados.\n'

															'- O input é para digitar palavras chaves para '
															'realizar busca.\n'
															
															'- O segundo botão é para realizar a busca.\n'
															
															'- O terceiro botão serve para adicionar um novo '
															'filme no catalogo.\n\n'
															
															'TUTORIAL(SubsribeMovie):\n'
															'- Todos o campos devem ser preenchidos com os '
															'dados do filmes. Caso possua mais de um nome\n'
															'   para atores, diretores ou roteiristas devem '
															'ser separados por virgula.'
															, justify="left")
		text.pack()																																	# Posiciona o texto na janela
		root.mainloop()

	def processaSair(self):																												# Método para destruir janela do cliente
		self.destroy()

if __name__ == "__main__":
	i = Interface(None)
	i.mainloop()