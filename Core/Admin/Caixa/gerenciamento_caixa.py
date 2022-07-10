from load import *


# #essa é só de only int or float
# def to_vendas():
#     widget.setCurrentIndex(0)

# def ncm_only_int():
#     gerenciamento_caixa.label_menssagem.setText("")

#     try:
#         if int(gerenciamento_caixa.lineEdit_ncm.text()):
#             pass
#     except:
#         text = gerenciamento_caixa.lineEdit_ncm.text()
#         text1= text[:-1]
#         text = gerenciamento_caixa.lineEdit_ncm.setText(f"{text1}")


# def icms_origem_only_int():
#     gerenciamento_caixa.label_menssagem.setText("")

#     try:
#         if int(gerenciamento_caixa.lineEdit_icms_origem.text()):
#             pass
#     except:
#         text = gerenciamento_caixa.lineEdit_icms_origem.text()
#         text1= text[:-1]
#         text = gerenciamento_caixa.lineEdit_icms_origem.setText(f"{text1}")


# def codigo_produto_only_int():
#     gerenciamento_caixa.label_menssagem.setText("")


# def descriçao_only_int():
#     gerenciamento_caixa.label_menssagem.setText("")


# def preco_only_float():
#     gerenciamento_caixa.label_menssagem.setText("")

#     try:
#         if float(gerenciamento_caixa.lineEdit_preco.text()):
#             pass
#     except:
#         text = gerenciamento_caixa.lineEdit_preco.text()
#         text1= text[:-1]
#         text = gerenciamento_caixa.lineEdit_preco.setText(f"{text1}")


# def ref_only_int():
#     gerenciamento_caixa.label_menssagem_nfce.clear()
#     try:
#         if int(gerenciamento_caixa.lineEdit_ref.text()):
#             pass
#     except:
#         text = gerenciamento_caixa.lineEdit_ref.text()
#         text1= text[:-1]
#         text = gerenciamento_caixa.lineEdit_ref.setText(f"{text1}")

# def gerar_codigo_aleatorio_nfe():

#     codigo = randint(0,9999999)
#     gerenciamento_caixa.lineEdit_codigo_produto.setText(f"{codigo}")


# #ir para a tela de gerenciamento
# def ir_gerenciamento():
#     widget.setCurrentIndex(5)

# #pagamento

# def setar_formas_de_pagamentos():
#     gerenciamento_caixa.label_menssagem_nfce.clear()
#     combo_texto = gerenciamento_caixa.comboBox.currentText()

#     if combo_texto == "Dinheiro":
#         gerenciamento_caixa.label_9.show()
#         gerenciamento_caixa.label_10.show()
#         gerenciamento_caixa.lineEdit_pagamento.show()
#         gerenciamento_caixa.lineEdit_troco.show()
#         gerenciamento_caixa.lineEdit_pagamento.setFocus()
#         gerenciamento_caixa.comboBox_bandeira_operadora.hide()

#     elif combo_texto == "Cartão de Crédito" :
#         gerenciamento_caixa.comboBox_bandeira_operadora.show()
#         gerenciamento_caixa.label_9.hide()
#         gerenciamento_caixa.label_10.hide()
#         gerenciamento_caixa.lineEdit_pagamento.hide()
#         gerenciamento_caixa.lineEdit_troco.hide()

#     elif combo_texto == "Cartão de Débito" :
#         gerenciamento_caixa.comboBox_bandeira_operadora.show()
#         gerenciamento_caixa.label_9.hide()
#         gerenciamento_caixa.label_10.hide()
#         gerenciamento_caixa.lineEdit_pagamento.hide()
#         gerenciamento_caixa.lineEdit_troco.hide()


#     else:
#         gerenciamento_caixa.label_9.hide()
#         gerenciamento_caixa.label_10.hide()
#         gerenciamento_caixa.lineEdit_pagamento.hide()
#         gerenciamento_caixa.lineEdit_troco.hide()
#         gerenciamento_caixa.comboBox_bandeira_operadora.hide()


# def pagamento_nfce():

#     gerenciamento_caixa.label_menssagem_nfce.clear()
#     try:
#         if float(gerenciamento_caixa.lineEdit_pagamento.text()):
#             pass
#     except:
#         text = gerenciamento_caixa.lineEdit_pagamento.text()
#         text1= text[:-1]
#         text = gerenciamento_caixa.lineEdit_pagamento.setText(f"{text1}")
#         return
    
#     valor_pagamento = float(gerenciamento_caixa.lineEdit_pagamento.text())

    
#     if float(valor_pagamento) < produtoNFCE.preco_total_nota:
#         gerenciamento_caixa.lineEdit_troco.setText("0.00")
#         return

#     troco = valor_pagamento - produtoNFCE.preco_total_nota
#     gerenciamento_caixa.lineEdit_troco.setText(f"{troco:.2f}")


# def setar_total_pagamento():
#     valor = gerenciamento_caixa.lineEdit_pagamento.text()
#     if valor == "":
#         gerenciamento_caixa.lineEdit_pagamento.setText(f"{produtoNFCE.preco_total_nota:.2f}")

