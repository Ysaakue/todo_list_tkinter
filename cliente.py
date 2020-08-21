from tkinter import Tk, Button, PhotoImage, Label, Menu, Entry, Frame, Scrollbar, ttk
from banco import Banco
class Interface(Tk):
  def __init__(self,parent):
    Tk.__init__(self,parent)
    self.parent = parent
    
    self.attributes('-fullscreen',True)
    self.currentScreem = ""
    self.titulos_treeview = ["Id", "Descricao", "Data"]

    self.menu()
    self.Home()

  def menu(self):
    topo = self.winfo_toplevel()
    self.menuBar = Menu(topo)

    mnuOpcoes = Menu(self.menuBar, tearoff=0)
    mnuOpcoes.add_command(label="Sair", command=self.processaSair)
    self.menuBar.add_cascade(label="Opções", menu=mnuOpcoes)

    topo.config(menu=self.menuBar)																							# Posiciona o menu no topo da janela
    
  def toobar(self,screem):
    self.toobarFrame = Frame(self)
    self.toobarFrame.pack(side="top",pady=5,fill="x")
    
    # Button de home
    self.homeB=Button(self.toobarFrame,justify = "left", command=self.Home)
    self.photoHome=PhotoImage(file="img/home.png")
    self.homeB.config(image=self.photoHome,width="20",height="20")
    self.homeB.pack(side="left", padx=5)
    if screem == "home":
      self.homeB.config(state="disabled")
    
    # Button de recarregar
    self.refreshB=Button(self.toobarFrame,justify = "left",command=self.handleRefresh)
    self.photoRefresh=PhotoImage(file="img/refresh.png")
    self.refreshB.config(image=self.photoRefresh,width="20",height="20")
    self.refreshB.pack(side="left")
    if screem != "home":
      self.refreshB.config(state="disabled")

    # Entry de busca
    self.searchE = Entry(self.toobarFrame)
    self.searchE.pack(side="left",padx=5)
    self.searchE.bind("<Return>",lambda x: self.handleSearch())
    if screem != "home":
      self.searchE.config(state="disabled")

    # Button de busca
    self.searchB=Button(self.toobarFrame,justify = "left",command=self.handleSearch)
    self.photoSearch=PhotoImage(file="img/search.png")
    self.searchB.config(image=self.photoSearch,width="20",height="20")
    self.searchB.pack(side="left")
    if screem != "home":
      self.searchB.config(state="disabled")

    self.addB=Button(self.toobarFrame,justify = "left",command=self.Formulario)
    self.photoAdd=PhotoImage(file="img/add.png")
    self.addB.config(image=self.photoAdd,width="20",height="20")
    self.addB.pack(side="left", padx=5)
    if screem == "formulario":
      self.addB.config(state="disabled")
    
  def Home(self):
    if self.currentScreem == "formulario":
      self.toobarFrame.pack_forget()
      self.telaFormulario.pack_forget()
    
    self.toobar("home")
    
    self.telaHome = Frame(None)
    self.telaHome.pack(fill="both")

    self.tree = ttk.Treeview(	self.telaHome,columns=self.titulos_treeview,show="headings")
    self.scbar = Scrollbar(self.telaHome,orient="vertical",command=self.tree.yview)
    self.tree.configure(yscrollcommand=self.scbar.set)
    
    self.scbar.pack(side="right", fill="y")
    self.tree.pack(side="top", fill='both')

    self.handleRefresh()

    self.currentScreem = "home"

  def Formulario(self,tarefa=[]):
    self.toobarFrame.pack_forget()
    self.telaHome.pack_forget()
    self.toobar("formulario")

    self.telaFormulario = Frame(None)
    self.telaFormulario.pack()

    self.btnAcao = Button(	self.telaFormulario,text="Cadastrar",command=self.cadastroTarefa)
    descricao = ""
    data = ""
    if tarefa != []:
      self.btnAcao = Button(	self.telaFormulario,text="Atualizar",command=self.cadastroTarefa)
      descricao = tarefa[1]
      data = tarefa[2]

    self.lblDescricao = Label(self.telaFormulario, text="Descrição")
    self.lblDescricao.pack()
    self.entryDescricao = Entry(self.telaFormulario)
    self.entryDescricao.insert(0,descricao)
    self.entryDescricao.pack()

    self.lblData= Label(self.telaFormulario,text="Data")
    self.lblData.pack()
    self.entryData = Entry(self.telaFormulario)
    self.entryData.insert(0,data)
    self.entryData.pack()
    
    if tarefa != []:
      self.tarefa_id = tarefa[0]
      self.btnAcao = Button(	self.telaFormulario,text="Atualizar",command=self.atualizarTarefa)
      self.btnExcluir = Button(	self.telaFormulario,text="Excluir",command=self.excluirTarefa)
      self.btnExcluir.pack(pady=10,side="bottom")
    self.btnAcao.pack(pady=10,side="bottom")


    self.lblres= Label(self.telaFormulario, text="")
    self.lblres.pack()

    self.currentScreem = "formulario"
    
  def OnDoubleClick(self, event):																								# Método para identificar item clicado na lista
    item = self.tree.selection()																								# Identifica item clicado
    for i in item:
      self.Formulario(self.tree.item(i, "values"))																	# Chama método para mostrar os dados do filme

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
      print("Busca sem filtro feita com sucesso!")
    except:
      print("Ocorreu um erro na busca do usuário")
    
  def handleRefresh(self):																											# Método para receber os filmes do servidor e renderizar na tela
    self.onlyRefresh()																													# Chama método para atualizar os filmes
    self.mostrarTarefas(self.tarefas)																							# Chama o método para renderizar os filmes

  def handleSearch(self):
    busca = self.searchE.get()
    self.searchE.delete("0", "end")
    filmes_busca = []
    banco = Banco()
    try:
      c = banco.conexao.cursor()
      query = "select * from tarefas where id like '%{0}%' or descricao like '%{0}%' or data like '%{0}%';".format(busca)
      c.execute(query)
      for linha in c:
        obj = {}
        obj["id"] = linha[0]
        obj["descricao"] = linha[1]
        obj["data"] = linha[2]
        filmes_busca.append(obj)
      c.close()
      print("Busca com filtro feita com sucesso!")
    except:
      print("Ocorreu um erro na busca do usuário")

    self.mostrarTarefas(filmes_busca)

  def mostrarTarefas(self, tarefas):																								# Método para renderizar tarefas na tela
    for i in self.tree.get_children():																					# Apaga todos os tarefas já na tela
      self.tree.delete(i)
    
    for col in self.titulos_treeview:																						# Monta cabeçario da treeview
      self.tree.heading(col, text=col.title())

    for tarefa in tarefas:																												# Percorre tarefas e inseri na treeview
      item = (tarefa['id'], tarefa['descricao'], tarefa['data'])
      self.tree.insert('', 'end', values=item)
    
    self.tree.pack(side="top", fill='both')																				# Posiciona a treeview na tela preenchendo 
    self.tree.bind("<Double-1>", self.OnDoubleClick)														# Espera evento de click

  def cadastroTarefa(self):																								# Método que envia requisição para o cadastro de um filme
    descricao = self.entryDescricao.get()																							# Pega os dados do input
    data = self.entryData.get()

    if len(descricao)<1 or len(data)<1:
      self.changeMSG("Todos os campos devem ser preenchidos",'red')
    else:
      banco = Banco()
      try:
        c = banco.conexao.cursor()
        query = "insert into tarefas (descricao,data) values ('{0}','{1}');".format(descricao,data)
        c.execute(query)
        banco.conexao.commit()
        if c.lastrowid > 0:
          self.changeMSG("Tarefa cadastrado com sucesso","green")
          self.entryDescricao.delete("0","end")
          self.entryData.delete("0","end")
          print("sucesso")
        else:
          print("erro")
          self.changeMSG("Ocorreu um erro no cadastro da tarefa","red")
        c.close()
      except:
        print("exceção")
        self.changeMSG("Ocorreu um erro no cadastro da tarefa","red")
  
  def atualizarTarefa(self):
    descricao = self.entryDescricao.get()
    data = self.entryData.get()

    if len(descricao)<1 or len(data)<1:
      self.changeMSG("Todos os campos devem ser preenchidos",'red')
    else:
      banco = Banco()
      try:
        c = banco.conexao.cursor()
        query = "update tarefas set descricao = '{0}',data = '{1}' where id = {2};".format(descricao,data,self.tarefa_id)
        c.execute(query)
        banco.conexao.commit()
        self.changeMSG("Tarefa atualizada com sucesso","green")
        self.entryDescricao.delete("0","end")
        self.entryData.delete("0","end")
        print("sucesso")
        c.close()
      except:
        print("exceção")
        self.changeMSG("Ocorreu um erro no cadastro da tarefa","red")
    self.tarefa_id = 0

  def excluirTarefa(self):
    banco = Banco()
    try:
      c = banco.conexao.cursor()
      query = "delete from tarefas where id ={0};".format(self.tarefa_id)
      c.execute(query)
      banco.conexao.commit()
      self.changeMSG("Tarefa excluida com sucesso","green")
      self.entryDescricao.delete("0","end")
      self.entryData.delete("0","end")
      print("sucesso")
      c.close()
    except:
      print("exceção")
      self.changeMSG("Ocorreu um erro no cadastro da tarefa","red")
    self.tarefa_id = 0

  def changeMSG(self,texto,color):																							# Método para mudar a mensagem
    self.lblres.destroy()																												# Destroi a antiga mensagem
    
    self.lblres= Label(self.telaFormulario, text=texto,bg='{}'.format(color))

    self.lblres.pack(pady=5, side="bottom")																			# Posiciona na parte de baixo da janela com espaçamento vertical

  def processaSair(self):																												# Método para destruir janela do cliente
    self.destroy()

if __name__ == "__main__":
  i = Interface(None)
  i.mainloop()