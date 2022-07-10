
import configparser
from load import *
from Core.Admin.Caixa.NFE import NFCE,final_requirements_to_finish_vendas
from Core.Admin.Caixa.cupom_recibo import Recibo




def only_int_codigo_vendas():
    texto = tela_vendas.lineEdit_codigo.text()
    widget.setCurrentIndex(0)
    if len(texto) == 0:
        return

    tela_vendas.label_codigo_invalido.setText("")



def only_int_quantidade_vendas():
    tela_vendas.label_codigo_invalido.clear()
    try:
        if int(tela_vendas.lineEdit_quantidade.text()):
            pass
    except:
        text = tela_vendas.lineEdit_quantidade.text()
        text1= text[:-1]
        text = tela_vendas.lineEdit_quantidade.setText(f"{text1}")
def only_int_desconto_vendas():
    tela_vendas.label_codigo_invalido.clear()
    try:
        if int(tela_vendas.lineEdit_desconto.text()):
            pass
    except:
        text = tela_vendas.lineEdit_desconto.text()
        text1= text[:-1]
        text = tela_vendas.lineEdit_desconto.setText(f"{text1}")

class AThread(QThread):

    def __init__(self, parent = None):
        super().__init__(parent=parent)



    def run(self):
        while produto.instancia == 0:
            time.sleep(0.2)
        #a quando a instancia não for mais 0, a tela de confirmação ira fechar
        confirmaçao.close()
        produto.instancia = 0

        widget.setCurrentIndex(widget.currentIndex()+2)


        #esse metodo ira preencher os dados de resulmo
        produto.go_to_resulmo()
        produto.resetar_classe()
        time.sleep(3.5)
        widget.setCurrentIndex(widget.currentIndex()-4)
        for i in range(0,10):
            tela_vendas.lineEdit_codigo.setFocus()



#adicionar produtos na tela de vendas