#     elif float(valor) < produtoNFCE.preco_total_nota:
#         gerenciamento_caixa.lineEdit_pagamento.setText(f"{produtoNFCE.preco_total_nota:.2f}")



# #classe de produto nfc-e

# class produtoNFCE:
    
#     lista_itens = []
#     nfce = {}
#     numero_itens = 0
#     formas_pagamento={}
#     cnpj_emitente =37480491000206       
#     nome_emitente = "AU DA COSTA SOUZA"
#     nome_fantasia_emitente = "PARIS HOTEL E MODA DO DIA"
#     logradouro_emitente = "AVENIDA COARACY NUNES,CENTRO"
#     numero_emitente = 189
#     bairro_emitente = "CENTRO"
#     municipio_emitente = "oiapoque"
#     uf_emitente ="AP"
#     cep_emitente = 68980000
#     inscricao_estadual_emitente = "030639930"
#     cfop = 5102
#     icms_situacao_tributaria = 102
#     unidade_comercial = "PC"
#     preco_total_nota = 0.00

#     def __init__(self,codigo,descricao,preco,ncm,icms_origem,quantidade):
#         itens = {}
#         preco_total = float(preco) * quantidade
        
#         produtoNFCE.numero_itens += 1
#         itens["numero_item"] = f"{produtoNFCE.numero_itens}"
#         itens["codigo_produto"] = f"{codigo}"
#         itens["descricao"] = f"{descricao}"
#         itens["codigo_ncm"] = f"{ncm}"
#         itens["cfop"] = f"{produtoNFCE.cfop}"
#         itens["valor_desconto"] = f"0.00"
#         itens["icms_origem"] =f"{icms_origem}"
#         itens["icms_situacao_tributaria"] = f"{produtoNFCE.icms_situacao_tributaria}"
#         itens["unidade_comercial"] = f"{produtoNFCE.unidade_comercial}"
#         itens["unidade_tributavel"] = f"{produtoNFCE.unidade_comercial}"
#         itens["quantidade_comercial"] = f"{quantidade}"
#         itens["quantidade_tributavel"] = f"{quantidade}"
#         itens["valor_unitario_comercial"] = f"{preco}"
#         itens["valor_unitario_tributavel"] = f"{preco}"
#         itens["valor_bruto"] = f"{preco_total}"

        
#         produtoNFCE.lista_itens.append(copy.deepcopy(itens))
        
#         gerenciamento_caixa.lineEdit_quantidade.setText(f"{produtoNFCE.numero_itens}")
#         produtoNFCE.preco_total_nota += preco_total
#         gerenciamento_caixa.lineEdit__valor_total.setText(f"{produtoNFCE.preco_total_nota:.2f}")
#         gerenciamento_caixa.lineEdit_quantidade_nfce.clear()


#     @classmethod
#     def resetar_class(cls):
#         produtoNFCE.preco_total_nota = 0.00
#         produtoNFCE.lista_itens.clear()
#         produtoNFCE.numero_itens = 1
#         produtoNFCE.nfce.clear()
#         gerenciamento_caixa.tableWidget_nfce.clearContents()
#         gerenciamento_caixa.tableWidget_nfce.setRowCount(0)
#         gerenciamento_caixa.lineEdit_pagamento.clear()
#         gerenciamento_caixa.lineEdit__valor_total.setText("0.00")
#         gerenciamento_caixa.lineEdit_quantidade.setText("0")


# #esse apaga produtos no banco de dados
# def deletar_produto_nfce():
#     v = "'"

#     cr = adicionar_produto_nfce.tableWidget_produtos.currentRow()
    

#     try:
#         item = adicionar_produto_nfce.tableWidget_produtos.item(cr,0).text()

#     except:
#         return

#     cursor.execute(f"delete from produtos_nfe where codigo_produto = {v+item+v}")
#     banco.commit()
#     cursor.execute("select codigo_produto , descricao , preco , ncm from produtos_nfe")

#     dados = cursor.fetchall()
#     adicionar_produto_nfce.tableWidget_produtos.setRowCount(len(dados))
#     adicionar_produto_nfce.tableWidget_produtos.setColumnCount(4)
#     for i in range(0, len(dados)):
#         for j in range(0,4):
#             adicionar_produto_nfce.tableWidget_produtos.setItem(i,j , QtWidgets.QTableWidgetItem(str(dados[i][j])))
#     adicionar_produto_nfce.tableWidget_produtos.resizeColumnsToContents()

# #esse apaga produtos da tela de emitir nfce
# def apagar_produto_nfce():
#     gerenciamento_caixa.label_menssagem_nfce.clear()

#     cr = gerenciamento_caixa.tableWidget_nfce.currentRow()

#     if cr == -1:
#         return

#     produtoNFCE.preco_total_nota -= float(produtoNFCE.lista_itens[cr]["valor_bruto"])
#     produtoNFCE.numero_itens -= 1
#     gerenciamento_caixa.lineEdit_quantidade.setText(f"{produtoNFCE.numero_itens}")
#     gerenciamento_caixa.lineEdit__valor_total.setText(f"{produtoNFCE.preco_total_nota:.2f}")

