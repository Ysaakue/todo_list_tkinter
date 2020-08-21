from tkinter import Tk, Button, PhotoImage, Label, Menu, Entry, Frame, Scrollbar, ttk
from datetime import date
from banco import Banco
class Interface(Tk):
  def __init__(self,parent):																										# Método construtor
    Tk.__init__(self,parent)																										# Chama init da classe Tk
    self.parent = parent																												# Define a conexão com parent
    
    self.attributes('-fullscreen',True)																					# Inicia janela em tela cheia
    self.currentScreem = ""																											# Variavel de controle para gerar telas
    self.currentUser = {}
    self.currentUser["logado"] = False
    self.titulos_treeview = ["Id", "Descricao", "Data"]			# Cabeçario para treeview

    self.menu()																																	# Chama o metodo para criar menu
    self.Home()																																	# Chama o método para criar a estrutura da janela

  def menu(self):																																# Método para criar menu
    topo = self.winfo_toplevel()																								# Cria widget na parte superior para o menu
    self.menuBar = Menu(topo)																										# Cria uma barra de menus nesta janela
      
    mnuOpcoes = Menu(self.menuBar, tearoff=0)																		# Cria o menu Opções
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

    self.infoFrame = Frame(self.homeScreem)
    self.infoFrame.pack()

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
    
  def OnDoubleClick(self, event):																								# Método para identificar item clicado na lista
    item = self.tree.selection()																								# Identifica item clicado
    for i in item:
      self.renderInfo(self.tree.item(i, "values")[0])																	# Chama método para mostrar os dados do filme

  def renderInfo(self, titulo):																												# Método para mostrar informações do filme
    for filme in self.tarefas:																										# Percorre os filmes
      if titulo == filme['titulo']:																							# Busca o filme com titulo correspondente para mostrar as informações
        self.info=filme
        break
    self.infoFrame.pack_forget()

    self.infoFrame = Frame(self.homeScreem)

    #titulo
    self.lblTituloFilme = Label(self.infoFrame, justify="left",
      text="TITULO:\n - {}".format(self.info["titulo"]), anchor="w")
    self.lblTituloFilme.pack(fill="x")
    #atores
    self.lblAtoresFilme = Label(self.infoFrame, justify="left",
      text="ATORES:\n - {}".format(", ".join(self.info["atores"])), anchor="w")
    self.lblAtoresFilme.pack(fill="x")
    #diretores
    self.lblDiretoresFilme = Label(self.infoFrame, justify="left",
      text="DIRETORES:\n - {}".format(", ".join(self.info["diretores"])), anchor="w")
    self.lblDiretoresFilme.pack(fill="x")
    #roteiristas
    self.lblRoteiristasFilme = Label(self.infoFrame, justify="left", anchor="w",
      text="ROTEIRISTAS:\n - {}".format(", ".join(self.info["roteiristas"])))
    self.lblRoteiristasFilme.pack(fill="x")
    
    like = 0
    dislike = 0
    for key in self.info["avaliacao"]:
      if self.info["avaliacao"][key] == "like":
        like+=1
      else:
        dislike+=1
    
    #likes
    self.lblLikesFilme = Label(self.infoFrame, justify="left", anchor="w",
      text="\nLIKES: {}".format(like))
    self.lblLikesFilme.pack(fill="x")
    #dislikes
    self.lblDislikesFilme = Label(self.infoFrame, justify="left", anchor="w",
      text="DISLIKES: {}".format(dislike))
    self.lblDislikesFilme.pack(fill="x")

    if self.currentUser["logado"]:
      self.avaliacaoFrame = Frame(self.infoFrame)
      try:
        avaliacao = self.info["avaliacao"][self.currentUser]
      except:
        avaliacao = "avaliar"

      if avaliacao == "avaliar":
        self.likebnt = Button(self.avaliacaoFrame, text="Like",
                                command=self.handleLike)
        self.likebnt.pack(side="left",padx=2)
        self.dislikebnt = Button(self.avaliacaoFrame, text="Dislike",
                                command=self.handleDislike)
        self.dislikebnt.pack(side="left",padx=2)
      
      elif avaliacao == "like":
        self.likebnt = Button(self.avaliacaoFrame, text="Liked",
                                state="disabled")
        self.likebnt.pack()
      
      else:
        self.dislikebnt = Button(self.avaliacaoFrame, text="Disliked",
                                state="disabled")
        self.dislikebnt.pack()

      self.avaliacaoFrame.pack()
    
    self.infoFrame.pack(fill="x")

  def onlyRefresh(self):																												# Método para buscar filmes no servidor
    banco = Banco()
    try:
      c = banco.conexao.cursor()
      c.execute("select * from tarefas;")
      self.tarefas = []
      for linha in c:
        obj = {}
        obj["id"] = linha[0]
        obj["descricao"] = linha[1]
        obj["data"] = linha[2]
        self.tarefas.append(obj)
      c.close()
      return "Busca feita com sucesso!"
    except:
      return "Ocorreu um erro na busca do usuário"
    
  def handleRefresh(self):																											# Método para receber os filmes do servidor e renderizar na tela
    self.onlyRefresh()																													# Chama método para atualizar os filmes
    self.renderFilmes(self.tarefas)																							# Chama o método para renderizar os filmes

  def handleSearch(self):																												# Método para fazer buscas nos filmes que já estão
    busca = self.searchE.get()																									# Recebe string para fazer busca
    self.searchE.delete("0", "end")
    filmes_busca = []																														# Cria lista
    self.onlyRefresh()																													# Chama método para atualizar lista de filmes
    
    for filme in self.tarefas:																										# Faz busca nos filmes
      if busca.lower() in filme['titulo'].lower():
        filmes_busca.append(filme)

    self.renderFilmes(filmes_busca)																							# Chama método para renderizar filmes que batem com a busca

  def renderFilmes(self, tarefas):																								# Método para renderizar tarefas na tela
    for i in self.tree.get_children():																					# Apaga todos os tarefas já na tela
      self.tree.delete(i)
    
    for col in self.titulos_treeview:																						# Monta cabeçario da treeview
      self.tree.heading(col, text=col.title())

    for tarefa in tarefas:																												# Percorre tarefas e inseri na treeview
      item = (tarefa['id'], tarefa['descricao'], tarefa['data'])
      self.tree.insert('', 'end', values=item)
    
    self.tree.pack(side="top", fill='x')																				# Posiciona a treeview na tela preenchendo 
    self.tree.bind("<Double-1>", self.OnDoubleClick)														# Espera evento de click

  def handleCadastroFilme(self):																								# Método que envia requisição para o cadastro de um filme
    titulo = self.entryTitulo.get()																							# Pega os dados do input
    atores = self.entryAtores.get()
    diretores = self.entryDiretores.get()
    roteiristas = self.entryRoteiristas.get()
    self.entryAtores.delete("0","end")
    self.entryDiretores.delete("0","end")
    self.entryRoteiristas.delete("0","end")

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
      
      if(response["response"]["return"]):																									# Caso a resposta seja true
        self.changeMSG("Cadastrado com sucesso","green","subscribe")						# Mostra mensagem de sucesso com cor verde
        self.entryTitulo.delete("0","end")
      else:																																			# Caso a resposta seja false
        self.changeMSG(response["response"]["msg"],"red","subscribe")									# Mostra mensagem de erro com cor azul

  def changeMSG(self,texto,color,screem):																							# Método para mudar a mensagem
    self.lblres.destroy()																												# Destroi a antiga mensagem
    
    if screem == "subscribe":
      self.lblres= Label(self.subscribeMovieScreem, text=texto,										# Cria novo label com o texto e cor de fundo passada
                          bg='{}'.format(color))
    elif screem == "login":
      self.lblres= Label(self.SigninScreem, text=texto,bg='{}'.format(color))
    
    elif screem == "signup":
      self.lblres= Label(self.SignupScreem, text=texto,bg='{}'.format(color))

    elif screem == "hate":
      self.lblres= Label(self.avaliacaoFrame, text=texto,bg='{}'.format(color))

    self.lblres.pack(pady=5, side="bottom")																			# Posiciona na parte de baixo da janela com espaçamento vertical

  def processaSair(self):																												# Método para destruir janela do cliente
    self.destroy()

if __name__ == "__main__":
  i = Interface(None)
  i.mainloop()