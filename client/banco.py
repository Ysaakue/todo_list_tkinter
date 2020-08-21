#importando módulo do SQlite
import sqlite3

class Banco():
  def __init__(self):
    self.conexao = sqlite3.connect(r"/home/isaac/projetos/terceiros/sofia/tkinter/client/teste_database.sqlite")
    self.createTable()

  def createTable(self):
    c = self.conexao.cursor()
    c.execute("""create table if not exists tarefas (
                id integer primary key autoincrement ,
                descricao text,
                data datetime
                )""")
    self.conexao.commit()
    c.close()