#     del produtoNFCE.lista_itens[cr]

#     itens= []
#     for i in range(len(produtoNFCE.lista_itens)):
#         itens.append([produtoNFCE.lista_itens[i]["descricao"],produtoNFCE.lista_itens[i]["quantidade_comercial"],format(float(produtoNFCE.lista_itens[i]["valor_bruto"]),".2f")])


#     gerenciamento_caixa.tableWidget_nfce.setRowCount(len(itens))
#     gerenciamento_caixa.tableWidget_nfce.setColumnCount(3)
#     for i in range(0, len(itens)):
#         for j in range(0,3):
#             gerenciamento_caixa.tableWidget_nfce.setItem(i,j , QtWidgets.QTableWidgetItem(str(itens[i][j])))
#     gerenciamento_caixa.tableWidget_nfce.resizeColumnsToContents()


#     print(cr)



# def emitir_nfce():
#     gerenciamento_caixa.label_menssagem_nfce.clear()

#     url = "https://api.focusnfe.com.br/v2/nfce?ref=REFERENCIA"
#     token="vd12bdhncNMf5h9OQUBCU4RkcD7NAEbz"
#     combo_texto = gerenciamento_caixa.comboBox.currentText()
#     data = datetime.datetime.now().isoformat()

#     valor_pagamento = gerenciamento_caixa.lineEdit_pagamento.text()

#     if valor_pagamento == "":
#         valor_pagamento = 0.00
        
#     valor_pagamento = float(valor_pagamento)
#     troco = float(gerenciamento_caixa.lineEdit_troco.text())
#     formas_pagamento = {}
#     ref = gerenciamento_caixa.lineEdit_ref.text()
#     bandeira = gerenciamento_caixa.comboBox_bandeira_operadora.currentText()

#     if ref == "":
#         ref = 1

#     ref = {"ref":f"{ref}"}


#     #definir bandeira do cartão
#     if bandeira == "Visa":
#         bandeira = 1
#     elif bandeira == "Mastercard":
#         bandeira = 2
#     elif bandeira == "American Express":
#         bandeira = 3 
#     elif bandeira == "Sorocred":
#         bandeira = 4
#     elif bandeira == "Outros":
#         bandeira = 99
#     else :
#         pass
    
#     print("bandeira " ,bandeira)


    

 

#     #pegar a forma de pagamento
#     if combo_texto == "Dinheiro":
#         formas_pagamento["forma_pagamento"] = "1"
#         produtoNFCE.nfce["forma_pagamento"] = "1"
#         formas_pagamento["valor_pagamento"] = f"{valor_pagamento}"
#         produtoNFCE.nfce["valor_troco"] = f"{troco}"


#     elif combo_texto == "Cartão de Crédito":
#         #4 é cartão de credito
#         formas_pagamento["forma_pagamento"] = "3"
#         produtoNFCE.nfce["forma_pagamento"] = "3"
#         formas_pagamento["valor_pagamento"] = f"{produtoNFCE.preco_total_nota}"
#         produtoNFCE.nfce["valor_troco"] = f"0.00"
#         formas_pagamento["bandeira_operadora"] = f"{bandeira}"

#     elif combo_texto == "Cartão de Débito":
#         formas_pagamento["forma_pagamento"] = "4"
#         produtoNFCE.nfce["forma_pagamento"] = "4"
#         formas_pagamento["valor_pagamento"] = f"{produtoNFCE.preco_total_nota}"
#         produtoNFCE.nfce["valor_troco"] = f"0.00"
#         formas_pagamento["bandeira_operadora"] = f"{bandeira}"
        


#     elif combo_texto == "outros":
#         formas_pagamento["forma_pagamento"] = "99"
#         produtoNFCE.nfce["forma_pagamento"] = "99"
#         formas_pagamento["valor_pagamento"] = f"{produtoNFCE.preco_total_nota}"
#         produtoNFCE.nfce["valor_troco"] = f"0.00"


#     produtoNFCE.nfce["cnpj_emitente"] = "37480491000206"
#     produtoNFCE.nfce["nome_emitente"] = "Au da costa souza"
#     produtoNFCE.nfce["nome_fantasia_emitente"] = "PARIS HOTEL E MODA DO DIA"
#     produtoNFCE.nfce["logradouro_emitente"] = "AVENIDA COARACY NUNES,CENTRO"
#     produtoNFCE.nfce["numero_emitente"] = "189"
#     produtoNFCE.nfce["bairro_emitente"] = "GERAL-OIAPOQUE"
#     produtoNFCE.nfce["municipio_emitente"] = "oiapoque"
#     produtoNFCE.nfce["uf_emitente"] = "AP"
#     produtoNFCE.nfce["cep_emitente"] = "68980-000"
#     produtoNFCE.nfce["inscricao_estadual_emitente"] = "030639930"
#     produtoNFCE.nfce["data_emissao"] = f"{data}"
#     produtoNFCE.nfce["natureza_operacao"] = "Venda ao Consumidor"
#     produtoNFCE.nfce["tipo_documento"] = "1"
#     produtoNFCE.nfce["presenca_comprador"] = "1"
#     produtoNFCE.nfce["finalidade_emissao"] = "1"
#     produtoNFCE.nfce["modalidade_frete"] = "9"
    

