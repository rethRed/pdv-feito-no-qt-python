from concurrent.futures import thread
from email.charset import QP
from logging import exception
from operator import itemgetter
from pydoc import visiblename
from re import S
from turtle import update
from typing import Container
from PyQt5.QtCore import QTextDecoder,QRect
from PyQt5.QtWidgets import QComboBox, QGridLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from Core.vendas.tela_vendas import produto
from Core.Admin.Caixa.cupom_recibo import Recibo
from load import *


def abrir_tela_marcas():
    Tela_Marca("tela_admin.lineEdit_marca","CadastrarProdutos.marca")
  

def remover_marca():
    tela_admin.lineEdit_marca.setText("NULL")
    CadastrarProdutos.marca = None

class MudarNomeMarca:
    def __init__(self,cur_name,fuc_after = None):

        mudar_nome_marca.closeEvent = MudarNomeMarca.close
        mudar_nome_marca.pushButton.clicked.connect(self.setar_novo_nome)

        self.fuc_after = fuc_after
        self.cur_name = cur_name
        mudar_nome_marca.exec()

    def setar_novo_nome(self):
        marca = mudar_nome_marca.lineEdit.text().upper().rstrip().lstrip()
        if marca == "":
            return

        if marca == "NULL":
            return
        try:
            cursor.execute(f"update Marca set MARCA = '{marca}' where MARCA = '{self.cur_name}'")
            banco.commit()

        except sqlite3.IntegrityError:
            #checar se existe uma marca igual no dataBase
            msg = QMessageBox()
            msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
            msg.setText(f''' Nome da Marca Inserido Já exististente.''')
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Marca Já existente")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)
            msg = msg.exec_()
            
            mudar_nome_marca.lineEdit.clear()
            return

        if self.fuc_after != None:
            self.fuc_after()

        mudar_nome_marca.close()

    @classmethod
    def close(cls,event):
        mudar_nome_marca.lineEdit.clear()


class Tela_Marca:

    mudar = None
    setar = None

    def __init__(self, mudar = None, setar = None):

        Tela_Marca.mudar = mudar
        Tela_Marca.setar = setar

        tela_add_marcas.lineEdit.clear()
        Tela_Marca.pesquisar_marcas()

        tela_add_marcas.show()


    @classmethod
    def escolher_marca(cls):

        index = tela_add_marcas.listWidget.currentRow()
        
        if index == -1:
            print("invalid")
            return

        if Tela_Marca.mudar != None:
            eval(f"{Tela_Marca.mudar}.setText('{tela_add_marcas.listWidget.currentItem().text()}')")
            
        if Tela_Marca.setar != None:
            exec(f"{Tela_Marca.setar} = '{tela_add_marcas.listWidget.currentItem().text()}'")

        tela_add_marcas.close()




    def text_changed_inserir_marca():

        if len(tela_add_marcas.lineEdit_cadastrar_marcas.text()) > 0:
            tela_add_marcas.label.clear()
    tela_add_marcas.lineEdit_cadastrar_marcas.textChanged.connect(text_changed_inserir_marca)


    def add_marcas_dataBase():

        marca = tela_add_marcas.lineEdit_cadastrar_marcas.text().upper().rstrip().lstrip()

        if marca == "":
            return

        if marca == "NULL":
            return
        try:
            cursor.execute("insert into Marca values (?)",(f"{marca}",))
            banco.commit()

        except sqlite3.IntegrityError:
            #checar se existe uma marca igual no dataBase
            tela_add_marcas.label.setStyleSheet("color: rgb(255, 0, 0);")
            tela_add_marcas.label.setText("Erro: Marca inserida ja cadastrado.")
            tela_add_marcas.lineEdit_cadastrar_marcas.clear()
            return

        tela_add_marcas.label.setStyleSheet("color: rgb(85, 255, 0);")
        tela_add_marcas.label.setText("Marca Cadastrada com sucesso!")
        tela_add_marcas.lineEdit_cadastrar_marcas.clear()


    def pesquisar_marcas():
        tela_add_marcas.label.clear()
        tela_add_marcas.listWidget.clear()
        marca = tela_add_marcas.lineEdit.text()
        cursor.execute(f"select MARCA from Marca where MARCA like '%{marca}%';")
        lista = cursor.fetchall()

        for i in range(len(lista)):
            tela_add_marcas.listWidget.addItem(str(lista[i][0]))




    def deletar_marca():
        msg = QMessageBox(visualizar_grade)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255); QDialog{border:1px solid;} QDialog::title{font-weight: bold;}')
        msg.setText(f''' Todos os Produtos que ultilizam esta marca terão suas marcas removidas. ''')
        msg.setWindowTitle("Deseja excluir a marca?")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)  
        msg = msg.exec_()

        if msg == QMessageBox.Yes:
            print("yes")
            pass
        elif msg == QMessageBox.No:
            print("no")
            return
            
        marca = tela_add_marcas.lineEdit.text()
        index = tela_add_marcas.listWidget.currentRow()

        if index == -1:
            return

        cursor.execute(f"select MARCA from Marca where MARCA like '%{marca}%';")
        mar = cursor.fetchall()[index][0]
        cursor.execute(f"delete from MARCA where Marca =?",(f"{mar}",))

        banco.commit()
        if tela_admin.lineEdit_marca.text() == mar:
            tela_admin.lineEdit_marca.setText("NULL")
            CadastrarProdutos.marca = None
        Tela_Marca.pesquisar_marcas()







def open_choose_exportar():
    Tela_exportar.show()
    url = fr"{c}\\DataBase\\produtos.db"
    Tela_exportar.lineEdit_2.setText(url)


def escolher_folder():
    fileName = QtWidgets.QFileDialog.getExistingDirectory(Tela_exportar, 'Desktop')
    Tela_exportar.lineEdit.setText(f"{fileName}")

def exportar():
    original = Tela_exportar.lineEdit_2.text()
    target = Tela_exportar.lineEdit.text()
    shutil.copy2(original,target)
    Tela_exportar.close()

def criar_caracteristica():
    if tela_admin.lineEdit_caracteristicas.text().rstrip().lstrip().upper() == "NULL":
        return
    grade = Grade()


def remover_caracteristica():
    current_row = tela_admin.listWidget_caracteristicas.currentRow()
    
    #controle

    if current_row == -1:
        return


    #deleta a instancia da grade

    del Grade.lis[current_row]

    #"reimprime" as caracteristicas na tableWidget

    Grade.add_tableList_caracteristica()


def remover_variacao():
    current_row = tela_admin.listWidget_caracteristicas.currentRow()
    
    if tela_admin.listWidget_variacoes.currentRow() == -1:
        return
  
    Grade.lis[current_row].variacoes.pop(tela_admin.listWidget_variacoes.currentRow())

    Grade.add_tableList_variacoes(current_row)



#criando classe para adicionar grades


class Grade:

    lis = []
    Nome_Grade = ""

    def __init__(self):

        if len(Grade.lis) > 1:
            tela_admin.label_menssa_grade.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssa_grade.setText("Numero maximo de caracteristica atingido!")
            return


        self.nome_caracteristica = tela_admin.lineEdit_caracteristicas.text().rstrip().lstrip().upper()

    
        self.variacoes = []
        

        if self.nome_caracteristica == "":
            tela_admin.label_menssa_grade.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssa_grade.setText("O nome da caracteristica não pode estar vazio!")
  
            return

        #armazenar a propria instancia em uma lista
        Grade.lis.append(self)

        #adicionar na tableWidget
        Grade.add_tableList_caracteristica()

        #limpar lineEdit
        tela_admin.lineEdit_caracteristicas.clear()
        tela_admin.lineEdit_caracteristicas.setFocus()

    def get_variacoes(self):
        return self.variacoes


    def insert_variacoes():
        current_row = tela_admin.listWidget_caracteristicas.currentRow()

        #controle
        if current_row == -1:
            tela_admin.label_menssa_grade.setStyleSheet("color: rgb(255, 85, 0);")
            tela_admin.label_menssa_grade.setText("Selecione uma característica!")
            return

        if tela_admin.lineEdit_variacoes.text() == "":
            tela_admin.label_menssa_grade.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssa_grade.setText("erro: O nome da variação não pode estar vazia.")
            return


        Grade.lis[current_row].variacoes.append(tela_admin.lineEdit_variacoes.text().rstrip().lstrip().upper())

        Grade.add_tableList_variacoes(current_row)

        tela_admin.lineEdit_variacoes.clear()


    def add_tableList_variacoes(current_row):

        items = Grade.lis[current_row].get_variacoes()

        tela_admin.listWidget_variacoes.clear()
        tela_admin.listWidget_variacoes.addItems(items)
        tela_admin.listWidget_variacoes.scrollToBottom()


    @classmethod

    def Row_chaged(cls):
        current_row = tela_admin.listWidget_caracteristicas.currentRow()

        if current_row == -1:
            tela_admin.listWidget_variacoes.clear()
            return
        Grade.add_tableList_variacoes(current_row)

    @classmethod
    def get_caracteristicas(cls):

        temp = []
        for i in range(len(Grade.lis)):
            temp.append(Grade.lis[i].nome_caracteristica)

        return temp


    @classmethod
    def add_tableList_caracteristica(cls):
        items = Grade.get_caracteristicas()

        tela_admin.listWidget_caracteristicas.clear()
        tela_admin.listWidget_caracteristicas.addItems(items)
        tela_admin.listWidget_caracteristicas.scrollToBottom()



    @classmethod
    def add_to_dataBase(cls):


        if len(Grade.lis) < 2:
            tela_admin.label_menssa_grade.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssa_grade.setText("Insira duas características!")
            return

        if len(Grade.lis) == 0:
            tela_admin.label_menssa_grade.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssa_grade.setText("erro: Grade sem atributos!")
            return


        for i in range(len(Grade.lis)):
            if len(Grade.lis[i].variacoes) == 0:
                tela_admin.label_menssa_grade.setStyleSheet("color: rgb(255, 0, 0);")
                tela_admin.label_menssa_grade.setText("erro: As variações não podem estar vazias!")
                return

        try:
            nome_da_grade = tela_admin.lineEdit_nome_grade.text().rstrip().lstrip()
            id_grade = randint(100000000,999999999)

            if nome_da_grade == "":
                tela_admin.label_menssa_grade.setStyleSheet("color: rgb(255, 0, 0);")
                tela_admin.label_menssa_grade.setText("erro: O nome da grade não pode estar vazio!")
                return
            

            while True:
            
                cursor.execute(f"select * from Grade_de_Produtos where ID = {id_grade}")
                dados = cursor.fetchall()

                if len(dados) == 0:
                    break

                else:
                    id_grade = randint(100000000,99999999)


            cursor.execute("insert into Grade_de_Produtos values (?,?)",(id_grade,nome_da_grade))
        


            for i in range(len(Grade.lis)):

                id_caracteristica = randint(100000000,999999999)
                

                while True:
            
                    cursor.execute(f"select * from Caracteristicas where ID = {id_caracteristica}")
                    dados = cursor.fetchall()

                    if len(dados) == 0:
                        break

                    else:
                        id_caracteristica = randint(100000000,999999999)

                cursor.execute("insert into Caracteristicas values (?,?,?)",(id_grade,id_caracteristica,Grade.lis[i].nome_caracteristica))

                for j in range(len(Grade.lis[i].variacoes)):
                    id_variacoes = randint(100000000,999999999)

                    while True:

                        cursor.execute(f"select * from Variacoes where ID = {id_variacoes}")
                        dados = cursor.fetchall()

                        if len(dados) == 0:
                            break

                        else:
                            id_variacoes = randint(100000000,999999999)

                    cursor.execute("insert into Variacoes values (?,?,?)",(id_caracteristica,id_variacoes,Grade.lis[i].variacoes[j]))
            banco.commit()

            tela_admin.listWidget_caracteristicas.clear()
            tela_admin.lineEdit_variacoes.clear()
            tela_admin.lineEdit_caracteristicas.clear()
            tela_admin.lineEdit_variacoes.clear()
            tela_admin.lineEdit_nome_grade.clear()
            tela_admin.label_menssa_grade.setStyleSheet("color: rgb(0, 255, 0);")
            tela_admin.label_menssa_grade.setText("Grade adicionado com sucesso!!")
            Grade.lis.clear()
        except:
            tela_admin.label_menssa_grade.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssa_grade.setText("algo deu errado, tente novamente!")
         
            return





def only_float_preco_cadastrar():

    only_float = tela_admin.lineEdit_preco.text()
    try:
        if float(tela_admin.lineEdit_preco.text().replace(",",".")):
            pass
    except:
        text = tela_admin.lineEdit_preco.text()
        text1= text[:-1]
        text = tela_admin.lineEdit_preco.setText(f"{text1}")
        return


def only_int_quantidade_cadastro():
   
    try:
        if int(tela_admin.lineEdit_quantidade_cadastro.text()):
            pass
    except:
        text = tela_admin.lineEdit_quantidade_cadastro.text()
        text1= text[:-1]
        text = tela_admin.lineEdit_quantidade_cadastro.setText(f"{text1}")
        return


def code_no_only_int():
    tela_admin.label_menssagem_cadastrar.clear()


#########################################    CADASTRAR PRODUTOS   #############################################

def batest():
    tela_admin.tableWidget_cadastrar.setRowCount(10)
    cur_dir = os.getcwd()


    for i in range(10):
        btn = QPushButton("", tela_admin)
        btn.setStyleSheet("background-color:#34495e; border:None;")
       
        btn.setIcon(QtGui.QIcon(fr"{cur_dir}\imagem\red_trash.png"))
        btn.setIconSize(QtCore.QSize(30,39))
        btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn.setMaximumSize(50,70)
        btn.clicked.connect(ba)
        tela_admin.tableWidget_cadastrar.setCellWidget(i,0,btn)



