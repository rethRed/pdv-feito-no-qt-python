from load import *
from .tela_vendas import produto,finalizar_venda





def sub_total_KeyPress(event):
    if event.key() == Qt.Key_F10:
        finalizar_venda()
        return


def inserir_valor():
    tela_vendas.label_codigo_invalido.clear()
    #pega o valor dado pelo cliente
    valor = tela_sub_total.lineEdit_valor.text().replace(",",".")

    if valor == "":
        troco = 0.00
        for i in range(len(produto.valor_recebido)):
            troco += float(produto.valor_recebido[i])
        troco -= float(produto.total)

        if troco >= 0:
            tela_sub_total.label_troco.setText("TROCO:")

        else:
            tela_sub_total.label_troco.setText("FALTA A PAGAR:")

            
        tela_sub_total.lineEdit_troco.setText(f'{str(format(troco,".2f")).replace(".",",")}')
        return


    #verifica se o valor é float, se não é, Return
    try:
        if float(tela_sub_total.lineEdit_valor.text().replace(",",".")):
            pass
    except:
        text = tela_sub_total.lineEdit_valor.text()
        text1= text[:-1]
        text = tela_sub_total.lineEdit_valor.setText(f"{text1}".replace(".",","))
        return

    #reseta o valor do troco para 0
    troco = 0

    #calcula o valor do troco
    for i in range(len(produto.valor_recebido)):
        troco += float(produto.valor_recebido[i])
    troco += float(valor)
    troco -= float(produto.total)


    
    #não deixar o valor do troco ser menor que 0
    if troco < 0:
        tela_sub_total.label_troco.setText("FALTA A PAGAR:")
    
    else:
        tela_sub_total.label_troco.setText("TROCO:")

    #setar o texto da lineEdit = ao troco
    tela_sub_total.lineEdit_troco.setText(f"{troco:.2f}".replace(".",","))




def voltar_tela_vendas():
    tela_sub_total.lineEdit_troco.setText("")
    tela_sub_total.lineEdit_valor.setText("")
    widget.setCurrentIndex(widget.currentIndex()-2)