#     produtoNFCE.nfce["items"] = produtoNFCE.lista_itens
#     produtoNFCE.nfce["formas_pagamento"] = [formas_pagamento]

#     try:
#         r = requests.post(url, params=ref, data=json.dumps(produtoNFCE.nfce), auth=(token,""))
#     except:
#         gerenciamento_caixa.label_menssagem_nfce.setStyleSheet("color: rgb(255, 0, 0);")
#         gerenciamento_caixa.label_menssagem_nfce.setText("algo deu errado")
    
#         return
    

#     jay = r.json()
#     print(jay)
#     try:
#         danfe = jay["caminho_danfe"]

#         status = jay["status"]
        
#         if status == "autorizado":
#             menssagem_sefaz = jay["mensagem_sefaz"]
#             gerenciamento_caixa.label_menssagem_nfce.setStyleSheet("color: rgb(0, 255, 0);")
#             gerenciamento_caixa.label_menssagem_nfce.setText(f"{status}: {menssagem_sefaz}")
#             produtoNFCE.resetar_class()

#         elif status == "erro_autorizacao":
#             gerenciamento_caixa.label_menssagem_nfce.setStyleSheet("color: rgb(255, 0, 0);")
#             gerenciamento_caixa.label_menssagem_nfce.setText(status)
#     except:
#         pass

#     try:
#         msg = jay["mensagem"]
#         print(msg)
#         gerenciamento_caixa.label_menssagem_nfce.setStyleSheet("color: rgb(255, 0, 0);")
#         gerenciamento_caixa.label_menssagem_nfce.setText(msg)

#     except:
#         pass
    
#     print(r.status_code, r.text)

# #adicionar na tela de nfce

# def adicionar_produtos_nfce():
#     v = "'"
#     quantidade = gerenciamento_caixa.lineEdit_quantidade_nfce.text()

#     if quantidade == "":
#         quantidade = 1

#     cr = adicionar_produto_nfce.tableWidget_produtos.currentRow()
    

#     try:
#         item = adicionar_produto_nfce.tableWidget_produtos.item(cr,0).text()
#     except:
#         return


#     cursor.execute(f"select codigo_produto,descricao,preco,ncm,icms_origem from produtos_nfe where codigo_produto = {v+item+v}")
#     dados = cursor.fetchall()
#     produtosnfce = produtoNFCE(dados[0][0],dados[0][1],dados[0][2],dados[0][3],dados[0][4],int(quantidade))

#     itens= []
#     for i in range(len(produtoNFCE.lista_itens)):
#         itens.append([produtoNFCE.lista_itens[i]["descricao"],produtoNFCE.lista_itens[i]["quantidade_comercial"],format(float(produtoNFCE.lista_itens[i]["valor_bruto"]),".2f")])


#     gerenciamento_caixa.tableWidget_nfce.setRowCount(len(itens))
#     gerenciamento_caixa.tableWidget_nfce.setColumnCount(3)
#     for i in range(0, len(itens)):
#         for j in range(0,3):
#             gerenciamento_caixa.tableWidget_nfce.setItem(i,j , QtWidgets.QTableWidgetItem(str(itens[i][j])))
#     gerenciamento_caixa.tableWidget_nfce.resizeColumnsToContents()


#     adicionar_produto_nfce.close()

# #abrir tela de adicionar produtos para emissão
# def abri_add_produtos_para_emissao():
#     gerenciamento_caixa.label_menssagem_nfce.clear()
#     adicionar_produto_nfce.show()

#     cursor.execute("select codigo_produto , descricao , preco , ncm from produtos_nfe")

#     dados = cursor.fetchall()
#     adicionar_produto_nfce.tableWidget_produtos.setRowCount(len(dados))
#     adicionar_produto_nfce.tableWidget_produtos.setColumnCount(4)
#     for i in range(0, len(dados)):
#         for j in range(0,4):
#             adicionar_produto_nfce.tableWidget_produtos.setItem(i,j , QtWidgets.QTableWidgetItem(str(dados[i][j])))
#     adicionar_produto_nfce.tableWidget_produtos.resizeColumnsToContents()



# def add_produtos_nfe():
#     gerenciamento_caixa.label_menssagem.setText("")
#     v = "'"
#     #pegar todos os dados do produto

#     codigo_produto = gerenciamento_caixa.lineEdit_codigo_produto.text()
#     descricao = gerenciamento_caixa.lineEdit_descricao.text()
#     ncm = gerenciamento_caixa.lineEdit_ncm.text()
#     icms_origem = gerenciamento_caixa.lineEdit_icms_origem.text()
#     preco = gerenciamento_caixa.lineEdit_preco.text()

#     #verificar se os espaços estão vasios
#     if codigo_produto == "":
#         gerenciamento_caixa.label_menssagem.setStyleSheet("color: rgb(255, 0, 0);")
#         gerenciamento_caixa.label_menssagem.setText("os espaços não podem ficar em branco!")
#         gerenciamento_caixa.lineEdit_codigo_produto.setFocus()
#         return