class produto:
    quantidade_produtos = 0
    quantidade_itens = 0
    desconto = "0%"
    total = 0.00
    totalBC = 0.00
    lis = []
    id_da_venda_atual = 0
    forma_de_pagamento = []
    troco = 0.00
    valor_recebido = []
    cur_quantidade = "x1"
    cur_desconto = "0%"
    editavel = True

    #parte de theard

    instancia = 0

    def __init__(self):
        self.codigo = ""
        self.nome = ""
        self.preço_total = 0.00
        self.preço_UN = 0.00
        self.quantidade = "x1"
        self.desconto_UN = "0%"
        #colocar essa instancia em uma lista
        produto.lis.append(self)




    def keyPressCodigo(event):



        key = event.text()
        codigo = tela_vendas.lineEdit_codigo.text().replace("'","").replace('"',"")

        if event.key() ==  Qt.Key_Return  and codigo != "":


            #se quiser adicionar quantidade
            if codigo[-1] == "*":
                codigo = codigo[:-1]
                if codigo == "":
                    return
                try:
                    #verificar se o numero é int
                    codigo =  int(codigo)

                    #verificar se a quantidade é maior que 3 digitos
                    if len(str(codigo)) > 3:
                        tela_vendas.lineEdit_codigo.setText("Quantidade Invalida.")
                        produto.editavel = True
                        return

                    tela_vendas.lineEdit_quantidade.setText(f"x{codigo}")
                    produto.cur_quantidade = f"x{codigo}"
                    tela_vendas.lineEdit_codigo.setText("Insira Um Codigo.")
                    produto.editavel = True
                    return

                except ValueError:

                    tela_vendas.lineEdit_codigo.setText("Comando Inválido.")
                    produto.editavel = True
                    return


        

            #se quiser remover algum produto
            elif codigo[0] == "*" and codigo[1] == "*":

                produto.cancelarProdutos()
                tela_vendas.lineEdit_codigo.setText("Insira Um Codigo.")
                produto.editavel = True
                return

            try:
                #se quiser adicionar desconto
                if codigo[-1] == "/" and codigo[-2] != "/":

                    codigo = codigo[:-1]
                    if codigo == "":
                        return
                    try:
                        #verificar se o numero é int
                        codigo =  int(codigo)

                        #verificar se a dsconto é maior que 3 digitos
                        if len(str(codigo)) > 3:
                            tela_vendas.lineEdit_codigo.setText("Invalido.")
                            produto.editavel = True
                            return

                        if codigo > 100 or codigo < 0:
                            tela_vendas.lineEdit_codigo.setText("Invalido.")
                            produto.editavel = True
                            return


                        tela_vendas.lineEdit_desconto_ind.setText(f"{codigo}%")

                        produto.cur_desconto = f"{codigo}%"
                        tela_vendas.lineEdit_codigo.setText("Insira Um Codigo.")
                        produto.editavel = True
                        return

                    except ValueError:

                        tela_vendas.lineEdit_codigo.setText("Comando Inválido.")
                        produto.editavel = True
                        return

                 #adicionar desconto sobre o total
                elif codigo[-1] == "/" and codigo[-2] == "/":
                    codigo = codigo[:-2]
                    if codigo == "":
                        return
                    if int(codigo) < 0 or int(codigo) > 100:
                        tela_vendas.lineEdit_codigo.setText("Invalido")
                        produto.editavel = True
                        return
                    produto.desconto = f"{codigo}%"
                    produto.add_desconto_total()

                    tela_vendas.lineEdit__descontoo.setText(f"{str(produto.desconto)}")
                    tela_vendas.lineEdit_codigo.setText("Insira Um Codigo.")
                    produto.editavel = True
                    return

            except:
                return


            #adicionar na tabela

                #verificar se o codigo existe
                #retorna verdadeiro ou falso
            validacao = produto.verificar_codigo(codigo)

            if validacao == False:
                tela_vendas.lineEdit_codigo.setText("Código Invalido.")
                produto.editavel = True
                return

            #pega os valores do banco de dados
            valor = cursor.execute(f"select Nome, preco from Produtos where ID = {cursor.execute(f'select ID_Produtos from Codigo_Produtos where Codigo = {codigo}').fetchall()[0][0]}").fetchall()

            itens = produto()

            itens.codigo = codigo
            itens.nome = valor[0][0]
            itens.preço_UN = valor[0][1]

            #adiciona a quantidade para o produto
            itens.add_quantidade(str(itens.cur_quantidade).replace("x",""))

            #adiciona o desconto para o produto
            itens.add_desconto(str(produto.cur_desconto).replace("%",""))

            produto.add_tableWidget()

            tela_vendas.lineEdit_quantidade.setText("1x")
            tela_vendas.lineEdit_desconto_ind.setText("0%")
            tela_vendas.lineEdit__quantidade_itens.setText(f"{produto.quantidade_itens}")
            itens.add_total()
            itens.add_desconto_total()
            tela_vendas.lineEdit_codigo.setText(f"{itens.codigo}       {itens.nome}  {itens.quantidade} ")
            produto.cur_desconto = "0%"
            produto.cur_quantidade = "1x"

            #selecionar a ultima linha
            tela_vendas.tableWidget_vendas.selectRow(tela_vendas.tableWidget_vendas.rowCount()-1)
            produto.editavel = True


            return




            return


        if event.key() == Qt.Key_F2:
            file = f"{c}\DataBase\Config.ini"
            config = ConfigParser()
            config.read(file)

            if cursor.execute(f'select Registrar_Entrada_Do_Caixa from Acesso_usuario where id = {config["Caixa"]["id_funcionario"]}').fetchall()[0][0] != 1:
                
            
                while True:
                    permitido = PedirPermissao().return_answer()
                    
                    if permitido == True:
                        break

                    else:
                        widget.setCurrentIndex(3)
                        return
            registrar_entrada.show()
            return

        if event.key() == Qt.Key_F3:
            file = f"{c}\DataBase\Config.ini"
            config = ConfigParser()
            config.read(file)
            if cursor.execute(f'select Resgistrar_Saida_Do_Caixa from Acesso_usuario where id = {config["Caixa"]["id_funcionario"]}').fetchall()[0][0] != 1:
            
                while True:
                    permitido = PedirPermissao().return_answer()
                    
                    if permitido == True:
                        break

                    else:
                        widget.setCurrentIndex(3)
                        return
            resgistrar_saida.show()
            return

        if event.key() == Qt.Key_F4:
            file = f"{c}\DataBase\Config.ini"
            config = ConfigParser()
            config.read(file)
            if cursor.execute(f'select Consultar_Produtos from Acesso_usuario where id = {config["Caixa"]["id_funcionario"]}').fetchall()[0][0] != 1:
            
                while True:
                    permitido = PedirPermissao().return_answer()
                    
                    if permitido == True:
                        break

                    else:
                        return
            TelaViewProdutosNasVendas().execute()

            return



        # ir para a tela de sub_total
        if event.key() == Qt.Key_F10:
            ir_sub_total()
            return

        

        if event.key() == Qt.Key_F12:

            file = f"{c}\DataBase\Config.ini"
            config = ConfigParser()
            config.read(file)

            if cursor.execute(f'select Acesso_a_Tela_De_Gerenciamento_do_Caixa from Acesso_usuario where id = {config["Caixa"]["id_funcionario"]}').fetchall()[0][0] != 1:

                while True:
                    permitido = PedirPermissao().return_answer()
                    
                    if permitido == True:
                        break

                    else:
                        return


            id_caixa = config["Caixa"]["id"]
            gerenciamento_caixa.lineEdit_filtrar_vendas.clear()
            gerenciamento_caixa.lineEdit_filtrar_vendas.setVisible(False)
            gerenciamento_caixa.comboBox_filtrar_vendas.setCurrentIndex(0)
            gerenciamento_caixa.tableWidget_produtos_vendidos.setRowCount(0)

            data_abertura = cursor.execute(f"select data_abertura from caixa where id = {id_caixa}").fetchall()[0][0]
            hora_abertura = cursor.execute(f"select hora_abertura from caixa where id = {id_caixa}").fetchall()[0][0]

            gerenciamento_caixa.dateTimeEdit_filtrar_vendas_limite.setDateTime(QDateTime.currentDateTime()) 
            gerenciamento_caixa.dateTimeEdit_filtrar_vendas.setDateTime(QDateTime.fromString(f"{data_abertura} {hora_abertura}","yyyy-MM-dd HH:mm"))

            widget.setCurrentIndex(5)
            return

        if event.key() == Qt.Key_F1:
            fecha_caixar.show()
            return

        #se o usuario quiser a apagar o codigo
        if event.key() ==  Qt.Key_Backspace:
            tela_vendas.lineEdit_codigo.setText(f"{tela_vendas.lineEdit_codigo.text()[:-1]}")
            return

        #adicionar na line edit codigo
        tela_vendas.lineEdit_codigo.setText(f"{tela_vendas.lineEdit_codigo.text() +str(key)}")



    #verificar se o codigo existe
    @classmethod
    def verificar_codigo(cls,codigo):
        asp = "'"
        try:

            #buscar no banco de dados
            sql=f"select codigo from Codigo_Produtos where codigo = {asp+str(codigo)+asp}"
            cursor.execute(sql)
            dados = cursor.fetchall()
            # se codigo não esta cadastrado, o tamanho de "dados" sera 0
            # e será informado que o codigo não existe
            if len(dados) == 0:
                return False
            else:
                return True

        except:
            return

    #adcionar a quantidade
    def add_quantidade(self,quantidade):

        #preço total sera o resultado do preço UN x quantidade
        self.preço_total = float(self.preço_UN) * int(quantidade)
        #colocar a quantidade igual a quantidade dada pelo usuario
        self.quantidade = f"{quantidade}x"
        #adicionar quantidade de itens
        produto.quantidade_itens += int(quantidade)



    #adcionar desconto
    def add_desconto(self,desconto):

        #aplicar o desconto ao preço total
        self.preço_total = self.preço_total - (self.preço_total * int(desconto)/100)
        #atualizar o desconto
        self.desconto_UN = f"{desconto}%"



    #quando essa função é chamada, retorna os valores dessa instance

    def valores(self):
        #codigo    #nome   #preço un #quantidade   #desconto  #total
        return self.codigo, self.nome, str(format(float(self.preço_UN),".2f")).replace(".",","), self.quantidade,self.desconto_UN,str(format(float(self.preço_total),".2f")).replace(".",",")
    #adcionar na table widget

    @classmethod
    def add_tableWidget(cls):
        #adiciona itens na tableWidget
        index = len(produto.lis)
        tela_vendas.tableWidget_vendas.setRowCount(tela_vendas.tableWidget_vendas.rowCount()+1)


        u = str(index).zfill(3)

        for j in range(len(produto.lis[index-1].valores())):
            tela_vendas.tableWidget_vendas.setItem(index-1 ,j , QtWidgets.QTableWidgetItem(str(produto.lis[index-1].valores()[j])))
            tela_vendas.tableWidget_vendas.setVerticalHeaderItem(index-1, QtWidgets.QTableWidgetItem(str(u)))



        #adicionar quantidade de produtos
        produto.quantidade_produtos = tela_vendas.tableWidget_vendas.rowCount()
        tela_vendas.lineEdit__quantidade_produtos.setText(f"{produto.quantidade_produtos}")
        #just scrollToBotton
        tela_vendas.tableWidget_vendas.scrollToBottom()


    #calcula o valor total ainda sem o desconto
    def add_total(self):

        produto.total += float(self.preço_total)
        produto.totalBC += float(self.preço_total)

    #calcula o valor total com desconto. esse sera o "total final"
    @classmethod
    def add_desconto_total(cls):
        #total sera igual a o backup
        produto.total = produto.totalBC
        desconto = produto.desconto.replace("%","")
        #calcula a porcentagem sobre o total, que agora é igual ao backup
        produto.total = produto.total - (produto.total * int(desconto)/100)
        #adicionar o total na lineEdit
        tela_vendas.lineEdit__total.setText(f"{produto.total:.2f}".replace(".",","))

    #cancelar produtos
    @classmethod
    def cancelarProdutos(cls):
        #diminuir a quantidade de itens/produtos
        #esse "try" é usado para verificar se o iten existe,caso não exista, Return
        


        try:
            indice = int(tela_vendas.lineEdit_codigo.text()[2:]) - 1
            file = f"{c}\DataBase\Config.ini"
            config = ConfigParser()
            config.read(file)
            if cursor.execute(f'select Cancelar_Produtos from Acesso_usuario where id = {config["Caixa"]["id_funcionario"]}').fetchall()[0][0] != 1:
                while True:
                    permitido = PedirPermissao().return_answer()
                    
                    if permitido == True:
                        break

                    else:
                        return
        except:
            tela_vendas.lineEdit_codigo.setText("Digito invalido.")
            produto.editavel = True


        try:
            produto.quantidade_itens -= int(produto.lis[indice].quantidade.replace("x",""))
        except:
            tela_vendas.lineEdit_codigo.setText("Index Invalido.")
            produto.editavel = True
            return

        produto.quantidade_produtos -= 1

        #o total do backup é diminuido de acordo com valor do preço total da instancia
        produto.totalBC -= produto.lis[indice].preço_total


        #cancelar o produto
        fonte = QFont()
        fonte.setStrikeOut(True)

        tela_vendas.tableWidget_vendas.removeRow(indice)


        for j in range(len(produto.lis)):
            u = str(j+1).zfill(3)
            tela_vendas.tableWidget_vendas.setVerticalHeaderItem(j, QtWidgets.QTableWidgetItem(str(u)))


        #deleta a instancia da lista
        try:
            del produto.lis[indice]
        except:
            return




        tela_vendas.tableWidget_vendas.scrollToBottom()

        #chama o metodo da classe para colocar o novo total
        produto.add_desconto_total()

        #somente atualiza as linesEdits

        tela_vendas.lineEdit__total.setText(f"{produto.total:.2f}")
        tela_vendas.lineEdit__quantidade_itens.setText(f"{produto.quantidade_itens}")
        produto.quantidade_produtos = tela_vendas.tableWidget_vendas.rowCount()
        tela_vendas.lineEdit__quantidade_produtos.setText(f"{produto.quantidade_produtos}")
        tela_remover.close()


    @classmethod
    def resetar_classe(cls):
        produto.quantidade_produtos = 0
        produto.quantidade_itens = 0
        produto.desconto = "0%"
        produto.total = 0.00
        produto.totalBC = 0.00
        produto.lis = []
        produto.id_da_venda_atual = 0
        produto.forma_de_pagamento = []
        produto.troco = 0.00
        produto.valor_recebido = []
        produto.cur_quantidade = "x1"
        produto.cur_desconto = "0%"
        produto.editavel = True


    @classmethod
    def set_focus(cls):
        for i in range(200):
            time.sleep(0.2)
            tela_vendas.lineEdit_codigo.setFocus()


    @classmethod
    def emitir_nfce(cls):


        nfc = NFCE()

        for i in range(len(produto.lis)):


            fiscal = cursor.execute(f"select ID_Produtos from Codigo_Produtos where Codigo = {produto.lis[i].valores()[0]}").fetchall()[0][0]
            fiscal = cursor.execute(f"select NCM,Icms_Origem,Unidade from Fiscal_Produtos where ID_Produtos = {fiscal}").fetchall()[0]
            preco_total = float(produto.lis[i].preço_UN) * float(produto.lis[i].quantidade.replace("x",""))
            desconto_un = preco_total - (preco_total * float(produto.lis[i].desconto_UN.replace("%",""))/100)

            temp = preco_total - desconto_un

            desconto_t = desconto_un - (desconto_un * float(produto.desconto.replace("%",""))/100)

            desconto_un = (desconto_un - desconto_t) + temp

            #codigo    #nome   #preço un #quantidade   #desconto  #total
            nfc.add_itens(codigo = produto.lis[i].valores()[0],descricao =produto.lis[i].valores()[1],ncm = fiscal[0] ,valor_desconto = desconto_un,quantidade =produto.lis[i].quantidade.replace("x","") ,valor = produto.lis[i].preço_UN,valor_bruto = preco_total,unidade=fiscal[2],icms_origem=fiscal[1] )


        for i in range(len(produto.valor_recebido)):
            nfc.set_pagamentos(produto.forma_de_pagamento[i][1],produto.valor_recebido[i],"")



        nfc.emitir_nfce(str(produto.troco).replace(",","."),fuction_error = NFCE.chamar_menssagem)

        return

        # tela_vendas.lineEdit_codigo.clear()
        # tela_sub_total.lineEdit_valor.clear()
        # tela_sub_total.lineEdit_troco.clear()
        # tela_sub_total.tableWidget.clearContents()
        # tela_vendas.tableWidget_vendas.clearContents()
        # tela_vendas.tableWidget_vendas.setRowCount(0)
        # tela_vendas.lineEdit__quantidade_itens.setText("0")
        # tela_vendas.lineEdit__quantidade_produtos.setText("0")
        # tela_vendas.lineEdit__descontoo.setText("0%")
        # tela_vendas.lineEdit__total.setText("0.00")



        #esse metodo ira preencher os dados de resulmo
        produto.resetar_classe()
        #tela_sub_total.lineEdit_diminuir.setText(f"{num}")



    @classmethod
    def go_to_resulmo(cls):
        pass
        #preecher os dados de resulmo
        # total_recebido_resulmo = float(produto.valor_recebido)
        # resumo_operacao.label_valor_total.setText(f"R${produto.total:.2f}")
        # resumo_operacao.label_metodo_pagamento.setText(f"-{produto.forma_de_pagamento}")
        # resumo_operacao.label_pagamento_valor.setText(f"R${total_recebido_resulmo:.2f}")
        # resumo_operacao.label_total_recebido.setText(f"R${total_recebido_resulmo:.2f}")
        # resumo_operacao.label_troco.setText(f"R${produto.troco:.2f}")