def adicionar_pagamento():
    
    index = tela_sub_total.comboBox.currentIndex()

    if index == 0:
        return

    elif index == 1:
        
        #se  o usuario colocar apertar o valor sem colocar o preço , isso vai auto completar o preço restante
        if tela_sub_total.lineEdit_valor.text() == "":
            if float(tela_sub_total.lineEdit_troco.text().replace(",",".")) < 0:
                tela_sub_total.lineEdit_valor.setText(f"{format(abs(float(tela_sub_total.lineEdit_troco.text().replace(',','.'))),'.2f')}".replace(".",","))
                return
            return
        produto.forma_de_pagamento.append(["DINHEIRO",1])
        produto.valor_recebido.append(f'{tela_sub_total.lineEdit_valor.text().replace(",",".")}')
        tela_sub_total.listWidget_pagamento.addItem(f'DINHEIRO R$ {str(format(float(tela_sub_total.lineEdit_valor.text().replace(",",".")),".2f")).replace(".",",")}')
        tela_sub_total.lineEdit_valor.setText("")
        tela_sub_total.lineEdit_forma_de_pagamento.clear()
        tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
        tela_sub_total.comboBox.setCurrentIndex(0)
        tela_sub_total.listWidget_pagamento.scrollToBottom()
        return

    elif index == 2:
        #se  o usuario colocar apertar o valor sem colocar o preço , isso vai auto completar o preço restante
        if tela_sub_total.lineEdit_valor.text() == "":
            if float(tela_sub_total.lineEdit_troco.text().replace(",",".")) < 0:
                tela_sub_total.lineEdit_valor.setText(f"{format(abs(float(tela_sub_total.lineEdit_troco.text().replace(',','.'))),'.2f')}".replace(".",","))
                return
            return
        produto.forma_de_pagamento.append(["CHEQUE",2])
        produto.valor_recebido.append(f'{tela_sub_total.lineEdit_valor.text().replace(",",".")}')
        tela_sub_total.listWidget_pagamento.addItem(f'CHEQUE R$ {str(format(float(tela_sub_total.lineEdit_valor.text().replace(",",".")),".2f")).replace(".",",")}')
        tela_sub_total.lineEdit_valor.setText("")
        tela_sub_total.lineEdit_forma_de_pagamento.clear()
        tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
        tela_sub_total.comboBox.setCurrentIndex(0)
        tela_sub_total.listWidget_pagamento.scrollToBottom()
        return


    elif index == 3:

        #se  o usuario colocar apertar o valor sem colocar o preço , isso vai auto completar o preço restante
        if tela_sub_total.lineEdit_valor.text() == "":

            if float(tela_sub_total.lineEdit_troco.text().replace(",",".")) < 0:
                tela_sub_total.lineEdit_valor.setText(f"{format(abs(float(tela_sub_total.lineEdit_troco.text().replace(',','.'))),'.2f')}".replace(".",","))
                return
            return

        parcelas = tela_sub_total.lineEdit_parcelas.text()
        try:
            if int(parcelas) not in range(1,25):
                return

        except ValueError:
            parcelas = 1

        produto.forma_de_pagamento.append(["CARTÃO DE CRÉDITO",3,parcelas])
        produto.valor_recebido.append(f'{tela_sub_total.lineEdit_valor.text().replace(",",".")}')
        tela_sub_total.listWidget_pagamento.addItem(f'Cartão de Crédito R$ {str(format(float(tela_sub_total.lineEdit_valor.text().replace(",",".")),".2f")).replace(".",",")}/   {parcelas}X')
        tela_sub_total.lineEdit_valor.setText("")
        tela_sub_total.lineEdit_forma_de_pagamento.clear()
        tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
        tela_sub_total.comboBox.setCurrentIndex(0)
        tela_sub_total.lineEdit_parcelas.setVisible(False)
        tela_sub_total.label_parcelas.setVisible(False)
        tela_sub_total.lineEdit_parcelas.clear()
        tela_sub_total.listWidget_pagamento.scrollToBottom()
        return


    elif index == 4:
        #se  o usuario colocar apertar o valor sem colocar o preço , isso vai auto completar o preço restante
        if tela_sub_total.lineEdit_valor.text() == "":
            if float(tela_sub_total.lineEdit_troco.text().replace(",",".")) < 0:
                tela_sub_total.lineEdit_valor.setText(f"{format(abs(float(tela_sub_total.lineEdit_troco.text().replace(',','.'))),'.2f')}".replace(".",","))
                return
            return
        produto.forma_de_pagamento.append(["CARTÃO DE DÉBITO",4])
        produto.valor_recebido.append(f'{tela_sub_total.lineEdit_valor.text().replace(",",".")}')
        tela_sub_total.listWidget_pagamento.addItem(f'CARTÃO DE DÉBITO R$ {str(format(float(tela_sub_total.lineEdit_valor.text().replace(",",".")),".2f")).replace(".",",")}')
        tela_sub_total.lineEdit_valor.setText("")
        tela_sub_total.lineEdit_forma_de_pagamento.clear()
        tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
        tela_sub_total.comboBox.setCurrentIndex(0)
        tela_sub_total.listWidget_pagamento.scrollToBottom()
        return


    elif index == 5:
        if tela_sub_total.lineEdit_valor.text() == "":
            if float(tela_sub_total.lineEdit_troco.text().replace(",",".")) < 0:
                tela_sub_total.lineEdit_valor.setText(f"{format(abs(float(tela_sub_total.lineEdit_troco.text().replace(',','.'))),'.2f')}".replace(".",","))
                return
            return
        produto.forma_de_pagamento.append(["Crédito Loja",10])
        produto.valor_recebido.append(f'{tela_sub_total.lineEdit_valor.text().replace(",",".")}')
        tela_sub_total.listWidget_pagamento.addItem(f'Crédito Loja R$ {str(format(float(tela_sub_total.lineEdit_valor.text().replace(",",".")),".2f")).replace(".",",")}')
        tela_sub_total.lineEdit_valor.setText("")
        tela_sub_total.lineEdit_forma_de_pagamento.clear()
        tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
        tela_sub_total.comboBox.setCurrentIndex(0)
        tela_sub_total.listWidget_pagamento.scrollToBottom()
        return
    
    elif index == 6:
        if tela_sub_total.lineEdit_valor.text() == "":
            if float(tela_sub_total.lineEdit_troco.text().replace(",",".")) < 0:
                tela_sub_total.lineEdit_valor.setText(f"{format(abs(float(tela_sub_total.lineEdit_troco.text().replace(',','.'))),'.2f')}".replace(".",","))
                return
            return
        produto.forma_de_pagamento.append(["PIX",99])
        produto.valor_recebido.append(f'{tela_sub_total.lineEdit_valor.text().replace(",",".")}')
        tela_sub_total.listWidget_pagamento.addItem(f'PIX R$ {str(format(float(tela_sub_total.lineEdit_valor.text().replace(",",".")),".2f")).replace(".",",")}')
        tela_sub_total.lineEdit_valor.setText("")
        tela_sub_total.lineEdit_forma_de_pagamento.clear()
        tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
        tela_sub_total.comboBox.setCurrentIndex(0)
        tela_sub_total.listWidget_pagamento.scrollToBottom()
        return

    elif index == 7:
        if tela_sub_total.lineEdit_valor.text() == "":
            if float(tela_sub_total.lineEdit_troco.text().replace(",",".")) < 0:
                tela_sub_total.lineEdit_valor.setText(f"{format(abs(float(tela_sub_total.lineEdit_troco.text().replace(',','.'))),'.2f')}".replace(".",","))
                return
            return
        produto.forma_de_pagamento.append(["Vale Presente",13])
        produto.valor_recebido.append(f'{tela_sub_total.lineEdit_valor.text().replace(",",".")}')
        tela_sub_total.listWidget_pagamento.addItem(f'Vale Presente R$ {str(format(float(tela_sub_total.lineEdit_valor.text().replace(",",".")),".2f")).replace(".",",")}')
        tela_sub_total.lineEdit_valor.setText("")
        tela_sub_total.lineEdit_forma_de_pagamento.clear()
        tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
        tela_sub_total.comboBox.setCurrentIndex(0)
        tela_sub_total.listWidget_pagamento.scrollToBottom()
        return

    elif index == 8:
        if tela_sub_total.lineEdit_valor.text() == "":
            if float(tela_sub_total.lineEdit_troco.text().replace(",",".")) < 0:
                tela_sub_total.lineEdit_valor.setText(f"{format(abs(float(tela_sub_total.lineEdit_troco.text().replace(',','.'))),'.2f')}".replace(".",","))
                return
            return
        produto.forma_de_pagamento.append(["Outros",99])
        produto.valor_recebido.append(f'{tela_sub_total.lineEdit_valor.text().replace(",",".")}')
        tela_sub_total.listWidget_pagamento.addItem(f'Outros R$ {str(format(float(tela_sub_total.lineEdit_valor.text().replace(",",".")),".2f")).replace(".",",")}')
        tela_sub_total.lineEdit_valor.setText("")
        tela_sub_total.lineEdit_forma_de_pagamento.clear()
        tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
        tela_sub_total.comboBox.setCurrentIndex(0)
        tela_sub_total.listWidget_pagamento.scrollToBottom()
        return