#     if descricao == "":
#         gerenciamento_caixa.label_menssagem.setStyleSheet("color: rgb(255, 0, 0);")
#         gerenciamento_caixa.label_menssagem.setText("os espaços não podem ficar em branco!")
#         gerenciamento_caixa.lineEdit_codigo_produto.setFocus()
#         return

#     if ncm == "":
#         gerenciamento_caixa.label_menssagem.setStyleSheet("color: rgb(255, 0, 0);")
#         gerenciamento_caixa.label_menssagem.setText("os espaços não podem ficar em branco!")
#         gerenciamento_caixa.lineEdit_codigo_produto.setFocus()
#         return

#     if icms_origem == "":
#         gerenciamento_caixa.label_menssagem.setStyleSheet("color: rgb(255, 0, 0);")
#         gerenciamento_caixa.label_menssagem.setText("os espaços não podem ficar em branco!")
#         gerenciamento_caixa.lineEdit_codigo_produto.setFocus()
#         return

#     if preco == "":
#         gerenciamento_caixa.label_menssagem.setStyleSheet("color: rgb(255, 0, 0);")
#         gerenciamento_caixa.label_menssagem.setText("os espaços não podem ficar em branco!")
#         gerenciamento_caixa.lineEdit_codigo_produto.setFocus()
#         return

#     preco = format(float(preco),".2f")

#     #verificar se ja existe um codigo parecido
#     cursor.execute(f"select codigo_produto from produtos_nfe where codigo_produto = {v+codigo_produto+v}")
#     numero = cursor.fetchall()
#     if len(numero) > 0:
#         gerenciamento_caixa.label_menssagem.setStyleSheet("color: rgb(255, 0, 0);")
#         gerenciamento_caixa.label_menssagem.setText("o codigo cadastrado ja existe!!!")
#         return

#     if len(str(ncm)) < 8:
#         gerenciamento_caixa.label_menssagem.setStyleSheet("color: rgb(255, 0, 0);")
#         gerenciamento_caixa.label_menssagem.setText("o codigo ncm não pode ser menor do que 8 caracteres!!!")
#         return
#     #cadastrar o produto no banco de dados

#     cursor.execute("insert into produtos_nfe values (?, ?,?,?,?)", (codigo_produto,descricao,ncm,icms_origem,preco))

#     #limpar todas as line edit
#     gerenciamento_caixa.lineEdit_codigo_produto.clear()
#     gerenciamento_caixa.lineEdit_descricao.clear()
#     gerenciamento_caixa.lineEdit_ncm.clear()
#     gerenciamento_caixa.lineEdit_preco.clear()

#     #amostar menssagem que o produto for cadastrado com sucesso
#     gerenciamento_caixa.label_menssagem.setStyleSheet("color: rgb(0, 255, 0);")
#     gerenciamento_caixa.label_menssagem.setText("produto adicionado com sucesso!")
#     banco.commit()

# ##############################************************* Produtos Vendidos  ************************#########################



# def gerenciamento_key_press(event):
    
#     if event.key() == Qt.Key_Escape:
#         widget.setCurrentIndex(0)
#         return



# gerenciamento_caixa.keyPressEvent = gerenciamento_key_press

# # print(gerenciamento_caixa.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm"))

# def setar_filtro_vendas():
#     index = gerenciamento_caixa.comboBox_filtrar_vendas.currentIndex()

#     if index == 0:
#         gerenciamento_caixa.dateTimeEdit_filtrar_vendas_limite.setDateTime(QDateTime.currentDateTime()) 
#         gerenciamento_caixa.dateTimeEdit_filtrar_vendas.setVisible(True)
#         gerenciamento_caixa.dateTimeEdit_filtrar_vendas_limite.setVisible(True)
#         gerenciamento_caixa.label_de.setVisible(True)
#         gerenciamento_caixa.label_ate.setVisible(True)

#         gerenciamento_caixa.lineEdit_filtrar_vendas.clear()
#         gerenciamento_caixa.lineEdit_filtrar_vendas.setVisible(False)
        

#     else:
#         gerenciamento_caixa.dateTimeEdit_filtrar_vendas.setVisible(False)
#         gerenciamento_caixa.dateTimeEdit_filtrar_vendas_limite.setVisible(False)
#         gerenciamento_caixa.label_de.setVisible(False)
#         gerenciamento_caixa.label_ate.setVisible(False)


#         gerenciamento_caixa.lineEdit_filtrar_vendas.clear()
#         gerenciamento_caixa.lineEdit_filtrar_vendas.setVisible(True)




def start_pesquisar_vendas():


    if gerenciamento_caixa.comboBox_filtrar_vendas.currentText() == "Data E Hora":
        texto = gerenciamento_caixa.dateTimeEdit_filtrar_vendas.dateTime().toString("yyyy-MM-dd HH:mm:ss").split(" ")
        text = gerenciamento_caixa.dateTimeEdit_filtrar_vendas_limite.dateTime().toString("yyyy-MM-dd HH:mm:ss").split(" ")
        for i in range(len(text)):
            texto.append(text[i])

    else:
        texto = gerenciamento_caixa.lineEdit_filtrar_vendas.text().replace("'","").replace('"','')

    gerenciamento_caixa.tableWidget_produtos_vendidos.setRowCount(0)

    pesquisa = gerenciamento_caixa.thread = PesquisarVendasGerenciamento(texto)
    pesquisa.run()

    