def ba():
    button = tela_admin.sender()
    print(button)
    index = tela_admin.tableWidget_cadastrar.indexAt(button.pos())
    if index.isValid():
        print(index.row(), index.column())
    print(index)


def abrir_pesquisar_ncm():
    try:
        tex = tela_admin.lineEdit_ncm.text().replace(".","")
        if tex == "":
            return

        url = f"https://homologacao.focusnfe.com.br/v2/ncms/{tex}"


        token = "zc3CTMLn2Vmze0R3m8b6FQ8zj1Fo3osj"

        r = requests.get(url, auth=(token,""),timeout=7)

        pesquisar_ncm.textBrowser.setText(r.text)
        pesquisar_ncm.show()
    except:
        return


def abrir_tela_pesquisar_grade():
    escolher_grade.show()
    

def adicionar_itens():
    cadastrar = CadastrarProdutos()



lista_grade = []
caracteristica = []
variacao = []
variacao2 = []

def pesquisar_grade():
    global lista_grade
    user_input = escolher_grade.lineEdit.text()


    cursor.execute(f"select Descricao, ID from Grade_de_Produtos where Descricao like '%{user_input}%';")

    lista_grade = cursor.fetchall()
    
    escolher_grade.listWidget_pesquiasar_grade.clear()

    for i in range(len(lista_grade )):
        escolher_grade.listWidget_pesquiasar_grade.addItem(lista_grade [i][0])
      
    escolher_grade.listWidget_pesquiasar_grade.scrollToBottom()



def setar_variacoes():

    global lista_grade  
    global caracteristica
    global variacao
    global variacao2
    tela_admin.comboBox_variacao.clear()
    tela_admin.comboBox_variacao_2.clear()

    

    try:
        
        cursor.execute(f"select ID, Variacao from Variacoes where ID_Caracteristica = {caracteristica[0][0]}")
        variacao = cursor.fetchall()
        variacao = sorted(variacao, key=itemgetter(1))


        for i in range(len(variacao)):
            tela_admin.comboBox_variacao.addItem(variacao[i][1])
            
        cursor.execute(f"select ID, Variacao from Variacoes where ID_Caracteristica = {caracteristica[1][0]}")
        variacao2 = cursor.fetchall()
        variacao2 = sorted(variacao2, key=itemgetter(1))

        for i in range(len(variacao2)):
            tela_admin.comboBox_variacao_2.addItem(variacao2[i][1])
    except:
        return
    
 


def Trocar_grade_no():
    confirmar_trocar_grade.close()


def Trocar_grade_sim():
    confirmar_trocar_grade.close()
    CadastrarProdutos.resetar_cadastro()
    selecionar_grade()


def selecionar_grade():
    global lista_grade
    global caracteristica
    global variacao
    global variacao2

    if len(CadastrarProdutos.lis) > 0:
        confirmar_trocar_grade.show()
        return 

    nome_grade = escolher_grade.listWidget_pesquiasar_grade.currentItem().text()
    index = escolher_grade.listWidget_pesquiasar_grade.currentRow()

    codigo_grade = lista_grade[index][1]

    tela_admin.comboBox_grade.clear()
    tela_admin.comboBox_grade.addItem(nome_grade)

    tela_admin.comboBox_variacao.clear()
    tela_admin.comboBox_caracteristica.clear()

    tela_admin.comboBox_variacao_2.clear()
    tela_admin.comboBox_caracteristica_2.clear()


    CadastrarProdutos.setar_grade(nome_grade,codigo_grade)

    

    cursor.execute(f"select ID, Descricao from Caracteristicas where ID_Grade = {codigo_grade}")

    caracteristica = cursor.fetchall()


    setar_variacoes()



    
    tela_admin.comboBox_caracteristica.addItem(caracteristica[0][1])
    tela_admin.comboBox_caracteristica_2.addItem(caracteristica[1][1])
  


    escolher_grade.close()



class CadastrarProdutos():

    lis= []
    nome_grade = ""
    codigo_grade = ""
    qtd_produtos = "000"
    qtd_produtos_total = "000"
    marca = None

    def __init__(self):
        
        global lista_grade
        global caracteristica
        global variacao 
        global variacao2

        tela_admin.label_menssagem_cadastrar.clear()

        self.codigo = tela_admin.lineEdit_codigo.text()

        if self.codigo == "":
            tela_admin.label_menssagem_cadastrar.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssagem_cadastrar.setText("Insira um Codigo!")
            tela_admin.lineEdit_codigo.setFocus()
            return

        for i in range(len(CadastrarProdutos.lis)):
            if self.codigo == CadastrarProdutos.lis[i].codigo:
                tela_admin.label_menssagem_cadastrar.setStyleSheet("color: rgb(255, 0, 0);")
                tela_admin.label_menssagem_cadastrar.setText("Codigo ja inserido!")
                tela_admin.lineEdit_codigo.clear()
                tela_admin.lineEdit_codigo.setFocus()
                return

        cursor.execute(f"select * from Codigo_Produtos where Codigo = '{self.codigo}'")    

        dado = cursor.fetchall()

        if len(dado) > 0:
            tela_admin.label_menssagem_cadastrar.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssagem_cadastrar.setText("Codigo ja cadastrado!")
            tela_admin.lineEdit_codigo.setFocus()
            return

        if CadastrarProdutos.codigo_grade == "":
            tela_admin.label_menssagem_cadastrar.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssagem_cadastrar.setText("Insira uma grade!")
            tela_admin.lineEdit_codigo.setFocus()
            return

        self.qtd = tela_admin.lineEdit_quantidade_cadastro.text().zfill(3) if tela_admin.lineEdit_quantidade_cadastro.text() != "" else "001"

        CadastrarProdutos.qtd_produtos_total = str(int(CadastrarProdutos.qtd_produtos_total ) + int(self.qtd)).zfill(3)

        tela_admin.label_qtd_produtos_total.setText(f"Quantidade Total: {CadastrarProdutos.qtd_produtos_total}")

       

        CadastrarProdutos.qtd_produtos = str(int(CadastrarProdutos.qtd_produtos) + 1).zfill(3)

        tela_admin.label_qtd_produtos.setText(f"Produtos: {CadastrarProdutos.qtd_produtos}")

        self.caracteristica_nome = caracteristica[0][1]
        self.caracteristica_id = caracteristica[0][0]

        self.caracteristica_nome2 = caracteristica[1][1]
        self.caracteristica_id2 = caracteristica[1][0]


        self.variacao_nome = variacao[tela_admin.comboBox_variacao.currentIndex()][1]
        self.variacao_id = variacao[tela_admin.comboBox_variacao.currentIndex()][0]


        self.variacao_nome2 = variacao2[tela_admin.comboBox_variacao_2.currentIndex()][1]
        self.variacao_id2 = variacao2[tela_admin.comboBox_variacao_2.currentIndex()][0]

        self.lista_caracteristica = caracteristica.copy()
        self.lista_variacao = variacao.copy()
        self.lista_variacao2 = variacao2.copy()
 
        # print(self.caracteristica_nome, self.caracteristica_id , self.variacao_nome,self.variacao_id)

        CadastrarProdutos.lis.append(self)


        self.inserir_tableWidget()

    


    def inserir_tableWidget(self,ap = "n"):

        tela_admin.label_menssagem_cadastrar.clear()
        cur_dir = os.getcwd()
        tela_admin.tableWidget_cadastrar.setRowCount(len(CadastrarProdutos.lis))
        tela_admin.tableWidget_cadastrar.setColumnCount(5)
        index = CadastrarProdutos.lis.index(CadastrarProdutos.lis[-1])
        

        btn = QPushButton("", tela_admin)
        btn.setStyleSheet("background-color:rgb(46,51,73); border:None;")
       
        btn.setIcon(QtGui.QIcon(fr"{cur_dir}\imagem\red_trash.png"))
        btn.setIconSize(QtCore.QSize(30,39))
        btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn.setMaximumSize(50,70)
        btn.clicked.connect(CadastrarProdutos.apagar_itens_tableWidget)
        tela_admin.tableWidget_cadastrar.setCellWidget(index,4,btn)

      
            
            

        container = QWidget()
        layout = QVBoxLayout(container)
        container.setStyleSheet("border:none;")

        container2 = QWidget()
        layout2 = QVBoxLayout(container2)
        container2.setStyleSheet("border:none;")

        container3 = QWidget()
        layout3 = QVBoxLayout(container3)
        container3.setStyleSheet("border:none;")


        container4 = QWidget()
        layout4 = QVBoxLayout(container4)
        container4.setStyleSheet("border:none;")


        lineEdit = QLineEdit("batata",tela_admin)
        lineEdit.setStyleSheet("border:1px solid;color: rgb(255, 255, 255);font: 75 14pt 'MS Shell Dlg 2';")
        lineEdit.setMaximumHeight(30)
        lineEdit.setMaxLength(30)
        layout.addWidget(lineEdit)
            


        lineEdit2 = QLineEdit("batata",tela_admin)
        lineEdit2.setStyleSheet("border:1px solid;color: rgb(255, 255, 255);font: 75 14pt 'MS Shell Dlg 2';")
        lineEdit2.setMaximumHeight(30)
        lineEdit2.setValidator(QIntValidator())
        lineEdit2.setMaxLength(4)
          
        layout2.addWidget(lineEdit2)
           
           
        combo = QComboBox(tela_admin)
        combo.setStyleSheet("background-color: rgb(255, 255, 255);font: 14pt 'MS Shell Dlg 2';color: rgb(0, 0, 0);")
        combo.setMaximumHeight(30)
        layout3.addWidget(combo)
        combo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        header = tela_admin.tableWidget_cadastrar.verticalHeader()
            
        header.setDefaultAlignment(Qt.AlignHCenter)

        combo2 = QComboBox(tela_admin)
        combo2.setStyleSheet("background-color: rgb(255, 255, 255);font: 14pt 1MS Shell Dlg 21;color: rgb(0, 0, 0);")
        combo2.setMaximumHeight(30)
        layout4.addWidget(combo2)
        combo2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        tela_admin.tableWidget_cadastrar.setCellWidget(index,0,container)
        tela_admin.tableWidget_cadastrar.setCellWidget(index,1,container2)

        tela_admin.tableWidget_cadastrar.setCellWidget(index,2,container3)
        tela_admin.tableWidget_cadastrar.setCellWidget(index,3,container4)


        tela_admin.tableWidget_cadastrar.cellWidget(index,0).layout().itemAt(0).widget().setText(f"{CadastrarProdutos.lis[index].codigo}")
        tela_admin.tableWidget_cadastrar.cellWidget(index,1).layout().itemAt(0).widget().setText(f"{ CadastrarProdutos.lis[index].qtd}")

          
               
        tela_admin.tableWidget_cadastrar.cellWidget(index,2).layout().itemAt(0).widget().addItem(f"{CadastrarProdutos.lis[index].caracteristica_nome}")
        tela_admin.tableWidget_cadastrar.cellWidget(index,2).layout().itemAt(0).widget().addItem(f"{CadastrarProdutos.lis[index].caracteristica_nome2}")
       

        tela_admin.tableWidget_cadastrar.cellWidget(index,3).layout().itemAt(0).widget().addItem(f"{CadastrarProdutos.lis[index].variacao_nome}")


        lineEdit2.textChanged.connect(CadastrarProdutos.user_setar_qtd)
        combo.currentIndexChanged.connect(CadastrarProdutos.mudar_carac_tableWidget)


        

        tela_admin.tableWidget_cadastrar.scrollToBottom()

        if ap == "n":
            tela_admin.lineEdit_codigo.clear()
            tela_admin.lineEdit_quantidade_cadastro.clear()
            tela_admin.lineEdit_codigo.setFocus()

           

    def apagar_itens_tableWidget(self):
        tela_admin.label_menssagem_cadastrar.clear()
        try:
            button = tela_admin.sender()
            index = tela_admin.tableWidget_cadastrar.indexAt(button.pos())
        except:
            return
        if index.isValid():
            
            CadastrarProdutos.qtd_produtos = str(int(CadastrarProdutos.qtd_produtos) - 1).zfill(3)

            tela_admin.label_qtd_produtos.setText(f"Produtos: {CadastrarProdutos.qtd_produtos}")

            tela_admin.tableWidget_cadastrar.cellWidget(index.row(),1).layout().itemAt(0).widget().text()

            CadastrarProdutos.qtd_produtos_total = str(int(CadastrarProdutos.qtd_produtos_total) - int(CadastrarProdutos.lis[index.row()].qtd)).zfill(3)
            tela_admin.label_qtd_produtos_total.setText(f"Quantidade Total: {CadastrarProdutos.qtd_produtos_total}")

            del CadastrarProdutos.lis[index.row()]

            tela_admin.tableWidget_cadastrar.removeRow(index.row())

  
    def user_setar_qtd(self):
        try:
            tela_admin.label_menssagem_cadastrar.clear()
            
            quantidade = tela_admin.tableWidget_cadastrar.focusWidget().text()
        
            if len(quantidade) > 3:
                if int(quantidade[0]) == 0:
                    quantidade = quantidade[1:] 

                else:
                    quantidade = quantidade[:-1]

            
            tela_admin.tableWidget_cadastrar.focusWidget().setText(f"{str(quantidade).zfill(3)}")

            foc = tela_admin.tableWidget_cadastrar.focusWidget().parentWidget()
            index = tela_admin.tableWidget_cadastrar.indexAt(foc.pos())
            
            qtd_atual = CadastrarProdutos.lis[index.row()].qtd

            #qtd_final = int(qtd_atual) - int(quantidade)



            CadastrarProdutos.qtd_produtos_total = str(int(CadastrarProdutos.qtd_produtos_total) - int(qtd_atual) ).zfill(3)
            CadastrarProdutos.qtd_produtos_total = str(int(CadastrarProdutos.qtd_produtos_total) + int(quantidade) ).zfill(3)

            CadastrarProdutos.lis[index.row()].qtd = str(quantidade).zfill(3)



            tela_admin.label_qtd_produtos_total.setText(f"Quantidade Total: {CadastrarProdutos.qtd_produtos_total}")

        except:
            return




    @classmethod
    def add_to_dataBase(cls):
        
        if len(CadastrarProdutos.lis) == 0:
            tela_admin.label_menssagem_cadastrar.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssagem_cadastrar.setText("erro: Adicione um produto!")
            return

        descricao_produto = tela_admin.lineEdit_descricao.text().rstrip().lstrip()
        if descricao_produto == "":
            tela_admin.label_menssagem_cadastrar.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssagem_cadastrar.setText("erro: Descrição não pode estar vazio!")
            return



        try:
            preco = format(float(tela_admin.lineEdit_preco.text().replace(",",".")),".2f") 
        except:

            tela_admin.label_menssagem_cadastrar.setStyleSheet("color: rgb(255, 0, 0);")
            tela_admin.label_menssagem_cadastrar.setText("erro: Preço não pode estar vazio!")
            return

        ncm = tela_admin.lineEdit_ncm.text().rstrip().lstrip().replace(".","")
        
        #só coloque esse if statement para esconder esse codigo 
        if True:
            icms_origem = fiscal_cadastro.comboBox_icms_origem.currentText()[0]
            unidade = fiscal_cadastro.lineEdit_unidade.text().upper()





        id_produto = randint(10000000,99999999)

        while True:
            
            cursor.execute(f"select * from Produtos where ID = {id_produto}")
            dados = cursor.fetchall()

            if len(dados) == 0:
                break

            else:
                id_produto = randint(10000000,99999999)

        v = "'"
        cursor.execute("insert into Produtos values (?,?,?,?,?,?,?)",(id_produto,descricao_produto,preco,str(CadastrarProdutos.qtd_produtos_total),str(CadastrarProdutos.qtd_produtos),CadastrarProdutos.marca,str(CadastrarProdutos.codigo_grade)))

        cursor.execute("insert into Fiscal_Produtos values(?,?,?,?,?)",(id_produto,id_produto,icms_origem,ncm,unidade))

        for i in range(len(CadastrarProdutos.lis)):
            id_codigo = randint(10000000,99999999)

            while True:
            
                cursor.execute(f"select * from Codigo_Produtos where ID = {id_codigo}")
                dados = cursor.fetchall()

                if len(dados) == 0:
                    break

                else:
                    id_codigo = randint(10000000,99999999)

            cursor.execute("insert into Codigo_Produtos values (?,?,?,?,?,?)",(CadastrarProdutos.lis[i].variacao_id,CadastrarProdutos.lis[i].variacao_id2,id_produto,id_codigo,CadastrarProdutos.lis[i].qtd,CadastrarProdutos.lis[i].codigo))
        
        banco.commit()

        tela_admin.label_menssagem_cadastrar.setStyleSheet("color: rgb(85, 255, 0);")
        tela_admin.label_menssagem_cadastrar.setText("Cadastrado com sucesso!")

        CadastrarProdutos.resetar_cadastro()

   
        # tela_admin.label_menssagem_cadastrar.setStyleSheet("color: rgb(255, 0, 0);")
        # tela_admin.label_menssagem_cadastrar.setText("algo deu errado!")

    @classmethod
    def mudar_carac_tableWidget(cls):
        
        
        foc = tela_admin.tableWidget_cadastrar.focusWidget().parentWidget()
        index = tela_admin.tableWidget_cadastrar.indexAt(foc.pos())
        

        tela_admin.tableWidget_cadastrar.cellWidget(index.row(),3).layout().itemAt(0).widget().clear()
        
        cur_index = tela_admin.tableWidget_cadastrar.cellWidget(index.row(),2).layout().itemAt(0).widget().currentIndex()


        if cur_index == 0:
            tela_admin.tableWidget_cadastrar.cellWidget(index.row(),3).layout().itemAt(0).widget().addItem(f"{CadastrarProdutos.lis[index.row()].variacao_nome}")

        elif cur_index == 1:
            tela_admin.tableWidget_cadastrar.cellWidget(index.row(),3).layout().itemAt(0).widget().addItem(f"{CadastrarProdutos.lis[index.row()].variacao_nome2}")


    @classmethod
    def resetar_cadastro(cls):
        CadastrarProdutos.lis.clear()
        CadastrarProdutos.qtd_produtos = "000"
        CadastrarProdutos.qtd_produtos_total = "000"

        tela_admin.tableWidget_cadastrar.clearContents()
        tela_admin.tableWidget_cadastrar.setRowCount(0)
        tela_admin.lineEdit_descricao.clear()
        tela_admin.lineEdit_preco.clear()
        tela_admin.lineEdit_ncm.clear()
        tela_admin.lineEdit_codigo.clear()
        tela_admin.lineEdit_quantidade_cadastro.clear()
        tela_admin.label_qtd_produtos.setText("Produtos: 000")
        tela_admin.label_qtd_produtos_total.setText("Quantidade Total: 000")






    @classmethod
    def setar_grade(cls,nome_grade,codigo_grade):

        CadastrarProdutos.nome_grade = nome_grade
        CadastrarProdutos.codigo_grade = codigo_grade





