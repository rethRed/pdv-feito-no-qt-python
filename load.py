import sqlite3,datetime,time,ctypes
import pyautogui, threading,shutil
from PyQt5.QtWidgets import  QFileDialog,QWidget,qApp,QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QKeyEvent,QKeySequence,QFocusEvent,QDoubleValidator,QIntValidator,QMovie, QPixmap,QIcon,QFont,QColor,QBrush,QFontInfo,QPainter
from PyQt5 import uic,QtWidgets,QtGui,QtCore,QtPrintSupport
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,\
    QPrintPreviewDialog,QPrinterInfo
from configparser import ConfigParser
from random import randint
from PyQt5.QtCore import QObject, QThread, pyqtSignal,QCoreApplication,QPoint,QRunnable,QThreadPool,QTime,QEvent,QDateTime,QPointF
from PyQt5.QtWidgets import (QApplication, QWidget,QSpacerItem,QSizePolicy,QHBoxLayout,QVBoxLayout,QLabel,QFileDialog,QHeaderView,QTableWidgetItem,QToolButton,QListWidgetItem,QCheckBox)
from PyQt5.Qt import Qt
import win32api
import win32print
import os
from fpdf import FPDF
import datetime
from pdf2image import convert_from_path
import sys
import json
import requests
import datetime
import copy,pdfkit
from pdf2image import convert_from_path
from pdf2image.exceptions import (
     PDFInfoNotInstalledError,
     PDFPageCountError,
     PDFSyntaxError
     )

import gui.admin.resources_rc

import numpy as np; np.random.seed(1)
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import Cursor as cursor_grafico

import mplcursors
import pyqtgraph as pg

from PyQt5.QtChart import (QChart,QChartView,QPieSeries,QPieSlice)
from  PyQt5.QtGui import QPen
    
ades = 0
descontu= 0
quantidade_produtos_total=0 
total = 0.00
lis = []
zero = 0
desconto_unico = 0
qpro = 0
c= os. getcwd()
#carregar sql

try:
    banco = sqlite3.connect(fr"{c}\\DataBase\\produtos.db",check_same_thread=False)

except:
    banco = sqlite3.connect(fr"{c}\produtos.db",check_same_thread=False)


cursor = banco.cursor()
cursor_tela_admim = banco.cursor()
cursor_estatistica = banco.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")


#carregar as telas

app=QtWidgets.QApplication([])