################################################################

lockv = threading.Lock()

class PesquisarVendasGerenciamento():

    def __init__(self, pesquisar = ""):

        self.pesquisar = pesquisar
        self.resize_table = gerenciamento_caixa.tableWidget_produtos_vendidos.resizeColumnsToContents
        
    def run(self):

        combo = gerenciamento_caixa.comboBox_filtrar_vendas.currentText()

        if combo == "Data E Hora":
            print(self.pesquisar)
            cursor_tela_admim.execute(f"select strftime('%d/%m/%Y', Data) ,Hora,Quantidade,Troco,Total,ID from venda where Data BETWEEN datetime('{self.pesquisar[0]} {self.pesquisar[1]}', '-1 days') and datetime('{self.pesquisar[2]} {self.pesquisar[3]}', '+1 days') order by data desc,Hora desc")
            self.mostrar_na_table()
            self.resize_table()
            if lockv.locked():   
                lockv.release()
            return

        elif combo == "Total":
            cursor_tela_admim.execute(f"select strftime('%d/%m/%Y', Data),Hora,Quantidade,Troco,Total,ID from venda where Total like '%{str(self.pesquisar).replace(',','.')}%' order by Case total when '{str(self.pesquisar).replace(',','.')}' then 1 else Total end asc")
            self.mostrar_na_table()
            self.resize_table()
            if lockv.locked():   
                lockv.release()
            return

        elif combo == "Qtd.Vendido":
            cursor_tela_admim.execute(f"select strftime('%d/%m/%Y', Data),Hora,Quantidade,Troco,Total,ID from venda where Quantidade like '%{str(self.pesquisar).replace(',','.')}%' order by Case Quantidade when '{str(self.pesquisar)}' then 1 else Quantidade end asc")
            self.mostrar_na_table()
            self.resize_table()
            if lockv.locked():   
                lockv.release()
            return

        elif combo == "ID":
            cursor_tela_admim.execute(f"select strftime('%d/%m/%Y', Data),Hora,Quantidade,Troco,Total,ID from venda where Id like '%{str(self.pesquisar).replace(',','.')}%' order by Case Id when '{str(self.pesquisar).replace(',','.')}' then 1 else Id end asc ")
            self.mostrar_na_table()
            self.resize_table()
            if lockv.locked():   
                lockv.release()
            return
        if lockv.locked():
            lockv.release()
        return


    @classmethod
    def mostrar_na_table(cls):
        needed = 60
 
        data = cursor_tela_admim.fetchmany(needed)
        
        rowCount = gerenciamento_caixa.tableWidget_produtos_vendidos.rowCount()
        try:
            for i in range(0, needed):
                gerenciamento_caixa.tableWidget_produtos_vendidos.setRowCount(rowCount+i+1)
                for j in range(0, 6):
                    gerenciamento_caixa.tableWidget_produtos_vendidos.setItem(rowCount+i, j, QTableWidgetItem(str(data[i][j]).replace(".",",")))

            return


        except IndexError:
            gerenciamento_caixa.tableWidget_produtos_vendidos.setRowCount( gerenciamento_caixa.tableWidget_produtos_vendidos.rowCount() - 1)
            print("=====================")
            print("IndexError Because There is No Data to Get From Table")
            print("=====================")
            return