###################################################### visualizar os dados    ##########################################################






class NavegaDadosThread(QtCore.QThread):

    final = QtCore.pyqtSignal()

    update = QtCore.pyqtSignal()
    
    dados_pesquisar = ""
    pesquisar ="Nome"
    cur_data = []
    setar_nome_filtro = ""

    def __init__(self, parent = None, pesquisar = "n", dados_pesquisar=""):
        super(NavegaDadosThread,self).__init__(parent)
        self.pesquisar = pesquisar
        self.dados_pesquisar = dados_pesquisar
        


    def run(self):
 
        combo = tela_admin.comboBox.currentText()
         
        lista_opcoes = ["Produtos", "Grades"]

        if combo == "Produtos":
            
            if NavegaDadosThread.setar_nome_filtro == "sim":
                tela_admin.comboBox_2.clear()
                tela_admin.comboBox_2.addItems(["Nome","Preço","Codigo"])
                tela_admin.comboBox_2.setCurrentIndex(0)

            combo2 = tela_admin.comboBox_2.currentText()

            if combo2 == "Nome":
            
           
                cursor_tela_admim.execute(f"select ID, Nome , preco , qtd_produtos, qtd_itens from Produtos where Nome LIKE '%{tela_admin.lineEdit_pesquisar.text()}%'")

                setar_itens_TableWidget()
                self.final.emit()
                return
            elif combo2 == "Preço":
                
                cursor_tela_admim.execute(f"select ID, Nome , preco , qtd_produtos, qtd_itens from Produtos where preco LIKE '%{tela_admin.lineEdit_pesquisar.text()}%'")
                setar_itens_TableWidget()
                self.final.emit()
                return


            elif combo2 == "Codigo":

                cursor_tela_admim.execute(f"select ID_Produtos,Codigo, quantidade from Codigo_Produtos where Codigo LIKE '%{tela_admin.lineEdit_pesquisar.text()}%'")
                setar_itens_TableWidget()
                self.final.emit()
                return


        elif combo == "Grades":
            
            if NavegaDadosThread.setar_nome_filtro == "sim":
                tela_admin.comboBox_2.clear()
                tela_admin.comboBox_2.addItems(["Nome","ID"])
                tela_admin.comboBox_2.setCurrentIndex(0)

            combo2 = tela_admin.comboBox_2.currentText()

            if combo2 == "Nome":

                cursor_tela_admim.execute(f"select Descricao, ID from Grade_de_Produtos where Descricao LIKE '%{tela_admin.lineEdit_pesquisar.text()}%'")

                setar_itens_TableWidget()
                self.final.emit()
                return
        
            if combo2 == "ID":
                cursor_tela_admim.execute(f"select Descricao, ID from Grade_de_Produtos where ID LIKE '%{tela_admin.lineEdit_pesquisar.text()}%'")

                setar_itens_TableWidget()
                self.final.emit()
                return
            
            if lock.locked():
                lock.release()


            return
            if NavegaDadosThread.setar_nome_filtro == "sim":
                tela_admin.comboBox_2.clear()
                tela_admin.comboBox_2.addItems(["Nome"])



            cursor_tela_admim.execute("")


        
    def after_setar_dados():
      
        tela_admin.tableWidget_produtos.resizeColumnsToContents()
        
    



tela_admin.thread = NavegaDadosThread()
tela_admin.thread.final.connect(NavegaDadosThread.after_setar_dados)

def Pesquisar_itens_navegar_dados():
    
    tela_admin.lineEdit_pesquisar.clear()
    global thread_control
    list_thread = threading.enumerate()

    if len(list_thread) == 2:
        print("1")
        print(list_thread)
        return

    threadPesquisar = threading.Thread(target=Pesquisar_itens_navegar_dados_filtrado)

    threadPesquisar.daemon = True
    NavegaDadosThread.setar_nome_filtro = f"sim"
    threadPesquisar.start()


lock = threading.Lock()
thread_control = 0
def ban():

    list_thread = threading.enumerate()
    print("1")
    if len(list_thread) == 2:
        print("2")
        print(list_thread)
        print("2 thread")
        return

    threadPesquisar = threading.Thread(target=Pesquisar_itens_navegar_dados_filtrado)
    threadPesquisar.daemon = True
    NavegaDadosThread.setar_nome_filtro = f"não"
    threadPesquisar.start()
    print("no outro ali ",threading.enumerate())

def Pesquisar_itens_navegar_dados_filtrado():
    lock.acquire(True)

    tela_admin.tableWidget_produtos.setRowCount(0)
    while tela_admin.thread.isRunning():
        time.sleep(0.2)

    tela_admin.thread.start()
    tela_admin.thread.wait()
   
    


def setar_itens_TableWidget():
 

    combo = tela_admin.comboBox.currentText()


    if combo == "Produtos":
        combo2 = tela_admin.comboBox_2.currentText()

        
        if combo2 == "Codigo":
            needed = 60
            data = cursor_tela_admim.fetchmany(needed)
            
            data = [list(x) for x in data]

            if len(data) > 0:
              
                for i in range(len(data)):
                    temp = cursor.execute(f"select Nome, ID_Grade,preco From Produtos where ID = {data[i][0]}").fetchall()
                    data[i].append(temp[0][2])
                    data[i].append(temp[0][0])
                    temp = cursor.execute(f"select Descricao From Grade_de_Produtos where ID = {temp[0][1]}").fetchall()

                    data[i].append(temp[0][0])
        
            column = 4
            tela_admin.tableWidget_produtos.setColumnCount(column)
            
            column_name = ["Codigo", "Qtd","Preço","Descrição","Grade" ]
            

            tela_admin.tableWidget_produtos.setHorizontalHeaderLabels(column_name)

            rowCount = tela_admin.tableWidget_produtos.rowCount()
        
            try:
                for i in range(0, needed):
                    tela_admin.tableWidget_produtos.setRowCount(rowCount+i+1)
                    
                    for j in range(0, column):
                        tela_admin.tableWidget_produtos.setItem(rowCount+i, j, QTableWidgetItem(str(data[i][j+1])))
                if lock.locked():   
                    lock.release()
                tela_admin.thread.final.emit()


            

            except IndexError:
                tela_admin.tableWidget_produtos.setRowCount( tela_admin.tableWidget_produtos.rowCount() - 1)
                if lock.locked():   
                    lock.release()
                tela_admin.thread.final.emit()
                print("=====================")
                print("IndexError Because There is No Data to Get From Table")
                print("=====================")
                
                return
            return




        needed = 60

 
        data = cursor_tela_admim.fetchmany(needed)
        
       
            
        column = 4
        tela_admin.tableWidget_produtos.setColumnCount(column)
        
        column_name = ["Descrição", "Preço","Qtd.Produtos","Qtd.Itens" ]
        

        tela_admin.tableWidget_produtos.setHorizontalHeaderLabels(column_name)

        rowCount = tela_admin.tableWidget_produtos.rowCount()
     
        try:
            for i in range(0, needed):
                tela_admin.tableWidget_produtos.setRowCount(rowCount+i+1)
                for j in range(0, column):
                    tela_admin.tableWidget_produtos.setItem(rowCount+i, j, QTableWidgetItem(str(data[i][j+1])))
            if lock.locked():   
                lock.release()
            tela_admin.thread.final.emit()


        

        except IndexError:
            tela_admin.tableWidget_produtos.setRowCount( tela_admin.tableWidget_produtos.rowCount() - 1)
            if lock.locked():   
                lock.release()
            tela_admin.thread.final.emit()
            print("=====================")
            print("IndexError Because There is No Data to Get From Table")
            print("=====================")
            return



    if combo == "Grades":
        needed = 60
 
        data = cursor_tela_admim.fetchmany(needed)
        
            
        column = 2
        tela_admin.tableWidget_produtos.setColumnCount(column)
        
        column_name = ["Descrição", "ID"]
        

        tela_admin.tableWidget_produtos.setHorizontalHeaderLabels(column_name)

        rowCount = tela_admin.tableWidget_produtos.rowCount()
     
        try:
            for i in range(0, needed):
                tela_admin.tableWidget_produtos.setRowCount(rowCount+i+1)
                for j in range(0, column):
                    tela_admin.tableWidget_produtos.setItem(rowCount+i, j, QTableWidgetItem(str(data[i][j])))
            if lock.locked():   
                lock.release()
            tela_admin.thread.final.emit()

        

        except IndexError:
            tela_admin.tableWidget_produtos.setRowCount( tela_admin.tableWidget_produtos.rowCount() - 1)
            if lock.locked():   
                lock.release()
            tela_admin.thread.final.emit()
            print("=====================")
            print("IndexError Because There is No Data to Get From Table")
            print("=====================")
            return