tela_admin = uic.loadUi(fr"{c}\gui\admin\tela_admin.ui")
tela_error = uic.loadUi(fr"{c}\gui\admin\tela_error.ui")
tela_add_marcas = uic.loadUi(fr"{c}\gui\admin\add marcas.ui")
tela_aviso= uic.loadUi(fr"{c}\gui\vendas\tela_aviso.ui")
tela_imprimir= uic.loadUi(fr"{c}\gui\admin\imprimir.ui")
configurar_bot= uic.loadUi(fr"{c}\gui\admin\configurar_bot.ui")
tela_vendas = uic.loadUi(fr"{c}\gui\vendas\tela_vendas.ui")
tela_desconto = uic.loadUi(fr"{c}\gui\vendas\tela_desconto.ui")
tela_remover = uic.loadUi(fr"{c}\gui\vendas\remover_produto.ui")
pesquisar_produtos = uic.loadUi(fr"{c}\gui\vendas\pesquisar_produtos.ui")
tela_sub_total = uic.loadUi(fr"{c}\gui\vendas\sub_total.ui")
tela_login = uic.loadUi(fr"{c}\gui\login\tela_login.ui")
Tela_modificar_admin = uic.loadUi(fr"{c}\gui\admin\modificar_admin.ui")
Tela_exportar = uic.loadUi(fr"{c}\gui\admin\exportar_db.ui")
Tela_registro_vendas = uic.loadUi(fr"{c}\gui\admin\tela_registro_vendas.ui")
abrir_caixa = uic.loadUi(fr"{c}\gui\vendas\abrir_caixa.ui")
confirmaçao = uic.loadUi(fr"{c}\gui\vendas\confirmaçao_nfe.ui")
resumo_operacao = uic.loadUi(fr"{c}\gui\vendas\resumo_da_operaçao.ui")
gerenciamento_caixa = uic.loadUi(fr"{c}\gui\gerenciamento\gerenciamento_caixa.ui")
adicionar_produto_nfce = uic.loadUi(fr"{c}\gui\gerenciamento\adicionar_produto_nfce.ui")
escolher_grade = uic.loadUi(fr"{c}\gui\admin\escolher_grade.ui")
confirmar_trocar_grade = uic.loadUi(fr"{c}\gui\admin\confirmar_trocar_grade.ui")
pesquisar_ncm = uic.loadUi(fr"{c}\gui\admin\pesquisar_ncm.ui")
tela_produtos = uic.loadUi(fr"{c}\gui\admin\tela_produtos.ui")
cadastrar_produtos_linked_tela_produtos = uic.loadUi(fr"{c}\gui\admin\tela_cadastrarProdutos_linked_tela_produtos.ui")
mudar_variacao = uic.loadUi(fr"{c}\gui\admin\mudar_variacao.ui")
pegar_permissao = uic.loadUi(fr"{c}\gui\login\PedirPermicao.ui")
visualizar_grade = uic.loadUi(fr"{c}\gui\admin\visualizar_grade.ui")
fiscal_cadastro = uic.loadUi(fr"{c}\gui\admin\cadastro_fiscal.ui")
image_viwer = uic.loadUi(fr"{c}\gui\admin\image_viwer.ui")
fecha_caixar = uic.loadUi(fr"{c}\gui\vendas\fechar_caixa.ui")
registrar_entrada = uic.loadUi(fr"{c}\gui\vendas\registrar_entrada.ui")
resgistrar_saida = uic.loadUi(fr"{c}\gui\vendas\resistrar_saida.ui")
resumo_do_caixa = uic.loadUi(fr"{c}\gui\vendas\Resumo_do_caixa.ui")
estatisticas = uic.loadUi(fr"{c}\gui\admin\estatistica.ui")
estastiticas_venda = uic.loadUi(fr"{c}\gui\admin\venda_estatistica.ui")
mudar_nome_marca = uic.loadUi(fr"{c}\gui\admin\mudar_nome_marca.ui")
tela_imprimir_arquivo = uic.loadUi(fr"{c}\gui\gerenciamento\imprimir_arquivo_global.ui")
tela_salvar_arquivos = uic.loadUi(fr"{c}\gui\gerenciamento\salvar_arquivos.ui")
caixa_estatistica_view = uic.loadUi(fr"{c}\gui\admin\caixa_estatisticas_view.ui")
visualizar_produtos_nas_vendas = uic.loadUi(fr"{c}\gui\vendas\visualizar_produtos_nas_vendas.ui")
trocar_venda_vendas_view_estatisticas = uic.loadUi(fr"{c}\gui\admin\trocar_venda.ui")



def setIcon():
    tela_admin.pushButton_inicio.setIcon(QIcon(rf"{c}\imagem\Resources TelaAdmin\home.png"))
    tela_admin.pushButton_analize.setIcon(QIcon(rf"{c}\imagem\Resources TelaAdmin\diagram1.png"))
    tela_admin.pushButton_visualizar_produtos.setIcon(QIcon(rf"{c}\imagem\Resources TelaAdmin\lupa.png"))
    tela_admin.pushButton_cadastrar_produtos.setIcon(QIcon(rf"{c}\imagem\Resources TelaAdmin\register png.png"))
    tela_admin.pushButton_cadastrar_grades.setIcon(QIcon(rf"{c}\imagem\Resources TelaAdmin\register png.png"))
    tela_admin.pushButton_configuracoes.setIcon(QIcon(rf"{c}\imagem\Resources TelaAdmin\Lrg-settings.png"))
    tela_admin.label_10.setPixmap(QPixmap(rf"{c}\imagem\Resources TelaAdmin\acount_icon.png"))
    tela_admin.pushButton_recarregar.setIcon(QIcon(rf"{c}\imagem\refresh (1).png"))
    tela_admin.label_49.setPixmap(QPixmap(rf"{c}\imagem\Resources TelaAdmin\money-bag.png"))
    tela_admin.label_52.setPixmap(QPixmap(rf"{c}\imagem\Resources TelaAdmin\money-bag.png"))
    