def abrir_navegar_vendas():


    

    combo = gerenciamento_caixa.comboBox_filtrar_vendas.currentText()
    index = gerenciamento_caixa.tableWidget_produtos_vendidos.currentIndex()

    if combo == "Data E Hora":
        texto = gerenciamento_caixa.dateTimeEdit_filtrar_vendas.dateTime().toString("yyyy-MM-dd HH:mm:ss").split(" ")
        text = gerenciamento_caixa.dateTimeEdit_filtrar_vendas_limite.dateTime().toString("yyyy-MM-dd HH:mm:ss").split(" ")
        for i in range(2):
            texto.append(text[i])
        cursor_tela_admim.execute(f"select id,id_caixa,Quantidade,Desconto,Data,Hora,Total,Troco,nfce_emitido from venda where Data BETWEEN datetime('{texto[0]} {texto[1]}', '-1 days') and datetime('{texto[2]} {texto[3]}', '+1 days') order by data desc,Hora desc")


    elif combo == "Total":
        texto = gerenciamento_caixa.lineEdit_filtrar_vendas.text()
        cursor_tela_admim.execute(f"select id,id_caixa,Quantidade,Desconto,Data,Hora,Total,Troco,nfce_emitido from venda where Total like '%{str(texto).replace(',','.')}%' order by Case total when '{str(texto).replace(',','.')}' then 1 else Total end asc")


    elif combo == "Qtd.Vendido":
        texto = gerenciamento_caixa.lineEdit_filtrar_vendas.text()
        cursor_tela_admim.execute(f"select id,id_caixa,Quantidade,Desconto,Data,Hora,Total,Troco,nfce_emitido from venda where Quantidade like '%{str(texto).replace(',','.')}%' order by Case Quantidade when '{str(texto)}' then 1 else Quantidade end asc")


    elif combo == "ID":
        texto = gerenciamento_caixa.lineEdit_filtrar_vendas.text()
        cursor_tela_admim.execute(f"select id,id_caixa,Quantidade,Desconto,Data,Hora,Total,Troco,nfce_emitido from venda where Id like '%{str(texto).replace(',','.')}%' order by Case Id when '{str(texto).replace(',','.')}' then 1 else Id end asc ")
  
    venda = cursor_tela_admim.fetchall()[index.row()]

    pagamento = cursor.execute(f"select * from Pagamento where ID_venda = {venda[0]}").fetchall()

    produtos = cursor.execute(f"select * from produtos_vendidos where ID_venda = {venda[0]}").fetchall()

    VisualizarVendas.id = venda[0]


    VisualizarVendas.produtos = produtos
    VisualizarVendas.venda = venda
    VisualizarVendas.pagamento = pagamento 

    Tela_registro_vendas.show()

    Tela_registro_vendas.tableWidget_pes.setRowCount(len(VisualizarVendas.produtos))
    Tela_registro_vendas.tableWidget_pes.setColumnCount(6)

    for i in range(0, len(VisualizarVendas.produtos)):
        for j in range(0,6):
            Tela_registro_vendas.tableWidget_pes.setItem(i,j , QtWidgets.QTableWidgetItem(str(VisualizarVendas.produtos[i][j+4])))

    for i in range(len(VisualizarVendas.pagamento)):
        if VisualizarVendas.pagamento[i][4] != None:
            Tela_registro_vendas.listWidget_forma_de_pagamento.addItem(f'{VisualizarVendas.pagamento[i][3]} / {VisualizarVendas.pagamento[i][4]}  {str(VisualizarVendas.pagamento[i][2]).replace(".",",")}')
            continue
        Tela_registro_vendas.listWidget_forma_de_pagamento.addItem(f'{VisualizarVendas.pagamento[i][3]} {str(VisualizarVendas.pagamento[i][2]).replace(".",",")}')

    total = 0

    for i in range(len(VisualizarVendas.pagamento)):
        total += float(str(VisualizarVendas.pagamento[i][2]).replace(",","."))


    data = [VisualizarVendas.venda[4].split('-')[-2+i] for i in range(3)]

    Tela_registro_vendas.label_data.setText(f"{data[1]}/{data[0]}/{data[2]}")
    Tela_registro_vendas.label_hora.setText(f"{VisualizarVendas.venda[5]}")

    Tela_registro_vendas.label_valor.setText(f"Total Da Venda: {VisualizarVendas.venda[6]}".replace(".",","))
    Tela_registro_vendas.label_desconto.setText(f"Desconto: {VisualizarVendas.venda[3]}")
    Tela_registro_vendas.label_total.setText(f"Total Pago: {total:.2f}".replace(".",","))
    Tela_registro_vendas.label_troco.setText(f"Troco: {float(VisualizarVendas.venda[7]):.2f}".replace(".",","))



    #setar impressora_cupom
    Tela_registro_vendas.comboBox_lista_impressora.clear()
    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    cur_impressora = config["Config_Impressao"]["impressora_cupom"]

    impressora = list(win32print.EnumPrinters(2))

    for i in range(len(impressora)):
        if str(cur_impressora) == str(impressora[i][2]):
            del impressora[i]
            Tela_registro_vendas.comboBox_lista_impressora.addItem(f"{cur_impressora}")
            break

    for i in range(len(impressora)):
        Tela_registro_vendas.comboBox_lista_impressora.addItem(impressora[i][2])


    verificar_cancelamento = cursor.execute(f'select * from venda where ID = {VisualizarVendas.id} and ID_caixa = {config["Caixa"]["id"]} ').fetchall()

    if verificar_cancelamento:
        Tela_registro_vendas.pushButton_cancelar_venda.setVisible(True)
    else:
        Tela_registro_vendas.pushButton_cancelar_venda.setVisible(False)


    Tela_registro_vendas.exec()
    
class VisualizarVendas:
    id = 0
    quantidade_produtos = 0
    venda = []
    pagamento = []
    produtos = []

    def __init__(self):
        pass

    def cancelar_produtos(self):

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
        
        cursor.execute(f"delete from venda where id = {VisualizarVendas.id}")
        banco.commit()
        Tela_registro_vendas.close()

        gerenciamento_caixa.dateTimeEdit_filtrar_vendas_limite.setDateTime(QDateTime.currentDateTime()) 

        msg = QMessageBox(Tela_registro_vendas)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
        msg.setText(f'''Venda Cancelada com sucesso''')
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Cancelado.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)  
        msg = msg.exec_()
        
       
        
        
    



def tela_ver_vendas_close_event(event):
    quantidade_produtos = 0
    VisualizarVendas.venda = []
    VisualizarVendas.pagamento = []
    VisualizarVendas.produtos = []
    Tela_registro_vendas.listWidget_forma_de_pagamento.clear()
    Tela_registro_vendas.tableWidget_pes.setRowCount(0)