def abrir_navegar_produto():
    combo = tela_admin.comboBox.currentText()

    if combo == "Produtos":
        
        tela_produtos.tableWidget_produto_pesquisar.clearContents()
        index = tela_admin.tableWidget_produtos.currentIndex()
        combo2 = tela_admin.comboBox_2.currentText()

        id_produtos = []

        if combo2 == "Nome":
            id_produtos = cursor.execute(f"select ID from Produtos where Nome LIKE '%{tela_admin.lineEdit_pesquisar.text()}%'").fetchall()[index.row()][0]
            
            
        elif combo2 == "Preço":
            
            id_produtos = cursor.execute(f"select ID from Produtos where preco LIKE '%{tela_admin.lineEdit_pesquisar.text()}%'").fetchall()[index.row()][0]

        
        elif combo2 == "Codigo":
            id_produtos = cursor.execute(f"select ID_Produtos from Codigo_Produtos where Codigo LIKE '%{tela_admin.lineEdit_pesquisar.text()}%'").fetchall()[index.row()][0]
            
        produtos_inf = cursor.execute(f"select Nome, preco, ID, qtd_produtos, qtd_itens, ID_Grade,Marca from Produtos where ID = {id_produtos}").fetchall()
        ncm = cursor.execute(f"select NCM from Fiscal_Produtos where ID = {id_produtos}").fetchall()[0][0]

        VisualizarProduto.marca = cursor.execute(f"select Marca from Produtos where ID = {id_produtos} ").fetchall()[0][0]

        if VisualizarProduto.marca == None:
            tela_produtos.lineEdit_marca.setText(f"NULL")
        else:
            tela_produtos.lineEdit_marca.setText(f"{VisualizarProduto.marca}")


        tela_produtos.lineEdit_produto_descricao.setText(str(produtos_inf[0][0]))
        tela_produtos.lineEdit_produto_preco.setText(str(produtos_inf[0][1]))
        tela_produtos.lineEdit_produto_ncm.setText(str(ncm))
        tela_produtos.label_produto_qtd_produtos.setText(f"Produtos: {str(produtos_inf[0][3]).zfill(3)}")
        tela_produtos.label_produto_qtd_itens.setText(f"Qtd. Itens Total: {str(produtos_inf[0][4]).zfill(3)}")

        cursor.execute(f"select * from Codigo_Produtos where ID_Produtos = {id_produtos}")

        produtos_codigo = cursor.fetchall()
        VisualizarProduto.ID_grade = str(produtos_inf[0][5])
        VisualizarProduto.qtd_produtos = str(produtos_inf[0][3]).zfill(3)
        VisualizarProduto.qtd_produtos_total = str(produtos_inf[0][4]).zfill(3)
        VisualizarProduto.ID_Produtos = str(id_produtos)

        for i in range(len(produtos_codigo)):
            visual = VisualizarProduto(produtos_codigo[i][0],produtos_codigo[i][1],produtos_codigo[i][2],produtos_codigo[i][3],produtos_codigo[i][4],produtos_codigo[i][5])

        tela_produtos.show()


    if combo == "Grades":

        index = tela_admin.tableWidget_produtos.currentIndex()
        combo2 = tela_admin.comboBox_2.currentText()
        
        id_produtos = []
        if combo2 == "Nome":
            id_grade = cursor.execute(f"select ID from Grade_de_Produtos where Descricao LIKE '%{tela_admin.lineEdit_pesquisar.text()}%'").fetchall()[index.row()][0]

        elif combo2 == "ID":
            id_grade = cursor.execute(f"select ID from Grade_de_Produtos where ID LIKE '%{tela_admin.lineEdit_pesquisar.text()}%'").fetchall()[index.row()][0]


        visualizar_grade.lineEdit_nome_grade.setText(cursor.execute(f"select Descricao from Grade_de_Produtos where ID = {id_grade}").fetchall()[0][0]) 
        GradeView.id_grade = id_grade
        GradeView.setar_itens()

        visualizar_grade.show()
            

class GradeView:
    id_grade = ""
    lis_caracteristica = []
    lis_variacao = []
    lis_variacao2 = []
    
    def __init__(self):
        pass

    @classmethod
    def alterar_variacao(cls,index = 99):
        if index == 99:
            index = visualizar_grade.listWidget_carc.currentRow()

        visualizar_grade.listWidget_varia.clear()


        if index == 0:
            for i in range(len( GradeView.lis_variacao)):
                visualizar_grade.listWidget_varia.addItem(f"{GradeView.lis_variacao[i][1]}")
            visualizar_grade.lineEdit_caracteristica.setText(f"{GradeView.lis_caracteristica[0][1]}")

        elif index == 1:

            for i in range(len(GradeView.lis_variacao2)):
                visualizar_grade.listWidget_varia.addItem(f"{GradeView.lis_variacao2[i][1]}")
            visualizar_grade.lineEdit_caracteristica.setText(f"{GradeView.lis_caracteristica[1][1]}")
    
        else:
            return
    

    def limpar_dados(event):
        GradeView.lis_caracteristica.clear()
        GradeView.lis_variacao.clear()
        GradeView.lis_variacao2.clear()
        visualizar_grade.listWidget_carc.clear()
        visualizar_grade.listWidget_varia.clear()
        visualizar_grade.lineEdit_nome_grade.clear()
        GradeView.id_grade = ""
        visualizar_grade.lineEdit_caracteristica.clear()



    @classmethod
    def setar_itens(cls):

        orden = '''
                        ORDER BY case Variacao when "P" then 0 
                        when "PP" then 2 
                        when "P" then 3 
                        when "M" then 4 
                        when "G" then 5 
                        when "GG" then 6 
                        when "XGG" then 7
                        when "G1" then 8 
                        when "G2" then 9 
                        when "G3" then 10 
                        ELSE variacao
                        end ASC'''

                        
        caracteristicas = cursor.execute(f"select ID, Descricao from Caracteristicas where id_grade = {GradeView.id_grade}").fetchall()

        visualizar_grade.listWidget_carc.clear()
        for i in range(len(caracteristicas)):
            temp = []
            for j in range(len(caracteristicas[i])):
                
                temp.append(caracteristicas[i][j])
            GradeView.lis_caracteristica.append(temp)
            visualizar_grade.listWidget_carc.addItem(str(caracteristicas[i][1]))


        variacao = cursor.execute(f"select ID,Variacao from Variacoes where ID_Caracteristica = {caracteristicas[0][0]} {orden}" ).fetchall()
        variacao2 = cursor.execute(f"select ID,Variacao from Variacoes where ID_Caracteristica = {caracteristicas[1][0]} {orden}").fetchall()

        for i in range(len(variacao)):
            temp = []
            for j in range(len(variacao[i])):
                
                temp.append(variacao[i][j])
            GradeView.lis_variacao.append(temp)

        for i in range(len(variacao2)):
            temp = []
            for j in range(len(variacao2[i])):
                
                temp.append(variacao2[i][j])
            GradeView.lis_variacao2.append(temp)


    @classmethod
    def adicionar_variacao(cls):

        index = visualizar_grade.listWidget_carc.currentRow()

        if index == -1:
            return
        variacao = visualizar_grade.lineEdit_variacao.text().upper().rstrip().lstrip()

        if variacao == "NULL":
            return

        if variacao == "":
            return

        if variacao[0] == "*":
            index_va = visualizar_grade.listWidget_varia.currentRow()
            visualizar_grade.lineEdit_variacao.clear()
            GradeView.trocar_nome(variacao[1:],GradeView.lis_variacao[index_va][1] if index == 0 else GradeView.lis_variacao2[index_va][1])
            return
        

        #verificar se existe um uma variacao com o mesmos nome
        nome_temp = cursor.execute(f"SELECT Variacao from Variacoes where ID_Caracteristica = {GradeView.lis_caracteristica[index][0]} and variacao = '{variacao}'").fetchall()
        if len(nome_temp) > 0 :
            visualizar_grade.lineEdit_variacao.clear()
            msg = QMessageBox(visualizar_grade)
            msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
            msg.setText(f''' ERRO: Nome Da Variação informada ja estar sendo ultilizada!''')
            msg.setIcon(QMessageBox. Warning)
            msg.setWindowTitle("ERRO")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)  
            msg = msg.exec_()
            return


        #gerar um id
        id = randint(100000000,999999999)
        dados = cursor.execute(f"SELECT Variacao from Variacoes where id = {id}")

        while True:

            if len(dados.fetchall()) < 1:
                break

            else:
                id = randint(100000000,999999999)
                dados = cursor.execute(f"SELECT Variacao from Variacoes where id = {id}")

        cursor.execute(f"insert into Variacoes values(?,?,?)", (GradeView.lis_caracteristica[index][0],id,variacao))
        banco.commit()

        GradeView.lis_caracteristica.clear()
        visualizar_grade.lineEdit_variacao.clear()
        GradeView.lis_variacao.clear()
        GradeView.lis_variacao2.clear()
        GradeView.setar_itens()
        GradeView.alterar_variacao(index)
        visualizar_grade.listWidget_carc.setCurrentRow(index)
        visualizar_grade.listWidget_varia.scrollToBottom()



    @classmethod
    def excluir_variacao(cls):
        index = visualizar_grade.listWidget_varia.currentRow()
        index_c = visualizar_grade.listWidget_carc.currentRow()

        if index == -1 or index_c == -1:
            return

        msg = QMessageBox(visualizar_grade)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255); QDialog{border:1px solid;} QDialog::title{font-weight: bold;}')
        msg.setText(f'''    Todos Os Produtos Que ultilizam ésta variação "{GradeView.lis_variacao[index][1] if index_c == 0 else GradeView.lis_variacao2[index][1]}"
    Terão suas variações INDEFINIDAS.

    Deseja Continuar Mesmo Assim?

    
        ''')



        msg.setWindowTitle("Deseja excluir ésta variação?")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)  
        msg = msg.exec_()

        if msg == QMessageBox.Yes:
            print("yes")
            pass
        elif msg == QMessageBox.No:
            print("no")
            return

        
        
       
        print(index)
    
        print(index_c)

        if index_c == 0:
   
            cursor.execute(f"delete from Variacoes  where ID = {GradeView.lis_variacao[index][0]};")

        elif index_c == 1:

            cursor.execute(f"delete from Variacoes  where ID = {GradeView.lis_variacao2[index][0]} ")

        else:
            return

        print("ANTES COMMIT")
        banco.commit()
        visualizar_grade.lineEdit_variacao.clear()
        GradeView.lis_variacao.clear()
        GradeView.lis_variacao2.clear()
        GradeView.setar_itens()
        GradeView.alterar_variacao(index_c)
        visualizar_grade.listWidget_carc.setCurrentRow(index_c)
        visualizar_grade.listWidget_varia.scrollToBottom()


    @classmethod
    def trocar_nome(cls,nome,nome_cur_variacao):

        index = visualizar_grade.listWidget_varia.currentRow()
        index_c = visualizar_grade.listWidget_carc.currentRow()

        if nome == "" or index == -1:
            return

        #verificar se exite outra variaçao com o mesmo nome na mesma caracteristica
        nome_temp = cursor.execute(f"SELECT Variacao from Variacoes where ID_Caracteristica = {GradeView.lis_caracteristica[index_c][0]} and variacao = '{nome}'").fetchall()
        if len(nome_temp) > 0 :
            print(nome_temp)
            msg = QMessageBox(visualizar_grade)
            msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
            msg.setText(f''' ERRO: Nome de variação escolhida ja estar sendo ultilizada.
            ''')


            msg.setIcon(QMessageBox. Warning)
            msg.setWindowTitle("Nome em ultilização.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)  
            msg = msg.exec_()
            return

        

        if nome == "" or index == -1:
            return

        
        msg = QMessageBox(visualizar_grade)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255); QDialog{border:1px solid;} QDialog::title{font-weight: bold;}')
        msg.setText(f''' Ao confimar, o nome da variação "{nome_cur_variacao}" 
        será trocado por "{nome}".
    
        ''')
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Deseja Trocar de Nome?")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)  
        msg = msg.exec_()

        if msg == QMessageBox.Yes:
            print("yes")
            pass
        elif msg == QMessageBox.No:
            print("no")
            return

        
        cursor.execute(f"update Variacoes set Variacao = '{nome}' where id = {GradeView.lis_variacao[index][0] if index_c == 0 else GradeView.lis_variacao2[index][0]}")

        banco.commit()
        visualizar_grade.lineEdit_variacao.clear()
        GradeView.lis_variacao.clear()
        GradeView.lis_variacao2.clear()
        GradeView.setar_itens()
        GradeView.alterar_variacao(index_c)
        visualizar_grade.listWidget_carc.setCurrentRow(index_c)
        visualizar_grade.listWidget_varia.scrollToBottom()


    @classmethod
    def trocar_nome_grade(cls):

        new_grade_name = visualizar_grade.lineEdit_nome_grade.text().lstrip().rstrip()

        if new_grade_name == "":
            return

        cursor.execute(f"update Grade_de_Produtos set Descricao = '{new_grade_name}' where id = {GradeView.id_grade}")

        banco.commit()
        
        

        msg = QMessageBox(visualizar_grade)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
        msg.setText(f''' Alterações salvas com sucesso!!
        ''')
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Sucesso.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)  
        msg = msg.exec_()

        ban()
    


    @classmethod
    def trocar_nome_carac(cls):
        item = visualizar_grade.lineEdit_caracteristica.text().lstrip().rstrip()
        index_c = visualizar_grade.listWidget_carc.currentRow()



        if index_c == -1 or item == "":
            return


        msg = QMessageBox(visualizar_grade)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255); ')
        msg.setText(f'''   Deseja Trocar o Nome Da Característica?
        ''')



        msg.setWindowTitle("Trocar Nome Da Característica.")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)  
        msg = msg.exec_()


        if msg == QMessageBox.Yes:
            print("yes")
            pass
        elif msg == QMessageBox.No:
            print("no")
            return

        if index_c == 0:

            cursor.execute(f"update Caracteristicas set Descricao = '{item}' where id = {GradeView.lis_caracteristica[0][0]}")
            banco.commit()

        elif index_c == 1:
            cursor.execute(f"update Caracteristicas set Descricao = '{item}' where id = {GradeView.lis_caracteristica[1][0]}")

            banco.commit()

        caracteristicas = cursor.execute(f"select ID, Descricao from Caracteristicas where id_grade = {GradeView.id_grade}").fetchall()
        GradeView.lis_caracteristica.clear()
        visualizar_grade.listWidget_carc.clear()
        visualizar_grade.listWidget_varia.clear()
        visualizar_grade.lineEdit_caracteristica.clear()
        for i in range(len(caracteristicas)):
            temp = []
            for j in range(len(caracteristicas[i])):
                
                temp.append(caracteristicas[i][j])
            GradeView.lis_caracteristica.append(temp)
            visualizar_grade.listWidget_carc.addItem(str(caracteristicas[i][1]))
        