setIcon()



#carregar widget
widget = QtWidgets.QStackedWidget()
widget.addWidget(tela_vendas)
widget.addWidget(tela_admin)
widget.addWidget(tela_sub_total)
widget.addWidget(tela_login)
widget.addWidget(resumo_operacao)
widget.addWidget(gerenciamento_caixa)


widget.showFullScreen()
widget.setCurrentIndex(3)

tela_sub_total.lineEdit_parcelas.setVisible(False)
tela_sub_total.label_parcelas.setVisible(False)
tela_sub_total.lineEdit_parcelas.setValidator(QIntValidator())

def detectar_input_tela_resulmo(event):
    if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
        from Core.vendas.tela_vendas import produto
        produto.editavel = False
        tela_vendas.lineEdit_codigo.setText(f'CAIXA LIVRE') 
        produto.editavel = True
        widget.setCurrentIndex(0) 
        return
    widget.setCurrentIndex(0) 
    try:
        key = event.key()
        key = chr(key)
        tela_vendas.lineEdit_codigo.setText(f"{key}")
    except:
        return

    tela_vendas.lineEdit_codigo.setText(f"{key}")

resumo_operacao.keyPressEvent = detectar_input_tela_resulmo




#só deixar ai para se eu quiser tirar a parte de cima de alguma janela

confirmaçao.setWindowFlags(Qt.FramelessWindowHint) 




pegar_permissao.setWindowFlags(Qt.FramelessWindowHint)
pegar_permissao.pushButton_sair.setVisible(False)
    
fechar_tela_abrir_caixa = False


def get_cur_caixa_id():
    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    return config["Caixa"]["id"]


class PedirPermissao:

    def __init__(self):

        pegar_permissao.lineEdit_senha.setFocus()
        pegar_permissao.pushButton_confimar.clicked.connect(self.run)
        pegar_permissao.lineEdit_senha.returnPressed.connect(self.run)


        self.fecharJanela = "Não"
        
        pegar_permissao.closeEvent = self.Close_Event

        self.permissao = False

        pegar_permissao.exec_()

        
    def run(self):
        input_senha = pegar_permissao.lineEdit_senha.text()

        if PedirPermissao.verificar_senha(input_senha):
            self.permissao = True
            self.fecharJanela = "Sim"
            pegar_permissao.lineEdit_senha.clear()
            pegar_permissao.close()

        else:
            pegar_permissao.lineEdit_senha.clear()
            pegar_permissao.lineEdit_senha.setFocus()
            msg = QMessageBox(visualizar_grade)
            msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
            msg.setText(f'''Senha Invalida.''')
            msg.setIcon(QMessageBox. Warning)
            msg.setWindowTitle("Senha Invalida!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)  
            msg = msg.exec_()



    def verificar_senha(senha):
        
        id_usuario = cursor.execute(f"select ID from Usuario where Senha_Acesso = '{senha}'").fetchall()

        for i in range(len(id_usuario)):
            if cursor.execute(f"select Permitir_aos_outros_usuários from Acesso_Usuario where Id = {id_usuario[i][0]}").fetchall()[0][0] == 1:
                return True
        return False


    def return_answer(self):
        return self.permissao

    
    def Close_Event(self, event):
        if self.fecharJanela == "Sim":
            pass

        else:
            event.ignore()

    def Close_Event_Button(self):
      
        self.fecharJanela = "Sim"
        pegar_permissao.close()






class FuntionsThead(QtCore.QThread):

    signal_handler =  QtCore.pyqtSignal()

    def __init__(self, parent = None, function = None,signal_type = None):
        super(FuntionsThead,self).__init__(parent)
        self.signal_handler.connect(function)




# Create printer


def set_column():

    header = tela_admin.tableWidget_cadastrar.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)


  
    tela_vendas.tableWidget_vendas.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    tela_vendas.tableWidget_vendas.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
    header = tela_vendas.tableWidget_vendas.horizontalHeader()
    tela_vendas.tableWidget_vendas.setColumnWidth(0,150)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(2, 30)
    header.setSectionResizeMode(3, 50)
    header.setSectionResizeMode(4, 60)
   

    
    

    header2 = pesquisar_produtos.tableWidget_pes.horizontalHeader()
    header3 = pesquisar_produtos.tableWidget_pes.verticalHeader()  
    
    header2.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    header3.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
    