def tela_de_desconto():
    tela_vendas.label_codigo_invalido.clear()
    tela_desconto.lineEdit.setFocus()
    tela_desconto.show()


def only_int_desconto():
    tela_vendas.label_codigo_invalido.clear()
    try:
        if int(tela_desconto.lineEdit.text()):
            pass
    except:
        text = tela_desconto.lineEdit.text()
        text1= text[:-1]
        text = tela_desconto.lineEdit.setText(f"{text1}")


def add_desconto():


    desconto = tela_desconto.lineEdit.text()

    if desconto == "":
        desconto = 0

    produto.desconto = f"{desconto}%"
    produto.add_desconto_total()

    tela_vendas.lineEdit__total.setText(f"{produto.total:.2f}")
    tela_vendas.lineEdit__descontoo.setText(f"{str(produto.desconto)}")
    tela_desconto.hide()
    #



    #cancelar produtos


#cancelar produtos

def tela_cancelar():
    tela_vendas.label_codigo_invalido.clear()
    tela_remover.show()

def only_int_cancelar():
    tela_vendas.label_codigo_invalido.clear()
    try:
        if int(tela_remover.lineEdit.text()):
            pass
    except:
        text = tela_remover.lineEdit.text()
        text1= text[:-1]
        text = tela_remover.lineEdit.setText(f"{text1}")