def forma_pagamento():

    tela_sub_total.lineEdit_valor.clear()

    combo = tela_sub_total.comboBox.currentText()
    index = str(tela_sub_total.comboBox.currentIndex())
    forma = tela_sub_total.lineEdit_forma_de_pagamento.text()

    if int(index) < 9:
        index = index.zfill(3)
    elif int(index)>10:
        index = index.zfill(3)


    if combo == "Dinheiro":
        if int(index) == 0:
            tela_sub_total.lineEdit_forma_de_pagamento.clear()
            return
        tela_sub_total.lineEdit_forma_de_pagamento.setText(str(index))
        return
    else:

        if int(index) == 0:
            tela_sub_total.lineEdit_forma_de_pagamento.clear()
            return
        tela_sub_total.lineEdit_forma_de_pagamento.setText(str(index))
        return



def only_int_forma_de_pagamento():
    
    try:
        if int(tela_sub_total.lineEdit_forma_de_pagamento.text()):
            pass
    except:
        text = tela_sub_total.lineEdit_forma_de_pagamento.text()
        text1= text[:-1]
        text = tela_sub_total.lineEdit_forma_de_pagamento.setText(f"{text1}")



def inserir_forma_pagamento():




    forma_de_pagamento = tela_sub_total.lineEdit_forma_de_pagamento.text()

    #verificar se forma_de_pagameto esta vazia
    if forma_de_pagamento == "":
        return

    #apagar metodos de pagamentos
    if len(str(forma_de_pagamento)) > 2:
        if str(forma_de_pagamento)[0] == "1" and str(forma_de_pagamento)[1] == "1":
            index = int(str(forma_de_pagamento)[-1]) - 1
            if index == -1:
                tela_sub_total.lineEdit_forma_de_pagamento.clear()
                tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
                return

            try:
                tela_sub_total.listWidget_pagamento.takeItem(index)
                del produto.forma_de_pagamento[index]
                del produto.valor_recebido[index]

            except IndexError:
                tela_sub_total.lineEdit_forma_de_pagamento.clear()
                tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
                return
            inserir_valor()
            tela_sub_total.lineEdit_forma_de_pagamento.clear()
            tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
            return




    #formatar o numero para colocar zero no inicio
    forma_de_pagamento = forma_de_pagamento.zfill(3)

    #mudar a line edit para o texto formatado
    tela_sub_total.lineEdit_forma_de_pagamento.setText(forma_de_pagamento)

    #mudar a forma de pagamento no comboBox
   
    tela_sub_total.comboBox.setCurrentIndex(int(forma_de_pagamento))
        #verificar se o index é valido
    texto_comboBox = tela_sub_total.comboBox.currentText()
    if texto_comboBox == "":
        tela_sub_total.comboBox.setCurrentIndex(0)
        tela_sub_total.lineEdit_forma_de_pagamento.clear()
        tela_sub_total.lineEdit_forma_de_pagamento.setFocus()
        tela_sub_total.lineEdit_parcelas.setVisible(False)
        tela_sub_total.label_parcelas.setVisible(False)
        return

    if tela_sub_total.comboBox.currentIndex() == 3:
        tela_sub_total.lineEdit_parcelas.setVisible(True)
        tela_sub_total.label_parcelas.setVisible(True)

    else:
        tela_sub_total.lineEdit_parcelas.setVisible(False)
        tela_sub_total.label_parcelas.setVisible(False)
    tela_sub_total.lineEdit_valor.setFocus()