####################################

def only_int_preco_pesquisar_produtos():
    tela_produtos.label_menssage_produto_ver.clear()
    try:
        if float(tela_produtos.lineEdit_produto_preco.text().replace(",",".")):
            pass
    except:
        text = tela_produtos.lineEdit_produto_preco.text()
        text1= text[:-1]
        text = tela_produtos.lineEdit_produto_preco.setText(f"{text1}")
        return

class VisualizarProduto:
    lis_del = []
    lis = []
    ID_grade = ""
    ID_Produtos = ""
    qtd_produtos = "000"
    qtd_produtos_total = "000"
    marca = None


    def __init__(self,ID_variacoes,ID_variacoes2,ID_Produtos,ID,quantidade,Codigo):
        tela_produtos.label_menssage_produto_ver.clear()
        self.ID_variacoes = ID_variacoes
        self.ID_variacoes2 = ID_variacoes2
        self.ID = ID
        self.quantidade = quantidade
        self.Codigo = Codigo


        
        #setar variacao e caracteristica 1 
        
        if self.ID_variacoes == None:
            self.variacao_nome = "NULL"
            self.caracteristica_nome = "NULL"

        else:
            cursor.execute(f"select Variacao from Variacoes where id = {self.ID_variacoes}")

            temp = cursor.fetchall()

            self.variacao_nome = temp[0][0]
            temp =  cursor.execute(f"select ID_Caracteristica from Variacoes where id = {ID_variacoes}").fetchall()

            temp = cursor.execute(f"select Descricao from Caracteristicas where ID = {temp[0][0]} ORDER BY Descricao ASC").fetchall()

            self.caracteristica_nome = temp[0][0]
            

        #setar variacao e caracteristica 1 
        if self.ID_variacoes2 == None:
            self.variacao_nome2 = "NULL"
            self.caracteristica_nome2 = "NULL"

        else:
            cursor.execute(f"select Variacao from Variacoes where id = {self.ID_variacoes2}")

            temp = cursor.fetchall()

            self.variacao_nome2 = temp[0][0]

            temp = cursor.execute(f"select ID_Caracteristica from Variacoes where id = {self.ID_variacoes2}").fetchall()

            temp = cursor.execute(f"select Descricao from Caracteristicas where ID = {temp[0][0]} ORDER BY Descricao ASC").fetchall()

            self.caracteristica_nome2 = temp[0][0]





        VisualizarProduto.lis.append(self)

        VisualizarProduto.inserir_tableWidget(self)



    def inserir_tableWidget(self,ap = "n"):

       
        cur_dir = os.getcwd()
        tela_produtos.tableWidget_produto_pesquisar.setRowCount(len(VisualizarProduto.lis))
        tela_produtos.tableWidget_produto_pesquisar.setColumnCount(5)
        index = VisualizarProduto.lis.index(VisualizarProduto.lis[-1])
        

        btn = QPushButton("", tela_produtos)
        btn.setStyleSheet("background-color:#34495e; border:None;")
       
        btn.setIcon(QtGui.QIcon(fr"{cur_dir}\imagem\red_trash.png"))
        btn.setIconSize(QtCore.QSize(30,39))
        btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn.setMaximumSize(50,70)
        btn.clicked.connect(VisualizarProduto.apagar_itens_tableWidget)
        tela_produtos.tableWidget_produto_pesquisar.setCellWidget(index,4,btn)

      
            
            

        container = QWidget()
        layout = QVBoxLayout(container)
        container.setStyleSheet("border:none;")

        container2 = QWidget()
        layout2 = QVBoxLayout(container2)
        container2.setStyleSheet("border:none;")

        container3 = QWidget()
        layout3 = QVBoxLayout(container3)
        container3.setStyleSheet("border:none;")


        container4 = QWidget()
        layout4 = QHBoxLayout(container4)
        container4.setStyleSheet("border:none;")


        lineEdit = QLineEdit("batata",tela_produtos)
        lineEdit.setStyleSheet("border:1px solid;color: rgb(255, 255, 255);font: 75 14pt 'MS Shell Dlg 2';")
        lineEdit.setMaximumHeight(30)
        lineEdit.setMaxLength(30)
        layout.addWidget(lineEdit)
            


        lineEdit2 = QLineEdit("batata",tela_produtos)
        lineEdit2.setStyleSheet("border:1px solid;color: rgb(255, 255, 255);font: 75 14pt 'MS Shell Dlg 2';")
        lineEdit2.setMaximumHeight(30)
        lineEdit2.setValidator(QIntValidator())
        lineEdit2.setMaxLength(10)
          
        layout2.addWidget(lineEdit2)
           
           
        combo = QComboBox(tela_produtos)
        combo.setStyleSheet("background-color: rgb(255, 255, 255);font: 14pt 'MS Shell Dlg 2';")
        combo.setMaximumHeight(30)
        layout3.addWidget(combo)
        combo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        header = tela_produtos.tableWidget_produto_pesquisar.verticalHeader()
            
        header.setDefaultAlignment(Qt.AlignHCenter)

        combo2 = QComboBox(tela_produtos)
        combo2.setStyleSheet("background-color: rgb(255, 255, 255);font: 14pt 1MS Shell Dlg 21;")
        combo2.setMaximumHeight(30)
        layout4.addWidget(combo2)
        combo2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


        toolButton = QToolButton(tela_produtos)
        toolButton.setStyleSheet("background-color: rgb(255, 255, 255);color:#000000;")
        toolButton.clicked.connect(VisualizarProduto.mudar_variacao)
        toolButton.setText("...")
        layout4.addWidget(toolButton)
        toolButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))




        tela_produtos.tableWidget_produto_pesquisar.setCellWidget(index,0,container)
        tela_produtos.tableWidget_produto_pesquisar.setCellWidget(index,1,container2)

        tela_produtos.tableWidget_produto_pesquisar.setCellWidget(index,2,container3)
        tela_produtos.tableWidget_produto_pesquisar.setCellWidget(index,3,container4)


        tela_produtos.tableWidget_produto_pesquisar.cellWidget(index,0).layout().itemAt(0).widget().setText(f"{self.Codigo}")
        tela_produtos.tableWidget_produto_pesquisar.cellWidget(index,1).layout().itemAt(0).widget().setText(f"{str(self.quantidade).zfill(3)}")

          


        
               
        tela_produtos.tableWidget_produto_pesquisar.cellWidget(index,2).layout().itemAt(0).widget().addItem(f"{self.caracteristica_nome}")
        tela_produtos.tableWidget_produto_pesquisar.cellWidget(index,2).layout().itemAt(0).widget().addItem(f"{self.caracteristica_nome2}")
       

        tela_produtos.tableWidget_produto_pesquisar.cellWidget(index,3).layout().itemAt(0).widget().addItem(f"{self.variacao_nome}")


        lineEdit2.textChanged.connect(VisualizarProduto.user_setar_qtd)
        combo.currentIndexChanged.connect(VisualizarProduto.mudar_carac_tableWidget)
        lineEdit.textChanged.connect(VisualizarProduto.setar_codigo)

        header = tela_produtos.tableWidget_produto_pesquisar.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        tela_produtos.tableWidget_produto_pesquisar.setColumnWidth(4,80)

        tela_produtos.tableWidget_produto_pesquisar.scrollToBottom()
        tela_produtos.tableWidget_produto_pesquisar.scrollToTop()
     

    def abrir_tela_marcas():
        Tela_Marca("tela_produtos.lineEdit_marca","VisualizarProduto.marca")
  

    def remover_marca():
        tela_produtos.lineEdit_marca.setText("NULL")
        VisualizarProduto.marca = None



    @classmethod
    def mudar_variacao(cls):
        
  
        try:
            button = tela_produtos.sender().parentWidget()
            index = tela_produtos.tableWidget_produto_pesquisar.indexAt(button.pos())

        except:
            return
            

        if index.isValid():
            index = index.row()
            VisualizarProduto.MudarVariacao.index_of_lis = index
            VisualizarProduto.MudarVariacao.setar_na_table()
            

            mudar_variacao.exec()
            VisualizarProduto.MudarVariacao.lis_variacao.clear()
            VisualizarProduto.MudarVariacao.index_of_lis = "NULL"
            VisualizarProduto.MudarVariacao.id_new_variacao = "NULL"
            VisualizarProduto.MudarVariacao.index_variacao = 100
        return


    
    class MudarVariacao:
        
        index_of_lis = "NULL"
        id_new_variacao = "NULL"
        lis_variacao = []
        index_variacao = 100


        @classmethod
        def setar_na_table(cls):
            mudar_variacao.listWidget.clear()
            
            index_variacao = tela_produtos.tableWidget_produto_pesquisar.cellWidget(VisualizarProduto.MudarVariacao.index_of_lis,2).layout().itemAt(0).widget().currentIndex()
            VisualizarProduto.MudarVariacao.index_variacao = index_variacao
            
            if index_variacao == 0:
                cur_variacao_id = VisualizarProduto.lis[VisualizarProduto.MudarVariacao.index_of_lis].ID_variacoes

                if cur_variacao_id == None:
                    cur_variacao_nome = "NULL"
                    mudar_variacao.lineEdit_variacao.setText(f"{cur_variacao_nome}")
                    orden = '''
                ORDER BY case Variacao when "P" then 0 
                when "PP" then 2 
                when "P" then 3 
                when "M" then 4 
                when "G" then 5 
                when "GG" then 6 
                when "XGG" then 7
                when "G1" then 8 
                when "G2" then 9 
                when "G3" then 10 
                ELSE variacao
                end ASC'''

                    temp = cursor.execute(f"select ID_Produtos from Codigo_Produtos where ID =  {VisualizarProduto.lis[VisualizarProduto.MudarVariacao.index_of_lis].ID}").fetchall()[0][0]
                    temp = cursor.execute(f"select ID_Grade from Produtos where ID = {temp}").fetchall()[0][0]
                    id_caracteristica = cursor.execute(f"select ID from Caracteristicas where ID_Grade = {temp} ORDER BY Descricao ASC").fetchall()
                    VisualizarProduto.MudarVariacao.lis_variacao = cursor.execute(f"select Variacao ,ID from Variacoes where ID_Caracteristica = {id_caracteristica[0][0]} {orden}").fetchall()
                    for i in range(len(VisualizarProduto.MudarVariacao.lis_variacao)):
                        mudar_variacao.listWidget.addItem(f"{VisualizarProduto.MudarVariacao.lis_variacao[i][0]}")


                else:
                    cur_variacao_nome = cursor.execute(f"select Variacao,ID from Variacoes  where id = {cur_variacao_id}").fetchall()[0][0]
                    mudar_variacao.lineEdit_variacao.setText(f"{cur_variacao_nome}")
                    orden = '''
                ORDER BY case Variacao when "P" then 0 
                when "PP" then 2 
                when "P" then 3 
                when "M" then 4 
                when "G" then 5 
                when "GG" then 6 
                when "XGG" then 7
                when "G1" then 8 
                when "G2" then 9 
                when "G3" then 10 
                ELSE variacao
                end ASC'''

                    variacao = cursor.execute(f"select ID_Caracteristica from Variacoes where id = {cur_variacao_id}").fetchall()[0][0]
                    VisualizarProduto.MudarVariacao.lis_variacao = cursor.execute(f"select Variacao,ID from Variacoes  where ID_Caracteristica = {variacao} {orden}").fetchall()

                    for i in range(len(VisualizarProduto.MudarVariacao.lis_variacao)):
                        mudar_variacao.listWidget.addItem(f"{VisualizarProduto.MudarVariacao.lis_variacao[i][0]}")


            elif index_variacao == 1:
                cur_variacao_id = VisualizarProduto.lis[VisualizarProduto.MudarVariacao.index_of_lis].ID_variacoes2

                if cur_variacao_id == None:
                    cur_variacao_nome = "NULL"
                    mudar_variacao.lineEdit_variacao.setText(f"{cur_variacao_nome}")
                    orden = '''
                ORDER BY case Variacao when "P" then 0 
                when "PP" then 2 
                when "P" then 3 
                when "M" then 4 
                when "G" then 5 
                when "GG" then 6 
                when "XGG" then 7
                when "G1" then 8 
                when "G2" then 9 
                when "G3" then 10 
                ELSE variacao
                end ASC'''
                    

                    temp = cursor.execute(f"select ID_Produtos from Codigo_Produtos where ID =  {VisualizarProduto.lis[VisualizarProduto.MudarVariacao.index_of_lis].ID}").fetchall()[0][0]
                    temp = cursor.execute(f"select ID_Grade from Produtos where ID = {temp}").fetchall()[0][0]
                    id_caracteristica = cursor.execute(f"select ID from Caracteristicas where ID_Grade = {temp} ORDER BY Descricao ASC").fetchall()
                    VisualizarProduto.MudarVariacao.lis_variacao = cursor.execute(f"select Variacao,ID from Variacoes where ID_Caracteristica = {id_caracteristica[1][0]} {orden}").fetchall()
                    for i in range(len(VisualizarProduto.MudarVariacao.lis_variacao)):
                        mudar_variacao.listWidget.addItem(f"{VisualizarProduto.MudarVariacao.lis_variacao[i][0]}")


                else:
                    cur_variacao_nome = cursor.execute(f"select Variacao from Variacoes where id = {cur_variacao_id}").fetchall()[0][0]
                    mudar_variacao.lineEdit_variacao.setText(f"{cur_variacao_nome}")
                    orden = '''
                ORDER BY case Variacao when "P" then 0 
                when "PP" then 2 
                when "P" then 3 
                when "M" then 4 
                when "G" then 5 
                when "GG" then 6 
                when "XGG" then 7
                when "G1" then 8 
                when "G2" then 9 
                when "G3" then 10 
                ELSE variacao
                end ASC'''

                    variacao = cursor.execute(f"select ID_Caracteristica from Variacoes where id = {cur_variacao_id}").fetchall()[0][0]
                    VisualizarProduto.MudarVariacao.lis_variacao = cursor.execute(f"select Variacao,ID from Variacoes where ID_Caracteristica = {variacao} {orden}").fetchall()

                    for i in range(len(VisualizarProduto.MudarVariacao.lis_variacao)):
                        mudar_variacao.listWidget.addItem(f"{VisualizarProduto.MudarVariacao.lis_variacao[i][0]}")


        @classmethod
        def pegar_nova_variacao(cls):

            index_ba = mudar_variacao.listWidget.currentRow()

            mudar_variacao.lineEdit_variacao.setText(f"{VisualizarProduto.MudarVariacao.lis_variacao[index_ba][0]}")
            VisualizarProduto.MudarVariacao.id_new_variacao = VisualizarProduto.MudarVariacao.lis_variacao[index_ba][1]



        @classmethod
        def adicionar_nova_variacao(cls):
        

            if VisualizarProduto.MudarVariacao.id_new_variacao == "NULL":
                return

            msg = QMessageBox(visualizar_grade)
            msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255); QDialog{border:1px solid;} QDialog::title{font-weight: bold;}')
            msg.setText(f'''  Gostaria de Trocar de variação?
            ''')



            msg.setWindowTitle("Confirmar A Troca De Variações.")
            msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)  
            msg = msg.exec_()

            if msg == QMessageBox.Yes:

                if VisualizarProduto.MudarVariacao.index_variacao == 0:
                    cursor.execute(f"update Codigo_Produtos set ID_variacoes = {VisualizarProduto.MudarVariacao.id_new_variacao} where ID = {VisualizarProduto.lis[VisualizarProduto.MudarVariacao.index_of_lis].ID}")
                    banco.commit()
                    VisualizarProduto.limpar_data()
                    abrir_navegar_produto()
                    return

                elif VisualizarProduto.MudarVariacao.index_variacao == 1:
                    cursor.execute(f"update Codigo_Produtos set ID_variacoes2 = {VisualizarProduto.MudarVariacao.id_new_variacao} where ID = {VisualizarProduto.lis[VisualizarProduto.MudarVariacao.index_of_lis].ID}")
                    banco.commit()
                    VisualizarProduto.limpar_data()
                    abrir_navegar_produto()
                    return
                return

            elif msg == QMessageBox.No:
                print("no")
                pass
                



    def apagar_itens_tableWidget(self):

        try:
            tela_produtos.label_menssage_produto_ver.clear()
            button = tela_produtos.sender()
            index = tela_produtos.tableWidget_produto_pesquisar.indexAt(button.pos())
        except:
            return
        if index.isValid():
            VisualizarProduto.qtd_produtos = str(int(VisualizarProduto.qtd_produtos) - 1).zfill(3)

            tela_produtos.label_produto_qtd_produtos.setText(f"Produtos: {VisualizarProduto.qtd_produtos}")

            tela_produtos.tableWidget_produto_pesquisar.cellWidget(index.row(),1).layout().itemAt(0).widget().text()

            VisualizarProduto.qtd_produtos_total = str(int(VisualizarProduto.qtd_produtos_total) - int(VisualizarProduto.lis[index.row()].quantidade)).zfill(3)
            tela_produtos.label_produto_qtd_itens.setText(f"Qtd. Itens Total: {VisualizarProduto.qtd_produtos_total}")

            VisualizarProduto.lis_del.append(VisualizarProduto.lis[index.row()].ID)

            del VisualizarProduto.lis[index.row()]

            tela_produtos.tableWidget_produto_pesquisar.removeRow(index.row())

    @classmethod
    def limpar_data(cls):
        VisualizarProduto.lis.clear()
        VisualizarProduto.lis_del.clear()
        VisualizarProduto.ID_grade = ""
        VisualizarProduto.qtd_produtos = "000"
        VisualizarProduto.qtd_produtos_total = "000"


    def setar_codigo():
        tela_produtos.label_menssage_produto_ver.clear()
        codigo = tela_produtos.tableWidget_produto_pesquisar.focusWidget().text()
        foc = tela_produtos.tableWidget_produto_pesquisar.focusWidget().parentWidget()
        index = tela_produtos.tableWidget_produto_pesquisar.indexAt(foc.pos())

        VisualizarProduto.lis[index.row()].Codigo = codigo
  



    def user_setar_qtd():
        try:
            tela_produtos.label_menssage_produto_ver.clear()
            
            quantidade = tela_produtos.tableWidget_produto_pesquisar.focusWidget().text()
        
            if len(quantidade) > 3:
                if int(quantidade[0]) == 0:
                    quantidade = quantidade[1:] 

                else:
                    quantidade = quantidade[:-1]

            
            tela_produtos.tableWidget_produto_pesquisar.focusWidget().setText(f"{str(quantidade).zfill(3)}")

            foc = tela_produtos.tableWidget_produto_pesquisar.focusWidget().parentWidget()
            index = tela_produtos.tableWidget_produto_pesquisar.indexAt(foc.pos())
            
            qtd_atual = VisualizarProduto.lis[index.row()].quantidade

            #qtd_final = int(qtd_atual) - int(quantidade)




            VisualizarProduto.qtd_produtos_total = str(int(VisualizarProduto.qtd_produtos_total) - int(qtd_atual) ).zfill(3)
   
            VisualizarProduto.qtd_produtos_total = str(int(VisualizarProduto.qtd_produtos_total) + int(quantidade) ).zfill(3)

            VisualizarProduto.lis[index.row()].quantidade = str(quantidade).zfill(3)



            tela_produtos.label_produto_qtd_itens.setText(f"Qtd. Itens Total: {VisualizarProduto.qtd_produtos_total}")

        except:
            return


    def mudar_carac_tableWidget():
        tela_produtos.label_menssage_produto_ver.clear()
        foc = tela_produtos.tableWidget_produto_pesquisar.focusWidget().parentWidget()
        index = tela_produtos.tableWidget_produto_pesquisar.indexAt(foc.pos())
        

        tela_produtos.tableWidget_produto_pesquisar.cellWidget(index.row(),3).layout().itemAt(0).widget().clear()
        
        cur_index = tela_produtos.tableWidget_produto_pesquisar.cellWidget(index.row(),2).layout().itemAt(0).widget().currentIndex()


        if cur_index == 0:
            tela_produtos.tableWidget_produto_pesquisar.cellWidget(index.row(),3).layout().itemAt(0).widget().addItem(f"{VisualizarProduto.lis[index.row()].variacao_nome}")

        elif cur_index == 1:
            tela_produtos.tableWidget_produto_pesquisar.cellWidget(index.row(),3).layout().itemAt(0).widget().addItem(f"{VisualizarProduto.lis[index.row()].variacao_nome2}")



    def salvar_alteracoes():
        tela_produtos.label_menssage_produto_ver.clear()

        descricao = tela_produtos.lineEdit_produto_descricao.text()

        if descricao == "":
            tela_produtos.label_menssage_produto_ver.setStyleSheet("color: rgb(170, 0, 0);")
            tela_produtos.label_menssage_produto_ver.setText("Campo 'Descrição' Não pode estar vazio!")
            return
            
        try:
            preco = format(float(tela_produtos.lineEdit_produto_preco.text().replace(",",".")),".2f")
        except:
            tela_produtos.label_menssage_produto_ver.setStyleSheet("color: rgb(170, 0, 0);")
            tela_produtos.label_menssage_produto_ver.setText("Campo 'Preço' Não pode estar vazio!")
            return

        ncm = tela_produtos.lineEdit_produto_ncm.text().replace(".","")

        print( VisualizarProduto.marca)
        if VisualizarProduto.marca == None:
            VisualizarProduto.marca = "NULL"
        else:
            VisualizarProduto.marca = f"'{VisualizarProduto.marca}'"

        cursor.execute(f" UPDATE Produtos SET  Marca = {VisualizarProduto.marca}, Nome = '{descricao}', preco = '{preco}', qtd_itens = {int(VisualizarProduto.qtd_produtos_total)} , qtd_produtos = {int(VisualizarProduto.qtd_produtos)} where ID = {VisualizarProduto.ID_Produtos};")
        cursor.execute(f" UPDATE Fiscal_Produtos SET NCM = '{ncm}' where ID_Produtos = {VisualizarProduto.ID_Produtos};")

        if VisualizarProduto.marca == "NULL":
            VisualizarProduto.marca = None


        for i in range(len(VisualizarProduto.lis_del)):
            cursor.execute(f"delete from Codigo_Produtos where ID = {VisualizarProduto.lis_del[i]};")


        for i in range(len(VisualizarProduto.lis)):
            try:

                cursor.execute(f"update Codigo_Produtos set quantidade = {VisualizarProduto.lis[i].quantidade}, Codigo = '{VisualizarProduto.lis[i].Codigo}' where ID = {VisualizarProduto.lis[i].ID}")
            
            except:
                tela_produtos.label_menssage_produto_ver.setStyleSheet("color: rgb(170, 0, 0);")
                tela_produtos.label_menssage_produto_ver.setText("codigo duplicado!!")
                return


        banco.commit()
        ban()
        tela_produtos.tableWidget_produto_pesquisar.scrollToTop()
        tela_produtos.label_menssage_produto_ver.setStyleSheet("color: rgb(0, 255, 0);")
        tela_produtos.label_menssage_produto_ver.setText("Salvo com sucesso!")

    
    def deletar_produto():
        msg = QMessageBox(tela_produtos)
        msg.setStyleSheet('background-color:#34495e;font: 75 12pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255); border:none;')
        msg.setText("Deseja excluir o Produto?")
        msg.setWindowTitle("Excluir Produto.")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)  
        msg = msg.exec_()

        if msg == QMessageBox.Yes:
            print("yes")
            pass
        elif msg == QMessageBox.No:
            print("no")
            return
        cursor.execute(f"delete from Produtos where ID = {VisualizarProduto.ID_Produtos}")

        print("id do produtoto ",VisualizarProduto.ID_Produtos)
        banco.commit()

        tela_produtos.close()
        ban()



