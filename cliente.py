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
    self.searchB=Button(self.toobarFrame,justify = "left",command=self.handleSearch)
    self.photoSearch=PhotoImage(file="img/search.png")													# Cria uma imagem com referencia a um Search Icon
    self.searchB.config(image=self.photoSearch,width="20",height="20")					# Associa a imagem ao botão
    self.searchB.pack(side="left")																							# Posiciona o botão ao lado esquerdo do Frame
    if screem != "home":
      self.searchB.config(state="disabled")

    self.addB=Button(self.toobarFrame,justify = "left",command=self.SubscribeMovie)
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
      self.formulario.pack_forget()																		# Apaga tela de cadastro de filmes
    elif self.currentScreem == "signUp":																				# Verifica de estava na tela de login
      self.toobarFrame.pack_forget()																						# Apaga barra de ferramentas da tela inicial
      self.SignupScreem.pack_forget()																						# Apaga tela de login

    self.toobar("home")																													# Cria barra de ferramentas para home
    
    self.homeScreem = Frame(None)																								# Cria frame para tela de login
    self.homeScreem.pack(fill="both")

    self.tree = ttk.Treeview(	self.homeScreem,columns=self.titulos_treeview,show="headings")
    self.scbar = Scrollbar(self.homeScreem,orient="vertical",command=self.tree.yview)
    self.tree.configure(yscrollcommand=self.scbar.set)													# Configura para TreeView usar a ScrollBar
    
    self.scbar.pack(side="right", fill="y")																			# Posiciona ScrollBar no lado direito para preencher a altura
    self.tree.pack(side="top", fill='x')																				# Posiciona a lista no top preenchendo lateralmente
    
    self.handleRefresh()																												# Recarrega para renderizar a lista de filmes

    self.infoFrame = Frame(self.homeScreem)
    self.infoFrame.pack()

    self.currentScreem = "home"																									# Define que a tela atual é a home, por conta de referencia

  def SubscribeMovie(self,tarefa=[]):
    botao = "Cadastrar"
    descricao = ""
    data = ""
    if tarefa != []:
      botao = "Atualizar"
      descricao = tarefa[1]
      data = tarefa[2]
    
    self.toobarFrame.pack_forget()
    self.homeScreem.pack_forget()
    self.toobar("subscribe")

    self.formulario = Frame(None)
    self.formulario.pack()

    self.lblDescricao = Label(self.formulario, text="Descrição")
    self.lblDescricao.pack()
    self.entryDescricao = Entry(self.formulario)
    self.entryDescricao.insert(0,descricao)
    self.entryDescricao.pack()

    self.lblData= Label(self.formulario,text="Data")
    self.lblData.pack()
    self.entryData = Entry(self.formulario)
    self.entryData.insert(0,data)
    self.entryData.pack()
    
    self.btnCadastrar = Button(	self.formulario,text=botao,command=self.handleCadastroFilme)
    self.btnCadastrar.pack(pady=10,side="bottom")

    self.lblres= Label(self.formulario, text="")
    self.lblres.pack()

    self.currentScreem = "subscribeMovie"
    
  def OnDoubleClick(self, event):																								# Método para identificar item clicado na lista
    item = self.tree.selection()																								# Identifica item clicado
    for i in item:
      self.SubscribeMovie(self.tree.item(i, "values"))																	# Chama método para mostrar os dados do filme

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
    self.mostrarTarefas(self.tarefas)																							# Chama o método para renderizar os filmes

  def handleSearch(self):																												# Método para fazer buscas nos filmes que já estão
    busca = self.searchE.get()																									# Recebe string para fazer busca
    self.searchE.delete("0", "end")
    filmes_busca = []																														# Cria lista
    self.onlyRefresh()																													# Chama método para atualizar lista de filmes
    
    for filme in self.tarefas:																										# Faz busca nos filmes
      if busca.lower() in filme['titulo'].lower():
        filmes_busca.append(filme)

    self.mostrarTarefas(filmes_busca)																							# Chama método para renderizar filmes que batem com a busca

  def mostrarTarefas(self, tarefas):																								# Método para renderizar tarefas na tela
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
    titulo = self.entryDescricao.get()																							# Pega os dados do input
    atores = self.entryData.get()
    diretores = self.entryDiretores.get()
    roteiristas = self.entryRoteiristas.get()
    self.entryData.delete("0","end")
    self.entryDiretores.delete("0","end")
    self.entryRoteiristas.delete("0","end")

    if len(titulo)<1 or len(atores)<1 or len(diretores)<1 or len(roteiristas)<1:# Caso todos os inputs estejam vazios
      self.changeMSG("Todos os campos devem ser preenchidos",'red',"subscribe")	# Mostra mensagem de erro com cor vermelha
    
    else:
      response = {}
      if(response["response"]["return"]):																									# Caso a resposta seja true
        self.changeMSG("Cadastrado com sucesso","green","subscribe")						# Mostra mensagem de sucesso com cor verde
        self.entryDescricao.delete("0","end")
      else:																																			# Caso a resposta seja false
        self.changeMSG(response["response"]["msg"],"red","subscribe")									# Mostra mensagem de erro com cor azul

  def changeMSG(self,texto,color,screem):																							# Método para mudar a mensagem
    self.lblres.destroy()																												# Destroi a antiga mensagem
    
    if screem == "subscribe":
      self.lblres= Label(self.formulario, text=texto,bg='{}'.format(color))
    
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