def imprimir_cupom_na_view_produtos():
    from Core.Admin.Caixa.cupom_recibo import Recibo

    url = f"{c}\cupom_vendas\Recibos\{VisualizarVendas.id}.pdf"
    impressora = Tela_registro_vendas.comboBox_lista_impressora.currentText()

    Recibo.imprimir_cupom(url,impressora)



def index_tab_gerenciamento_changed():
    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    index = gerenciamento_caixa.tabWidget.currentIndex()

    if index == 0:
        pass
    elif index == 1:
        #lista de impressoras
        impressora = list(win32print.EnumPrinters(2))
        cur_impressora = config["Config_Impressao"]["impressora_cupom"]

        for i in range(len(impressora)):
            if str(cur_impressora) == str(impressora[i][2]):
                del impressora[i]
                gerenciamento_caixa.comboBox_lista_impressora.addItem(f"{cur_impressora}")
                break

        for i in range(len(impressora)):
            gerenciamento_caixa.comboBox_lista_impressora.addItem(impressora[i][2])

        #check box

        if config["Caixa"]["imprimir_recibo"] == "True":
            gerenciamento_caixa.checkBox_imprimir_cupom_nao_fiscal_finish_venda.setChecked(True)
        
        if config["Caixa"]["imprimir_nfce"] == "True":
            gerenciamento_caixa.checkBox_imprimir_danfe.setChecked(True)

        if config["Caixa"]["emitir_nfce"] == "True":
            gerenciamento_caixa.checkBox_emitir_nfce.setChecked(True)


        gerenciamento_caixa.lineEdit_referencia_nfce.setText(f'{config["NFE"]["ref"]}')

        return


def definir_impressora_padrao():

    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    nome_impressora = gerenciamento_caixa.comboBox_lista_impressora.currentText()
    config["Config_Impressao"]["impressora_cupom"] = nome_impressora
    with open(file, 'w') as configfile:
        config.write(configfile)

    msg = QMessageBox()
    msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
    msg.setText(f'''Definida como Padrão.''')
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Sucesso")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    msg = msg.exec_()


def definir_atual_referencia_nfe_gerenciamento():
    user_text = gerenciamento_caixa.lineEdit_referencia_nfce.text()

    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    config["NFE"]["ref"] = user_text

    with open(file, 'w') as configfile:
        config.write(configfile)
    
    msg = QMessageBox()
    msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
    msg.setText(f'''Definida como Padrão.''')
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Sucesso")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    msg = msg.exec_()



def setar_checkBox_gerenciamento(comando):
    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    if comando == "imprimir cupom nao fiscal":

        if gerenciamento_caixa.checkBox_imprimir_cupom_nao_fiscal_finish_venda.isChecked():
            config["Caixa"]["imprimir_recibo"] = "True"

        else:
            config["Caixa"]["imprimir_recibo"] = "False"

        with open(file, 'w') as configfile:
            config.write(configfile)
        return

    elif comando == "emitir nfce":
        if gerenciamento_caixa.checkBox_emitir_nfce.isChecked():
            config["Caixa"]["emitir_nfce"] = "True"

        else:
            config["Caixa"]["emitir_nfce"] = "False"

        with open(file, 'w') as configfile:
            config.write(configfile)
        return

    elif comando == "imprimir danfe":
        if gerenciamento_caixa.checkBox_imprimir_danfe.isChecked():
            config["Caixa"]["imprimir_nfce"] = "True"

        else:
            config["Caixa"]["imprimir_nfce"] = "False"
            
        with open(file, 'w') as configfile:
            config.write(configfile)
        return


def imprimir_pagina_teste_gerenciamento():
    output = f"{c}\cupom_vendas\Recibos\Desmontração De teste.pdf"
    impressora = gerenciamento_caixa.comboBox_lista_impressora.currentText()

    
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




gerenciamento_caixa.pushButton_definir_atual_referencia.clicked.connect(definir_atual_referencia_nfe_gerenciamento)
gerenciamento_caixa.tabWidget.currentChanged.connect(index_tab_gerenciamento_changed)
gerenciamento_caixa.pushButton_definir_impressora.clicked.connect(definir_impressora_padrao)

gerenciamento_caixa.checkBox_imprimir_cupom_nao_fiscal_finish_venda.stateChanged.connect(lambda:setar_checkBox_gerenciamento("imprimir cupom nao fiscal"))
gerenciamento_caixa.checkBox_emitir_nfce.stateChanged.connect(lambda:setar_checkBox_gerenciamento("emitir nfce"))
gerenciamento_caixa.checkBox_imprimir_danfe.stateChanged.connect(lambda:setar_checkBox_gerenciamento("imprimir danfe"))

gerenciamento_caixa.pushButton_imprimir_pagina_teste.clicked.connect(imprimir_pagina_teste_gerenciamento)


Tela_registro_vendas.pushButton_imprimir_cupom.clicked.connect(imprimir_cupom_na_view_produtos)
Tela_registro_vendas.closeEvent = tela_ver_vendas_close_event