caracteristica_linked_tela_produtos = []
variacao_linked_tela_produtos = []
variacao2_linked_tela_produtos = []


def abrir_tela_add_produtos_na_visualizacao():

    try:
        global caracteristica_linked_tela_produtos
        global variacao_linked_tela_produtos
        global variacao2_linked_tela_produtos


        cursor.execute(f"select ID, Descricao from Caracteristicas where ID_Grade = {VisualizarProduto.ID_grade}")

        caracteristica_linked_tela_produtos = cursor.fetchall()
        
        cursor.execute(f"select ID , Variacao from Variacoes where ID_Caracteristica = {caracteristica_linked_tela_produtos[0][0]}")

        variacao_linked_tela_produtos = cursor.fetchall()

        cursor.execute(f"select ID , Variacao from Variacoes where ID_Caracteristica = {caracteristica_linked_tela_produtos[1][0]}")

        variacao2_linked_tela_produtos = cursor.fetchall()
    
        cadastrar_produtos_linked_tela_produtos.comboBox_carac.clear()
        cadastrar_produtos_linked_tela_produtos.comboBox_carac2.clear()
        cadastrar_produtos_linked_tela_produtos.comboBox_varia.clear()
        cadastrar_produtos_linked_tela_produtos.comboBox_varia2.clear()

        cadastrar_produtos_linked_tela_produtos.comboBox_carac.addItem(str(caracteristica_linked_tela_produtos[0][1]))
        cadastrar_produtos_linked_tela_produtos.comboBox_carac2.addItem(str(caracteristica_linked_tela_produtos[1][1]))

        for i in range(len(variacao_linked_tela_produtos)):
            cadastrar_produtos_linked_tela_produtos.comboBox_varia.addItem(str(variacao_linked_tela_produtos[i][1]))


        
        for i in range(len(variacao2_linked_tela_produtos)):
            cadastrar_produtos_linked_tela_produtos.comboBox_varia2.addItem(str(variacao2_linked_tela_produtos[i][1]))

        cadastrar_produtos_linked_tela_produtos.show()

    except:
        return