set_column()


def fazer_line_para_colocar_valor(line):
    texto = eval(f'{line}.text().replace(",",".")')
    try:
        if float(texto):
            pass
    except:
        text1= texto[:-1]
        eval(f"{line}.setText('{text1}')")
        return



#tela para imprimir

class ImprimirArquivo():

    def __init__(self, url = ""):

        self.url = url

        file = f"{c}\DataBase\Config.ini"
        config = ConfigParser()
        config.read(file)

        cur_impressora = config["Config_Impressao"]["impressora_cupom"]

        impressora = list(win32print.EnumPrinters(2))

        for i in range(len(impressora)):
            if str(cur_impressora) == str(impressora[i][2]):
                del impressora[i]
                tela_imprimir_arquivo.comboBox_lista_impressoras.addItem(f"{cur_impressora}")
                break


        for i in range(len(impressora)):
            tela_imprimir_arquivo.comboBox_lista_impressoras.addItem(impressora[i][2])



        tela_imprimir_arquivo.pushButton_imprimir.clicked.connect(self.imprimir)

        tela_imprimir_arquivo.exec()


    def imprimir(self):

        impressora = tela_imprimir_arquivo.comboBox_lista_impressoras.currentText()

        
        try:
            win32print.SetDefaultPrinterW(impressora)
            win32api.ShellExecute(0,"print",self.url,None,".",0)

        except:
            msg = QMessageBox()
            msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
            msg.setText(f'''algo Deu errado''')
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)  
            msg = msg.exec_()
            return



#tela para salvar arquivo

class SalvarArquivo:

    def __init__(self,url_arquivo = ""):

        self.url_arquivo = url_arquivo
        self.local_salvar = None
        self.output = None
        

        tela_salvar_arquivos.lineEdit_arquivo.setText(f"{self.url_arquivo}")

        tela_salvar_arquivos.toolButton.clicked.connect(self.set_save_local)
        tela_salvar_arquivos.pushButton.clicked.connect(self.salvar)

        tela_salvar_arquivos.exec_()

    def set_save_local(self):
        self.local_salvar = QtWidgets.QFileDialog.getExistingDirectory(tela_salvar_arquivos, 'Desktop')
        tela_salvar_arquivos.lineEdit_caminho_salvar.setText(f"{self.local_salvar}")
        

    def salvar(self):

        try:
            shutil.copy2(self.url_arquivo,self.local_salvar)
            msg = QMessageBox(tela_salvar_arquivos)
            msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
            msg.setText(f'''Salvo Com Sucesso.''')
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Salvo")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)  
            msg = msg.exec_()
            

        except TypeError:
            msg = QMessageBox(tela_salvar_arquivos)
            msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
            msg.setText(f''' insira um caminho.''')
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("erro")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)  
            msg = msg.exec_()
            return

        except FileNotFoundError:
            msg = QMessageBox(tela_salvar_arquivos)
            msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
            msg.setText(f''' arquivo não encontrado.''')
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("erro")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)  
            msg = msg.exec_()
            return

        except:
            msg = QMessageBox(tela_salvar_arquivos)
            msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
            msg.setText(f''' Algo deu errado.''')
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("erro")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)  
            msg = msg.exec_()
            return

        tela_salvar_arquivos.close()