def cancelar_produtos():

    if tela_remover.lineEdit.text() == "":
            return

    indice= int(tela_remover.lineEdit.text())

    indice = indice - 1

    produto.cancelarProdutos(indice)
    return

#pesquisar produtos

def tela_pesquisar():
    tela_vendas.label_codigo_invalido.clear()
    pesquisar_produtos.show()
    cursor.execute("select Codigo,Nome,Quantidade_total,Tamanho,Preco,Marca from produtos_estoque")
    dados_lidos = cursor.fetchall()


    pesquisar_produtos.tableWidget_pes.setRowCount(len(dados_lidos))
    pesquisar_produtos.tableWidget_pes.setColumnCount(6)


    for i in range(0, len(dados_lidos)):
        for j in range(0,6):
            pesquisar_produtos.tableWidget_pes.setItem(i,j , QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def pesquisar_produtos_vendas():
    tela_vendas.label_codigo_invalido.clear()
    filtro = pesquisar_produtos.comboBox.currentText()

    pesquisa = pesquisar_produtos.lineEdit.text()
    por = "%"
    asp = "'"
    chave = asp+por+pesquisa+por+asp

    if filtro == "Codigo":
        sql=f"select Codigo,Nome,Quantidade_total,Tamanho,preco,Marca from produtos_estoque where codigo like {chave};"

        cursor.execute(sql)
        dados_lidos = cursor.fetchall()


        pesquisar_produtos.tableWidget_pes.setRowCount(len(dados_lidos))
        pesquisar_produtos.tableWidget_pes.setColumnCount(6)


        for i in range(0, len(dados_lidos)):
            for j in range(0,6):
                pesquisar_produtos.tableWidget_pes.setItem(i,j , QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        return
    if filtro == "Produto":
        sql=f"select Codigo,Nome,Quantidade_total,Tamanho,preco,Marca from produtos_estoque where Nome like {chave};"

        cursor.execute(sql)
        dados_lidos = cursor.fetchall()


        pesquisar_produtos.tableWidget_pes.setRowCount(len(dados_lidos))
        pesquisar_produtos.tableWidget_pes.setColumnCount(6)


        for i in range(0, len(dados_lidos)):
            for j in range(0,6):
                pesquisar_produtos.tableWidget_pes.setItem(i,j , QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        return
    if filtro == "Marca":
        sql=f"select Codigo,Nome,Quantidade_total,Tamanho,preco,Marca from produtos_estoque where Marca like {chave};"

        cursor.execute(sql)
        dados_lidos = cursor.fetchall()


        pesquisar_produtos.tableWidget_pes.setRowCount(len(dados_lidos))
        pesquisar_produtos.tableWidget_pes.setColumnCount(6)


        for i in range(0, len(dados_lidos)):
            for j in range(0,6):
                pesquisar_produtos.tableWidget_pes.setItem(i,j , QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        return
    if filtro == "Tamanho":
        sql=f"select Codigo,Nome,Quantidade_total,Tamanho,preco,Marca from produtos_estoque where Tamanho like {chave};"

        cursor.execute(sql)
        dados_lidos = cursor.fetchall()


        pesquisar_produtos.tableWidget_pes.setRowCount(len(dados_lidos))
        pesquisar_produtos.tableWidget_pes.setColumnCount(6)


        for i in range(0, len(dados_lidos)):
            for j in range(0,6):
                pesquisar_produtos.tableWidget_pes.setItem(i,j , QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        return
    if filtro == "Quantidade":
        sql=f"select Codigo,Nome,Quantidade_total,Tamanho,preco,Marca from produtos_estoque where Quantidade_total like {chave};"

        cursor.execute(sql)
        dados_lidos = cursor.fetchall()


        pesquisar_produtos.tableWidget_pes.setRowCount(len(dados_lidos))
        pesquisar_produtos.tableWidget_pes.setColumnCount(6)


        for i in range(0, len(dados_lidos)):
            for j in range(0,6):
                pesquisar_produtos.tableWidget_pes.setItem(i,j , QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        return
    if filtro == "Preço":

        sql=f"select Codigo,Nome,Quantidade_total,Tamanho,preco,Marca from produtos_estoque where Preco like {chave};"

        cursor.execute(sql)
        dados_lidos = cursor.fetchall()


        pesquisar_produtos.tableWidget_pes.setRowCount(len(dados_lidos))
        pesquisar_produtos.tableWidget_pes.setColumnCount(6)


        for i in range(0, len(dados_lidos)):
            for j in range(0,6):
                pesquisar_produtos.tableWidget_pes.setItem(i,j , QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        return

def ir_sub_total():
    resumo_operacao.listWidget_metodo_pagamento.clear()
    resumo_operacao.listWidget_valores_recebidos.clear()
    tela_sub_total.listWidget_pagamento.clear()
    tela_vendas.label_codigo_invalido.clear()

    tela_sub_total.lineEdit_desconto.setText(f"{str(produto.desconto)}")
    tela_sub_total.lineEdit_qtdprodutos.setText(str(produto.quantidade_produtos))
    tela_sub_total.lineEdit_qtditens.setText(str(produto.quantidade_itens))
    tela_sub_total.lineEdit_total.setText(f"{produto.total:.2f}")
    tela_sub_total.comboBox.setCurrentIndex(0)
    tela_sub_total.tableWidget.setRowCount(0)

    tela_sub_total.tableWidget.setRowCount(len(produto.lis))
    tela_sub_total.tableWidget.setColumnCount(6)
    for i in range(0, len(produto.lis)):
        for j in range(0,6):
            tela_sub_total.tableWidget.setItem(i,j , QtWidgets.QTableWidgetItem(str(produto.lis[i].valores()[j])))

    tela_sub_total.label_troco.setText("FALTA A PAGAR:")
    tela_sub_total.lineEdit_troco.setText(f"-{format(produto.total,'.2f')}".replace(".",","))

    header = tela_sub_total.tableWidget.horizontalHeader()
    header1 = tela_sub_total.tableWidget.verticalHeader()

    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    header1.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    tela_sub_total.tableWidget.scrollToBottom()
    widget.setCurrentIndex(widget.currentIndex()+2)
    tela_sub_total.lineEdit_forma_de_pagamento.setFocus()






def voltar_vendas_to_login():
    tela_vendas.label_codigo_invalido.clear()
    tela_sub_total.lineEdit_troco.setText("")
    tela_sub_total.lineEdit_valor.setText("")
    widget.setCurrentIndex(widget.currentIndex()+3)

def finalizar_venda():
    

    #se não tem nada para vender, não deixar vender
    if len(produto.lis) == 0:
        return


    #verificar se valor é menor que o total

    troco = 0
    for i in range(len(produto.valor_recebido)):
        troco += float(produto.valor_recebido[i])
    troco -= float(produto.total)


    if float(troco) < 0:
        print("o valor nao pode ser menor que o total")
        return

    produto.troco = format(float(str(troco).replace(",",".")),".2f")


    #criar um id
    id = randint(100000000,999999999)
        #se por acaso o id gerado for igual ao algum id que ja tenha sido gerado
        #esse while loop ira criar um novo id
    while True:
            #verificar se existe um id igual no banco de dados
        cursor.execute(f"select * from produtos_vendidos where Id = {id}")
        dados = cursor.fetchall()
        if len(dados) == 0:
            break
        else:
            id = randint(100000000,999999999)

     #

    #o id da venda atual sera igual ao id gerado
    produto.id_da_venda_atual = id


    #essa verificação não faz sentido, só coloquei porque sim, nunca se sabe
    if tela_sub_total.lineEdit_valor.text() == "":
        pass
    else:
        produto.valor_recebido = format(float(tela_sub_total.lineEdit_valor.text()),".2f")

    #data e hora
    data_agora=datetime.datetime.now()
    data = data_agora.strftime("%Y-%m-%d")
    hora = data_agora.strftime("%H-%M-%S").replace("-",":")

    #adicionar no banco de dados

        #pegar o caixa atual

    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    id_caixa = config["Caixa"]["ID"]

    #inserir nos produtos vendidos                                    #id_caixa
    cursor.execute("insert into Venda values (?,?,?,?,?,?,?,?,?,?,?)", (id ,id_caixa,int(config["Caixa"]["id_funcionario"]),produto.quantidade_itens,produto.desconto,data,hora,format(float(str(produto.total).replace(",",".")),".2f"),format(float(str(produto.troco).replace(",",".")),"2f"),None,None))


    for i in range(len(produto.valor_recebido)):

        while True:
                id_pagamento = randint(10000000000,9999999999999)
                cursor.execute(f"select * from pagamento where ID = {id_pagamento}")
                dados = cursor.fetchall()

                if len(dados) == 0:
                    break
                else:
                    id_pagamento = randint(10000000000,9999999999999)



        if len(produto.forma_de_pagamento[i]) > 2:

            cursor.execute("insert into Pagamento values(?,?,?,?,?)" ,(id_pagamento,id,format(float(produto.valor_recebido[i]),".2f"),produto.forma_de_pagamento[i][0],f'{produto.forma_de_pagamento[i][2]}X'))
            continue

        cursor.execute("insert into Pagamento values(?,?,?,?,?)" ,(id_pagamento,id,format(float(produto.valor_recebido[i]),".2f"),produto.forma_de_pagamento[i][0],None))

    #inserir nas informaçoes dos produtos vendidos
    for i in range(len(produto.lis)):
        id_codigo = cursor.execute(f"select ID,ID_Produtos from Codigo_Produtos where Codigo = {produto.lis[i].valores()[0]}").fetchall()[0]
        id_produto = cursor.execute(f"select ID from Produtos where ID = {id_codigo[1]}").fetchall()[0][0]

                                                                                                                         #codigo    #nome   #preço un #quantidade   #desconto  #total
        cursor.execute("insert into produtos_vendidos values (?,?,?,?,?,?,?,?,?,?)", (id, id , id_codigo[0], id_produto, produto.lis[i].valores()[0], produto.lis[i].valores()[1], produto.lis[i].valores()[3], produto.lis[i].valores()[2], produto.lis[i].valores()[4], produto.lis[i].valores()[5]))

    #da baixa no estoque

    for i in range (len (produto.lis)):
        
        cursor.execute(f''' 

        update Codigo_Produtos set quantidade = max(quantidade - {str(produto.lis[i].valores()[3]).replace("x","")},0) where Codigo = {produto.lis[i].valores()[0]}       
        
        ''')

        ID_produtos = cursor.execute(f''' 

        select ID_Produtos from Codigo_Produtos where Codigo = {produto.lis[i].valores()[0]}       
        
        ''').fetchall()[0][0]

        cursor.execute(f'''
        
        update Produtos set qtd_itens = max( qtd_itens - {str(produto.lis[i].valores()[3]).replace("x","")},0) where id = {ID_produtos}
        
         ''')


    banco.commit()


    #criar cupom de vendas
    # fazer_cupom_trocas()
    # confirmaçao.show()

    confirmaçao.show()
    confirmaçao.label_menssagem.setText("Finalizando...")

    file = f"{c}\DataBase\config.ini"
    informaçoes = ConfigParser()
    informaçoes.read(file)

    #se a opção de emitr recibo esta ativa
    if f'{informaçoes["Caixa"]["emitir_recibo"]}' == "True":

        recibo  = Recibo(produto.quantidade_itens,produto.quantidade_produtos,f'{float(str(produto.total).replace(",",".")):.2f}'.replace(".",","),f'{float(str(produto.troco).replace(",",".")):.2f}'.replace(".",","),f"{produto.id_da_venda_atual}",produto.forma_de_pagamento,produto.valor_recebido,produto.desconto)

        for i in range(len(produto.lis)):
            #codigo    #nome   #preço un #quantidade   #desconto  #total
            recibo.add_itens(produto.lis[i].valores()[0],produto.lis[i].valores()[1],
            str(produto.lis[i].valores()[3]).replace("x",""),str(produto.lis[i].valores()[2]).replace(".",","),
            produto.lis[i].valores()[4],str(produto.lis[i].valores()[5]).replace(".",","))

        url = recibo.criar_recibo()

        #imprimir o recibo

        if informaçoes["Caixa"]["imprimir_recibo"] == "True":
            try:

                win32print.SetDefaultPrinterW(f'{informaçoes["Config_Impressao"]["impressora_cupom"]}')

                win32api.ShellExecute(0,"print",url,None,".",0)

            except:
                msg = QMessageBox(visualizar_grade)
                msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
                msg.setText(f'''algo Deu errado Ao imprimir o Recibo''')
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)
                msg = msg.exec_()



    #se a opção de emitir nfce esta ativa
    if f'{informaçoes["Caixa"]["emitir_nfce"]}' == "True":
        t1 = threading.Thread(target=produto.emitir_nfce)
        t1.setDaemon(True)
        t1.start()
        return


    widget.setCurrentIndex(2)


    final_requirements_to_finish_vendas()




    return







def aumentar_index():
    widget.setCurrentIndex(widget.currentIndex()+2)

def diminuir_index():
    widget.setCurrentIndex(widget.currentIndex()-4)
    tela_vendas.lineEdit_codigo.setFocus()
    tela_vendas.lineEdit_codigo.setFocus()
    tela_vendas.lineEdit_codigo.setFocus()
    """ i = randint(0,10000000000)
    tela_sub_total.lineEdit_setar.setText(f"{i}") """

def setar_focus():
    confirmaçao.close()


def fazer_cupom_trocas():
    data_agora=datetime.datetime.now()
    data = data_agora.strftime("%d-%m-%y").replace("-","/")
    hora = data_agora.strftime("%H-%M-%S").replace("-",":")



    cdir =os.getcwd()
    #logo loja moda do dia
    pdf = FPDF("p","mm",(80,280))
    pdf.set_left_margin(margin = 3)
    pdf.set_right_margin(margin = 3)
    pdf.set_top_margin(margin= 5)
    tim = "-"



    pdf.add_page()

    #informações sobre a loja

    #logo loja moda do dia
    pdf.set_font("helvetica","b",16,)
    pdf.cell(0,5,"LOJA MODA DO DIA",ln=True,align="C")

    #linha separadora
    pdf.set_font("helvetica","",8,)
    pdf.cell(0,5,f"{tim * 100}",ln=True,align="C")


    #endereço

    pdf.set_font("helvetica","",6,)
    pdf.cell(0,3,"AU DA COSTA SOUZA",ln=True,align="l")
    pdf.cell(0,3,"AV.CORACY NUNES, Centro,189 Geral Oiapoque",ln=True,align="l")
    pdf.cell(0,3,"Centro - OIAPOQUE- AP ",ln=True,align="l")
    pdf.cell(0,3,"cep:68.980-000  ",ln=True,align="l")
    pdf.cell(0,3,"Tel:  ",ln=True,align="l")
    pdf.cell(0,3,f"DATA: {data}  {hora}",ln=True,align="l")

    #colocar as categorias para o produto
    pdf.set_font("helvetica","",7,)
    pdf.cell(0,5,f"{tim * 100}",ln=True,align="C")
    pdf.cell(0,8,f"     Descrição               QTD        VALOR         DES     TOTAL",ln=True,align="l")
    pdf.cell(0,5,f"{tim * 120}",ln=True,align="C")


    #adicionar os produtos
    i = 0
    for i in range(len(produto.lis)):
            #fonte
        pdf.set_font("helvetica","",6)
        #não deixar o tamanho do nome ser muito alto

        if len(produto.lis[i].valores()[1]) > 21:
            li = produto.lis[i].valores()[1]
            dot = "."
            s = " "
            li = li[0:20]
            li = li + dot * 3
            produto.lis[i].nome = f"{li}"
            #nome
        pdf.cell(26,4,f"{produto.lis[i].valores()[1]}",align="L")
            #preparando a quantidade de itens
        quan = str(produto.lis[i].valores()[4].replace("x",""))
        quan = quan.zfill(3)
            #quantidade de itens
        pdf.cell(10,4,f"{quan}",align="L")
            #valor unitario do produto
        pdf.cell(15,4,f"{produto.lis[i].valores()[3]}",align="L")
            #desconto
        pdf.cell(8,4,f"{produto.lis[i].valores()[5]}",align="L")
            #valor total do produto
        pdf.cell(19,4,f"{produto.lis[i].valores()[2]}",ln=True,align="L")
        i += 1
        #linha para separar
    pdf.cell(0,5,f"{tim * 100}",ln=True,align="C")

    #final
        #   quantidade total de itens
    pdf.set_font("helvetica","B",7)
    pdf.cell(50,4,f"Qtd.Total de Itens",align="L")
    pdf.set_font("helvetica","",7)
    quantidade_produtos_total =str(produto.quantidade_produtos)
    quantidade_produtos_total = quantidade_produtos_total.zfill(3)
    pdf.cell(0,4,f"{quantidade_produtos_total}",ln=True,align="L")
        #   valor total
    pdf.set_font("helvetica","B",7)
    pdf.cell(50,4,f"Valor Total",align="L")
    pdf.set_font("helvetica","",7)
    pdf.cell(0,4,f"{produto.total:.2f}",ln=True,align="L")
    pdf.ln(5)
    total_recebido_resulmo = produto.valor_recebido[0]
    pdf.cell(50,4,f"Forma de Pagamento",align="L")
    pdf.cell(0,4,f"Valor Pago",ln=True,align="L")
    pdf.cell(50,4,f"-{produto.forma_de_pagamento}",align="L")
    pdf.cell(0,4,f"R${float(total_recebido_resulmo):.2f}",ln=True,align="L")
    pdf.cell(50,4,f"Troco",align="L")
    pdf.cell(0,4,f"{float(produto.troco):.2f}",ln=True,align="L")
    pdf.cell(0,4,f"ID:{produto.id_da_venda_atual}",ln=True,align="L")
    pdf.cell(0,5,f"{tim * 100}",ln=True,align="C")
    pdf.set_font("helvetica","b",8,)

    pdf.cell(0,4,"Recibo Para Troca",ln=True,align="C")
    pdf.ln(5)
    pdf.set_font("helvetica","b",7,)

    pdf.cell(0,4,"*Troca Somente Com a Etiqueta",ln=True,align="L")
    pdf.cell(0,4,"*O Produto Deve Estar Em Perfeito Estado",ln=True,align="L")
    pdf.cell(0,4,"*Apresentar Este Recibo ou Algun Documento Fiscal",ln=True,align="L")
    pdf.cell(0,4,"*Prazo em Apenas 3 Dias",ln=True,align="L")

    #colocar no final "sem valor fiscal" de cada nota
    pdf.set_font("helvetica","b",8,)
    pdf.cell(0,30,"-------SEM VALOR FISCAL-------",ln=True,align="C")

    pdf.output(fr"{cdir}\cupom_vendas\Recibos\{produto.id_da_venda_atual}.pdf")


    path = fr"{cdir}\cupom_vendas\Recibos\{produto.id_da_venda_atual}.pdf"


    lista = win32print.EnumPrinters(2)

    impressora = lista[5]


    win32print.SetDefaultPrinterW(impressora[2])


    win32api.ShellExecute(0, 'print',path ,None, '.', 0)


def ir_tela_resulmo_to_vendas():
    widget.setCurrentIndex(widget.currentIndex()-4)




#tela de visualizaçao de produtos


#visualizar_produtos_nas_vendas

class TelaViewProdutosNasVendas:

    dados = []

    def __init__(self):
        visualizar_produtos_nas_vendas.tableWidget_produtos.setRowCount(0)
        visualizar_produtos_nas_vendas.comboBox_filtrar.setCurrentIndex(0)
        visualizar_produtos_nas_vendas.lineEdit_pesquisar.clear()

        TelaViewProdutosNasVendas.pesquisar()
        visualizar_produtos_nas_vendas.tableWidget_produtos.setFocus()
        


    def execute(self):
        visualizar_produtos_nas_vendas.exec_()
        TelaViewProdutosNasVendas.dados.clear()
    @classmethod
    def pesquisar(cls):
        TelaViewProdutosNasVendas.dados.clear()
        visualizar_produtos_nas_vendas.tableWidget_produtos.setRowCount(0)
        combo = visualizar_produtos_nas_vendas.comboBox_filtrar.currentText()

        if combo == "Codigo":
            pesquisa = visualizar_produtos_nas_vendas.lineEdit_pesquisar.text()
            cursor.execute(f''' 
            select Codigo_Produtos.Codigo, Produtos.Nome ,  Produtos.qtd_itens ,  Produtos.preco, ifnull(Produtos.Marca,'SEM MARCA')
            from Codigo_Produtos
            join Produtos on Codigo_Produtos.ID_produtos = Produtos.ID 
            where Codigo_Produtos.Codigo like '%{pesquisa}%'
            ''')
        
        elif combo == "Descricao":
            pesquisa = visualizar_produtos_nas_vendas.lineEdit_pesquisar.text()
            cursor.execute(f''' 
            select Codigo_Produtos.Codigo, Produtos.Nome ,  Produtos.qtd_itens ,  Produtos.preco, ifnull(Produtos.Marca,'SEM MARCA')
            from Codigo_Produtos
            join Produtos on Codigo_Produtos.ID_produtos = Produtos.ID 
            where Produtos.Nome like '%{pesquisa}%'
            ''')
        elif combo == "Qtd":
            pesquisa = visualizar_produtos_nas_vendas.lineEdit_pesquisar.text()
            cursor.execute(f''' 
            select Codigo_Produtos.Codigo, Produtos.Nome ,  Produtos.qtd_itens ,  Produtos.preco, ifnull(Produtos.Marca,'SEM MARCA')
            from Codigo_Produtos
            join Produtos on Codigo_Produtos.ID_produtos = Produtos.ID 
            where Produtos.qtd_itens like '%{pesquisa}%'
            ''')
        elif combo == "Preco":
            pesquisa = visualizar_produtos_nas_vendas.lineEdit_pesquisar.text()
            cursor.execute(f''' 
            select Codigo_Produtos.Codigo, Produtos.Nome ,  Produtos.qtd_itens ,  Produtos.preco, ifnull(Produtos.Marca,'SEM MARCA')
            from Codigo_Produtos
            join Produtos on Codigo_Produtos.ID_produtos = Produtos.ID 
            where Produtos.preco like '%{pesquisa.replace(",",".")}%'
            ''')
        elif combo == "Marca":
            pesquisa = visualizar_produtos_nas_vendas.lineEdit_pesquisar.text()
            cursor.execute(f''' 
            select Codigo_Produtos.Codigo, Produtos.Nome ,  Produtos.qtd_itens ,  Produtos.preco, ifnull(Produtos.Marca,'SEM MARCA') as marca_produtos
            from Codigo_Produtos
            join Produtos on Codigo_Produtos.ID_produtos = Produtos.ID 
            where marca_produtos like '%{pesquisa}%'
            ''')

        
        TelaViewProdutosNasVendas.SetarTable()

    @classmethod
    def SetarTable(cls):
        needed = 15
 
        data = cursor.fetchmany(needed)

        TelaViewProdutosNasVendas.dados = data + TelaViewProdutosNasVendas.dados
        
        rowCount = visualizar_produtos_nas_vendas.tableWidget_produtos.rowCount()
        try:
            for i in range(0, needed):
                visualizar_produtos_nas_vendas.tableWidget_produtos.setRowCount(rowCount+i+1)
                for j in range(0, 5):
                    visualizar_produtos_nas_vendas.tableWidget_produtos.setItem(rowCount+i, j, QTableWidgetItem(str(data[i][j]).replace(".",",")))
            visualizar_produtos_nas_vendas.tableWidget_produtos.resizeColumnsToContents()
            return


        except IndexError:
            visualizar_produtos_nas_vendas.tableWidget_produtos.setRowCount( visualizar_produtos_nas_vendas.tableWidget_produtos.rowCount() - 1)
            visualizar_produtos_nas_vendas.tableWidget_produtos.resizeColumnsToContents()
            print("=====================")
            print("IndexError Because There is No Data to Get From Table")
            print("=====================")
            return

    @classmethod
    def setar_produtos(cls):
        
        row = visualizar_produtos_nas_vendas.tableWidget_produtos.currentRow()
        print(row)
        if not visualizar_produtos_nas_vendas.tableWidget_produtos.hasFocus() or row == -1:
            print("row esta fora")
            return
        print(TelaViewProdutosNasVendas.dados)
        codigo = TelaViewProdutosNasVendas.dados[row][0]

        visualizar_produtos_nas_vendas.close()
        validacao = produto.verificar_codigo(codigo)

        if validacao == False:
            tela_vendas.lineEdit_codigo.setText("Código Invalido.")
            produto.editavel = True
            return

        #pega os valores do banco de dados
        valor = cursor.execute(f"select Nome, preco from Produtos where ID = {cursor.execute(f'select ID_Produtos from Codigo_Produtos where Codigo = {codigo}').fetchall()[0][0]}").fetchall()

        itens = produto()

        itens.codigo = codigo
        itens.nome = valor[0][0]
        itens.preço_UN = valor[0][1]

        #adiciona a quantidade para o produto
        itens.add_quantidade(str(itens.cur_quantidade).replace("x",""))

        #adiciona o desconto para o produto
        itens.add_desconto(str(produto.cur_desconto).replace("%",""))

        produto.add_tableWidget()

        tela_vendas.lineEdit_quantidade.setText("1x")
        tela_vendas.lineEdit_desconto_ind.setText("0%")
        tela_vendas.lineEdit__quantidade_itens.setText(f"{produto.quantidade_itens}")
        itens.add_total()
        itens.add_desconto_total()
        tem = f"{itens.codigo}       {itens.nome}  {itens.quantidade}"
        print(tem)
        tela_vendas.lineEdit_codigo.setText(tem)
        produto.cur_desconto = "0%"
        produto.cur_quantidade = "1x"

        #selecionar a ultima linha
        tela_vendas.tableWidget_vendas.selectRow(tela_vendas.tableWidget_vendas.rowCount()-1)
        produto.editavel = True
       

visualizar_produtos_nas_vendas.tableWidget_produtos.itemClicked.connect(TelaViewProdutosNasVendas.setar_produtos)


visualizar_produtos_nas_vendas.pushButton_enter.clicked.connect(TelaViewProdutosNasVendas.setar_produtos)