def controle_de_zero_na_tela_liked_tela_produto():
    cadastrar_produtos_linked_tela_produtos.label.clear()
    try:
        if int(cadastrar_produtos_linked_tela_produtos.lineEdit_quantidade.text()):
            pass
    except:
        text = cadastrar_produtos_linked_tela_produtos.lineEdit_quantidade.text()
        text1= text[:-1]
        text = cadastrar_produtos_linked_tela_produtos.lineEdit_quantidade.setText(f"{text1}")
        return

    try:
        cadastrar_produtos_linked_tela_produtos.label.clear()
        
        quantidade = cadastrar_produtos_linked_tela_produtos.lineEdit_quantidade.text()
    
        if len(quantidade) > 3:
            if int(quantidade[0]) == 0:
                quantidade = quantidade[1:] 

            else:
                quantidade = quantidade[:-1]

        cadastrar_produtos_linked_tela_produtos.lineEdit_quantidade.setText(str(quantidade).zfill(3))
    
    except:
        return


def adicionar_mercadoria_linked_tela_produtos():
    cadastrar_produtos_linked_tela_produtos.label.clear()
    id = randint(100000000,999999999)

    codigo = cadastrar_produtos_linked_tela_produtos.lineEdit_codigo.text()
    quantidade =  int(cadastrar_produtos_linked_tela_produtos.lineEdit_quantidade.text())

    cursor.execute(f"select * from Codigo_Produtos where Codigo = '{codigo}'")

    if len(cursor.fetchall()) > 0:
        cadastrar_produtos_linked_tela_produtos.label.setStyleSheet("color: rgb(255, 0, 0); border:none;")
        cadastrar_produtos_linked_tela_produtos.label.setText("codigo inserido ja existe!")
        return


    index = cadastrar_produtos_linked_tela_produtos.comboBox_varia.currentIndex()
    index2 = cadastrar_produtos_linked_tela_produtos.comboBox_varia2.currentIndex()

    id_variacao = variacao_linked_tela_produtos[index][0]
    id_variacao2 = variacao2_linked_tela_produtos[index2][0]



    while True:
            
        cursor.execute(f"select * from Codigo_Produtos where ID ={id}")
        dados = cursor.fetchall()

        if len(dados) == 0:
            break

        else:
            id = randint(100000000,99999999)

    v = "'"
    cursor.execute("insert into Codigo_Produtos values (?,?,?,?,?,?)",(id_variacao,id_variacao2,VisualizarProduto.ID_Produtos,id,str(quantidade),codigo))

    
    VisualizarProduto.qtd_produtos = str(int(VisualizarProduto.qtd_produtos) + 1).zfill(3)
    VisualizarProduto.qtd_produtos_total = str(int(VisualizarProduto.qtd_produtos_total) + int(quantidade)).zfill(3)
    cursor.execute(f"update Produtos set qtd_itens = {VisualizarProduto.qtd_produtos_total},qtd_produtos = {VisualizarProduto.qtd_produtos} where ID = {VisualizarProduto.ID_Produtos}")


    banco.commit()
  
    cadastrar_produtos_linked_tela_produtos.lineEdit_codigo.clear()

    tela_produtos.label_produto_qtd_produtos.setText(f"Produtos: {VisualizarProduto.qtd_produtos}")

    tela_produtos.label_produto_qtd_itens.setText(f"Qtd. Itens Total: {VisualizarProduto.qtd_produtos_total}")
    
    cadastrar_produtos_linked_tela_produtos.close()
    tela_produtos.close()
    VisualizarProduto.limpar_data()
    ban()
    





##################################################    ************** Config ************    ######################################################################



def adicionar_usuario():
    Nome_new_usuario = tela_admin.lineEdit_adicionar_usuarios_nome.text().lstrip().rstrip().replace("'","")
    senha_login_new_usuario = tela_admin.lineEdit_adicionar_usuarios_senha_login.text().lstrip().rstrip().replace("'","")
    senha_acesso_new_usuario = tela_admin.lineEdit_adicionar_usuarios_senha_acesso.text().lstrip().rstrip().replace("'","")

    
    if Nome_new_usuario == "" or senha_login_new_usuario == "" or senha_acesso_new_usuario == "": 
        msg = QMessageBox(visualizar_grade)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
        msg.setText(f''' ERRO: Os espaços não podem ficar em branco.''')
        msg.setIcon(QMessageBox. Warning)
        msg.setWindowTitle("Espaço em branco.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)  
        tela_admin.lineEdit_adicionar_usuarios_nome.clear()
        msg = msg.exec_()
        tela_admin.lineEdit_adicionar_usuarios_nome.setFocus()
        return


    #verificar se o nome do usuario existe
    if len(cursor.execute(f"select * from Usuario where usuario = '{Nome_new_usuario}'").fetchall()) > 0:
        msg = QMessageBox(visualizar_grade)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
        msg.setText(f''' ERRO: Nome escolhido ja estar sendo ultilizado.''')
        msg.setIcon(QMessageBox. Warning)
        msg.setWindowTitle("Nome em ultilização.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)  
        tela_admin.lineEdit_adicionar_usuarios_nome.clear()
        msg = msg.exec_()
        tela_admin.lineEdit_adicionar_usuarios_nome.setFocus()
        return

    #pegar o proximo id
    id = cursor.execute("select ifnull((SELECT max(ID) from usuario where id != 1000000000),0)").fetchall()[0][0] + 1


    cursor.execute("insert into usuario values(?,?,?,?)", (id,Nome_new_usuario,senha_login_new_usuario,senha_acesso_new_usuario))
    cursor.execute("insert into Acesso_usuario(ID,ID_Usuario) values (?,?)",(id,id))

    banco.commit()
    tela_admin.lineEdit_adicionar_usuarios_nome.clear()
    tela_admin.lineEdit_adicionar_usuarios_senha_login.clear()
    tela_admin.lineEdit_adicionar_usuarios_senha_acesso.clear()
    setar_initial_config()

    







def setar_initial_config():


    index = tela_admin.tabWidget_config.currentIndex()

    if index == 0:
        file = f"{c}\DataBase\Config.ini"
        config = ConfigParser()
        config.read(file)

        tela_admin.lineEdit_cnpj.setText(f'{config["Empresa"]["cnpj"]}')
        tela_admin.lineEdit_nome_empresa.setText(f'{config["Empresa"]["nome"]}')
        tela_admin.lineEdit_nome_fantasia.setText(f'{config["Empresa"]["nome_fantasia"]}')
        tela_admin.lineEdit_logradouro.setText(f'{config["Empresa"]["logradouro"]}')
        tela_admin.lineEdit_bairro.setText(f'{config["Empresa"]["bairro"]}')
        tela_admin.lineEdit_numero.setText(f'{config["Empresa"]["numero"]}')
        tela_admin.lineEdit_cep.setText(f'{config["Empresa"]["cep"]}')
        tela_admin.lineEdit_municipio.setText(f'{config["Empresa"]["municipio"]}')
        tela_admin.lineEdit_uf.setText(f'{config["Empresa"]["uf"]}')

        tela_admin.lineEdit_incricao_estadual.setText(f'{config["Empresa"]["inscricao"]}')
        tela_admin.lineEdit_icms_situacao_tributaria.setText(f'{config["Empresa"]["icms_situacao_tributaria"]}')
        tela_admin.lineEdit_token.setText(f'{config["NFE"]["token_produtocao"]}')
        tela_admin.lineEdit_ref_nota.setText(f'{config["NFE"]["ref"]}')
        return


    

    elif index == 1:


        if tela_admin.listWidget_permissoes.count() == 0: 

            retorno = PedirPermissao().return_answer()

            if retorno:
                pass
            else:
                tela_admin.tabWidget_config.setCurrentIndex(0)
                return

        tela_admin.listWidget_usuario.clear()
        tela_admin.listWidget_permissoes.clear()

        admin = cursor.execute("select usuario,Senha_login,Senha_Acesso from Usuario where ID = 1000000000").fetchall()[0]

        tela_admin.listWidget_usuario.addItem(f"{admin[0]} (Adiministrador)")


        AddWidget.space()
        AddWidget.add_label("Permissões : Todas")
        AddWidget.space()
        AddWidget.add_label("Usuário")
        AddWidget.add_line(f"{admin[0]}",tipo = "Nome")
        AddWidget.space()
        AddWidget.add_label("Senha De login","Mostrar Senha")
        AddWidget.add_line(f"{admin[1]}",QLineEdit.EchoMode.Password,"login")
        AddWidget.space()
        AddWidget.add_label("Senha De acesso","Mostrar Senha")
        AddWidget.add_line(f"{admin[2]}",QLineEdit.EchoMode.Password,"acesso")


        tela_admin.listWidget_usuario.setCurrentRow(0)

        usuarios_nome = cursor.execute("select usuario from Usuario where ID != 1000000000 order by ID ASC").fetchall()

        for i in range(len(usuarios_nome)):
            tela_admin.listWidget_usuario.addItem(usuarios_nome[i][0])

        
    elif index == 2:
        tela_admin.listWidget_info_adicionais_cupom_nao_fiscal.clear()
        file = f"{c}\DataBase\Config.ini"
        config = ConfigParser()
        config.read(file)

        tela_admin.lineEdit_largura_pagina.setText(f'{config["Recibo"]["page_width"]}')
        tela_admin.lineEdit_altura_pagina.setText(f'{config["Recibo"]["page_height"]}')
        tela_admin.lineEdit_nome_loja.setText(f'{config["Recibo"]["loja_titulo"]}')
        tela_admin.lineEdit_nome_empresa_cupom_nfiscal.setText(f'{config["Recibo"]["nome_empresa"]}')
        tela_admin.lineEdit_cep_nfical.setText(f'{config["Recibo"]["cep"]}')
        tela_admin.lineEdit_tel_nao_fiscal.setText(f'{config["Recibo"]["tel"]}')
        tela_admin.lineEdit_endereco_nfiscal.setText(f'{config["Recibo"]["endereco"]}')
        tela_admin.lineEdit_completo_nfiscal.setText(f'{config["Recibo"]["endereco_completo"]}')
        tela_admin.spinBox_font_size_nome_loja.setValue(int(f'{config["Recibo"]["loja_titulo_font_size"]}'))

        itens = json.loads(config.get("Recibo","informacoes_adicionais"))
        for i in range(len(itens)):
            tela_admin.listWidget_info_adicionais_cupom_nao_fiscal.addItem(itens[i])





def index_changed_usuarios():
    index = tela_admin.listWidget_usuario.currentIndex().row()

    tela_admin.listWidget_permissoes.clear()

    if index == 0:
        admin = cursor.execute("select usuario,Senha_login,Senha_Acesso from Usuario where ID = 1000000000").fetchall()[0]

        AddWidget.space()
        AddWidget.add_label("Permissões : Todas")
        AddWidget.space()
        AddWidget.add_label("Usuário")
        AddWidget.add_line(f"{admin[0]}",tipo = "Nome")
        AddWidget.space()
        AddWidget.add_label("Senha De login","Mostrar Senha")
        AddWidget.add_line(f"{admin[1]}",QLineEdit.EchoMode.Password,"login")
        AddWidget.space()
        AddWidget.add_label("Senha De acesso","Mostrar Senha")
        AddWidget.add_line(f"{admin[2]}",QLineEdit.EchoMode.Password,"acesso")
        return

    if index-1 == -1 or index == -1:
        return

    usuario = cursor.execute("select * from Usuario where ID != 1000000000 order by ID ASC").fetchall()[index-1]

    permissoes = list(cursor.execute(f"select * from Acesso_usuario where ID_usuario = {usuario[0]}").fetchall()[0])[2:]

    nome_permissoes = list(cursor.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('Acesso_usuario')").fetchall()[2:])


    AddWidget.space()
    AddWidget.add_label("Permissões:")
    AddWidget.space()

    for i in range(len(nome_permissoes)):
        AddWidget.add_check_permision(f'{nome_permissoes[i][0].replace("_"," ")}',"Permitir",True if permissoes[i] == 1 else False)


    AddWidget.space()
    AddWidget.add_label("Usuário")
    AddWidget.add_line(f"{usuario[1]}",tipo = "Nome")
    AddWidget.space()
    AddWidget.add_label("Senha De login","Mostrar Senha")
    AddWidget.add_line(f"{usuario[2]}",QLineEdit.EchoMode.Password,"login")
    AddWidget.space()
    AddWidget.add_label("Senha De acesso","Mostrar Senha")
    AddWidget.add_line(f"{usuario[3]}",QLineEdit.EchoMode.Password,"acesso")
    AddWidget.space()
    AddWidget.add_push_button_deletar("Excluir Usuário")



         
class FuctionsToWidgets:

    def excluir_usuario():
        msg = QMessageBox(visualizar_grade)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255); QDialog{border:1px solid;} QDialog::title{font-weight: bold;}')
        msg.setText(f''' Deseja excluir o usuário?''')
        msg.setWindowTitle("Deseja excluir o Usuário")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)  
        msg = msg.exec_()

        if msg == QMessageBox.Yes:
            print("yes")
            pass
        elif msg == QMessageBox.No:
            print("no")
            return

        row = tela_admin.listWidget_usuario.currentRow()
        id = cursor.execute("SELECT id from Usuario WHERE id != 1000000000 order by ID asc").fetchall()[row-1][0]
        cursor.execute(f"delete from usuario where ID = {id}")
        banco.commit()
        setar_initial_config()


    def motrar_senha():
        check = tela_admin.listWidget_permissoes.focusWidget()

        if check.isChecked():
            index = tela_admin.listWidget_permissoes.indexAt(check.parent().pos())  
            item = tela_admin.listWidget_permissoes.item(index.row() + 1)
            line = tela_admin.listWidget_permissoes.itemWidget(item).setEchoMode(QLineEdit.EchoMode.Normal)

        else:
            index = tela_admin.listWidget_permissoes.indexAt(check.parent().pos())  
            item = tela_admin.listWidget_permissoes.item(index.row() + 1)
            line = tela_admin.listWidget_permissoes.itemWidget(item).setEchoMode(QLineEdit.EchoMode.Password)


    def mudar_senha(tipo = "None"):

        input_new = tela_admin.listWidget_permissoes.focusWidget().text().replace("'","").rstrip().lstrip()
        tela_admin.listWidget_permissoes.focusWidget().setText(f"{input_new}")
        row = tela_admin.listWidget_usuario.currentRow()
        
        def menssagem_ok():
            msg = QMessageBox(visualizar_grade)
            msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
            msg.setText(f'''Salvo com sucesso!''')
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Salvo")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)  
            msg = msg.exec_()

        if row == 0:
            id = 1000000000

        else:
            id = cursor.execute("SELECT id from Usuario WHERE id != 1000000000 order by ID asc").fetchall()[row-1][0]


        if tipo == "login":
            cursor.execute(f"update Usuario set Senha_login = '{input_new}' where id = {id}")
            banco.commit()
            menssagem_ok()
            return

        elif tipo == "acesso":
            cursor.execute(f"update Usuario set Senha_Acesso = '{input_new}' where id = {id}")
            banco.commit()           
            menssagem_ok()
            return

        elif tipo == "Nome":
            cursor.execute(f"update Usuario set usuario = '{input_new}' where id = {id}")
            banco.commit()
            if row == 0:
                tela_admin.listWidget_usuario.item(row).setText(f"{input_new} (Adiministrador)")
            else:
                tela_admin.listWidget_usuario.item(row).setText(input_new)

            menssagem_ok()
            return

        else:
            pass

    def menssagem_ok():
            msg = QMessageBox(visualizar_grade)
            msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
            msg.setText(f'''Salvo com sucesso!''')
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Salvo")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)  
            msg = msg.exec_()


    def setar_permition():
        row = tela_admin.listWidget_usuario.currentRow()
        id = cursor.execute("SELECT id from Usuario WHERE id != 1000000000 order by ID asc").fetchall()[row-1][0]

        widget = tela_admin.listWidget_permissoes.focusWidget()

        ComboBoxChecked = widget.isChecked()



        coluna_nome = widget.parentWidget().children()[1].text().replace(" ","_")

        if ComboBoxChecked:

            cursor.execute(f"update Acesso_usuario set {coluna_nome} = 1 where ID_usuario = {id}")
            banco.commit()

        else:
            cursor.execute(f"update Acesso_usuario set {coluna_nome} = 0 where ID_usuario = {id}")
            banco.commit()



class AddWidget:

    def add_label(texto = "",checkBox = ""):
        item = QListWidgetItem("")
        label = QLabel(f"{texto}",tela_admin)
        label.setStyleSheet('font: 75 16pt "MS Shell Dlg 2" ; font-weight :bold;border:none;')

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(label)

        
        if checkBox != "":
            check = QCheckBox(checkBox,tela_admin)
            check.stateChanged.connect(FuctionsToWidgets.motrar_senha)
            layout.addWidget(check)


        tela_admin.listWidget_permissoes.addItem(item)
        tela_admin.listWidget_permissoes.setItemWidget(item,container)


    def space():
        item = QListWidgetItem("")
        label = QLabel("",tela_admin)
        tela_admin.listWidget_permissoes.addItem(item)
        tela_admin.listWidget_permissoes.setItemWidget(item,label)


    def add_line(texto = "" , echo = QLineEdit.EchoMode.Normal,tipo = "None"):
        line = QLineEdit(f"{texto}",tela_admin)
        line.setStyleSheet('font: 75 14pt "MS Shell Dlg 2" ;')
        line.setMaxLength(30)
        line.setEchoMode(echo)
        line.returnPressed.connect(lambda:FuctionsToWidgets.mudar_senha(tipo))
        item = QListWidgetItem("")
        tela_admin.listWidget_permissoes.addItem(item)
        tela_admin.listWidget_permissoes.setItemWidget(item,line)


    def add_check_permision(texto = "",checkBox = "",checkBoxChecked = False):
        item = QListWidgetItem("")
        label = QLabel(f"{texto}",tela_admin)
        label.setStyleSheet('font: 75 10pt "MS Shell Dlg 2" ; font-weight :bold;border:none;')

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(label)

    
        check = QCheckBox(checkBox,tela_admin)
        check.setChecked(checkBoxChecked)
        check.stateChanged.connect(FuctionsToWidgets.setar_permition)
        layout.addWidget(check)


        tela_admin.listWidget_permissoes.addItem(item)
        tela_admin.listWidget_permissoes.setItemWidget(item,container)


    def add_push_button_deletar(texto):
        btn = QPushButton(f"{texto}")
        btn.setStyleSheet('font: 75 14pt "MS Shell Dlg 2" ; background-color:rgb(85, 0, 0); color:rgb(255,255,255)')
        btn.clicked.connect(FuctionsToWidgets.excluir_usuario)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        item = QListWidgetItem("")
        tela_admin.listWidget_permissoes.addItem(item)
        tela_admin.listWidget_permissoes.setItemWidget(item,btn)





############################################## EMPRESA #########################################




def salvar_dados_empresa():
    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    cnpj = tela_admin.lineEdit_cnpj.text()
    nome_empresa = tela_admin.lineEdit_nome_empresa.text()
    nome_fantasia = tela_admin.lineEdit_nome_fantasia.text()
    logradouro = tela_admin.lineEdit_logradouro.text()
    bairro = tela_admin.lineEdit_bairro.text()
    numero = tela_admin.lineEdit_numero.text()
    cep = tela_admin.lineEdit_cep.text()
    municipio = tela_admin.lineEdit_municipio.text()
    uf = tela_admin.lineEdit_uf.text()

    incricao_estadual = tela_admin.lineEdit_incricao_estadual.text()
    icms_situacao_tributaria = tela_admin.lineEdit_icms_situacao_tributaria.text()
    token = tela_admin.lineEdit_token.text()
    ref_nota = tela_admin.lineEdit_ref_nota.text()


    config["Empresa"]["cnpj"] =cnpj
    config["Empresa"]["nome"] =nome_empresa
    config["Empresa"]["nome_fantasia"] =nome_fantasia
    config["Empresa"]["logradouro"] =logradouro
    config["Empresa"]["bairro"] =bairro
    config["Empresa"]["numero"] =numero
    config["Empresa"]["cep"] =cep 
    config["Empresa"]["municipio"] =municipio
    config["Empresa"]["uf"] =uf

    config["Empresa"]["inscricao"] =incricao_estadual
    config["Empresa"]["icms_situacao_tributaria"] =icms_situacao_tributaria
    config["NFE"]["token_produtocao"] =token
    config["NFE"]["ref"] =ref_nota

    with open(file, 'w') as configfile:
        config.write(configfile)

    FuctionsToWidgets.menssagem_ok()







############################################# ********   Personalizar cumpom não fiscal  ******** ############################################# 



def setar_a_imagem(file):

    rect = QRect(0,0,180,4180)
    maps = QPixmap(file)
    cropped = QPixmap(maps.copy(rect))
    tela_admin.label_image_cupom_test.setPixmap(QPixmap(cropped))


def fazer_cupom_de_teste():
    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    largura = tela_admin.lineEdit_largura_pagina.text()
    altura = tela_admin.lineEdit_altura_pagina.text()
    nome = tela_admin.lineEdit_nome_loja.text()
    nome_empresa = tela_admin.lineEdit_nome_empresa_cupom_nfiscal.text()
    cep = tela_admin.lineEdit_cep_nfical.text()
    tel = tela_admin.lineEdit_tel_nao_fiscal.text()
    endereco = tela_admin.lineEdit_endereco_nfiscal.text()
    completo  = tela_admin.lineEdit_completo_nfiscal.text()
    font_size = tela_admin.spinBox_font_size_nome_loja.value()

    info_adicionais = []
    for i in range(tela_admin.listWidget_info_adicionais_cupom_nao_fiscal.count() ):
        info_adicionais.append(tela_admin.listWidget_info_adicionais_cupom_nao_fiscal.item(i).text())

    config["Recibo"]["page_width"] =  str(largura)
    config["Recibo"]["page_height"] =str(altura)
    config["Recibo"]["loja_titulo"] =str(nome)
    config["Recibo"]["nome_empresa"] =str(nome_empresa)
    config["Recibo"]["cep"] = str(cep)
    config["Recibo"]["tel"] =  str(tel)
    config["Recibo"]["endereco"] =    str(endereco)
    config["Recibo"]["endereco_completo"] =  str(completo)
    config["Recibo"]["loja_titulo_font_size"] =  str(font_size)
    config["Recibo"]["informacoes_adicionais"] =  str(info_adicionais).replace("'",'"')


    with open(file, 'w') as configfile:
        config.write(configfile)



    nome_arquivo = "Desmontração De teste"

    recibo = Recibo("3","3","30,00","20,00",nome_arquivo,[["Dinheiro"]],["50,00"],"0%")

    for i in range(3):
        recibo.add_itens("1234567891","Produto De Test","1","10,00","0%","10,00")

    recibo.criar_recibo()

    output = f"{c}\cupom_vendas\Recibos\{nome_arquivo}.pdf"
    poppler = rf"{c}\cupom_vendas\poppler-0.68.0\bin"
    images = convert_from_path(output,500,poppler_path=poppler) #dpi=200, grayscale=True, size=(300,400), first_page=0, last_page=3)

    for image in images:
        image.save(rf"{c}\cupom_vendas\Recibos\Desmontração De teste.jpeg","JPEG")




def tela_imprimir_cupom():
    

    image_viwer.comboBox.clear()
    nome_arquivo = "Desmontração De teste"
    output = f"{c}\cupom_vendas\Recibos\Desmontração De teste.jpeg"
    pixmap = QPixmap(output)
    image_viwer.label.setPixmap(pixmap)
    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    cur_impressora = config["Config_Impressao"]["impressora_cupom"]

    impressora = list(win32print.EnumPrinters(2))

    for i in range(len(impressora)):
        if str(cur_impressora) == str(impressora[i][2]):
            del impressora[i]
            image_viwer.comboBox.addItem(f"{cur_impressora}")
            break


    for i in range(len(impressora)):
        image_viwer.comboBox.addItem(impressora[i][2])

    image_viwer.show()


def imprimir_cupom():
    output = f"{c}\cupom_vendas\Recibos\Desmontração De teste.pdf"
    impressora = image_viwer.comboBox.currentText()

    
    try:
        win32print.SetDefaultPrinterW(impressora)
        win32api.ShellExecute(0,"print",output,None,".",0)

    except:
        msg = QMessageBox(visualizar_grade)
        msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
        msg.setText(f'''algo Deu errado''')
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)  
        msg = msg.exec_()
        return




def setar_impressora_padrao():
    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    impressora = image_viwer.comboBox.currentText()
    config["Config_Impressao"]["impressora_cupom"] = impressora
    with open(file, 'w') as configfile:
        config.write(configfile)
    


def add_info_adicionais_():

    item = tela_admin.lineEdit_adicionar_info_adicionais.text().rstrip().lstrip().replace('"',"").replace("'",'')
    if item == "":
        return
    tela_admin.listWidget_info_adicionais_cupom_nao_fiscal.addItem(f"{item}")
    tela_admin.lineEdit_adicionar_info_adicionais.clear()

def remover_items_cupom_nao_fiscal():
    item = tela_admin.listWidget_info_adicionais_cupom_nao_fiscal.currentRow() 
    tela_admin.listWidget_info_adicionais_cupom_nao_fiscal.takeItem(item)


image_viwer.pushButton.clicked.connect(imprimir_cupom)
image_viwer.pushButton_2.clicked.connect(setar_impressora_padrao)
tela_admin.pushButton_salvar_config_cupom.clicked.connect(fazer_cupom_de_teste)
tela_admin.pushButton_imprimir.clicked.connect(tela_imprimir_cupom)

tela_admin.lineEdit_adicionar_info_adicionais.returnPressed.connect(add_info_adicionais_)
tela_admin.listWidget_info_adicionais_cupom_nao_fiscal.itemDoubleClicked.connect(remover_items_cupom_nao_fiscal)



















