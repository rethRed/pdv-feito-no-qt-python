
from load import *



class NFCE:


    def __init__(self) :

        data = datetime.datetime.now().isoformat()

        #armazena o dicionario de todos os itens da nfce

        self.lista_itens = []

        #armazena o dicionario de pagamentos

        self.lista_pagamentos = []

        #dicionario  da nfce


        self.nfce = {}


        #pegar as imformações do do emitente no file "Config.ini"
        file = f"{c}\DataBase\config.ini"
        self.informaçoes = ConfigParser()
        self.informaçoes.read(file)
        #informacões da empresa
        self.nfce["cnpj_emitente"] = f'{self.informaçoes["Empresa"]["cnpj"]}'
        self.nfce["nome_emitente"] = f'{self.informaçoes["Empresa"]["nome"]  }'
        self.nfce["nome_fantasia_emitente"] = f'{self.informaçoes["Empresa"]["nome_fantasia"]}'
        self.nfce["logradouro_emitente"] = f'{self.informaçoes["Empresa"]["logradouro"] }'
        self.nfce["numero_emitente"] = f'{self.informaçoes["Empresa"]["numero"] }'
        self.nfce["bairro_emitente"] = f'{self.informaçoes["Empresa"]["bairro"] }'
        self.nfce["municipio_emitente"] = f'{self.informaçoes["Empresa"]["municipio"] }'
        self.nfce["uf_emitente"] = f'{self.informaçoes["Empresa"]["uf"]}'
        self.nfce["cep_emitente"] = f'{self.informaçoes["Empresa"]["cep"] }'
        self.nfce["inscricao_estadual_emitente"] = f'{self.informaçoes["Empresa"]["inscricao"] }'
        self.nfce["data_emissao"] = f"{data}"
        self.nfce["tipo_documento"] = "1"
        self.nfce["presenca_comprador"] = "1"
        self.nfce["finalidade_emissao"] = "1"
        self.nfce["modalidade_frete"] = "9" 
        
        #informações do nfe

        self.url = self.informaçoes["NFE"]["url"]
        self.token = self.informaçoes["NFE"]["token_produtocao"]
        self.ref = self.informaçoes["NFE"]["ref"]


    def add_itens(self,codigo,descricao,ncm,valor_desconto,quantidade,valor,valor_bruto,unidade,icms_origem):

        itens = {}

        itens["numero_item"] = f"{len(self.lista_itens) + 1}"
        itens["codigo_produto"] = f"{codigo}"
        itens["descricao"] = f"{descricao}"
        itens["codigo_ncm"] = f"{ncm}"
        itens["cfop"] = f"{self.informaçoes['Empresa']['cfop']}"
        itens["valor_desconto"] = f"{valor_desconto}"
        itens["icms_origem"] =f"{icms_origem}"
        itens["icms_situacao_tributaria"] = f'{self.informaçoes["Empresa"]["icms_situacao_tributaria"]}'
        itens["unidade_comercial"] = f'{unidade}'
        itens["unidade_tributavel"] = f'{unidade}'
        itens["quantidade_comercial"] = f"{quantidade}"
        itens["quantidade_tributavel"] = f"{quantidade}"
        itens["valor_unitario_comercial"] = f"{valor}"
        itens["valor_unitario_tributavel"] = f"{valor}"
        itens["valor_bruto"] = f"{valor_bruto}"

        
        self.lista_itens.append(copy.deepcopy(itens))
            

    def set_pagamentos(self,forma_pagamento,valor_pagamento,bandeira_operadora = ""):

        formas_pagamento = {}

        formas_pagamento["forma_pagamento"] = f"{forma_pagamento}"

        #se for cartão, colocar a bandeira da operadora
        if str(forma_pagamento) == "3" or str(forma_pagamento) == "4":
            formas_pagamento["bandeira_operadora"] = f"{bandeira_operadora}"

        formas_pagamento["valor_pagamento"] = f"{valor_pagamento}"
        
        

        self.lista_pagamentos.append(copy.deepcopy(formas_pagamento))

 

    def emitir_nfce(self,troco,funtion_complete = None, fuction_error = None):

        #setar os itens, pagamentos e o troco
        
        self.nfce["items"] = self.lista_itens
        self.nfce["formas_pagamento"] = self.lista_pagamentos
        self.nfce["valor_troco"] = f"{troco}"

 
        

        ref = {"ref":f"{self.ref}"}
 
    
        try:
            r = requests.post(f"{self.url}", params=ref, data=json.dumps(self.nfce), auth=(f"{self.token}",""),timeout=10)

        except requests.exceptions.ConnectTimeout:
            fuction_error(f"Erro: Demorou muito tempo para emitir a Nota. Nota não emitida.")
            final_requirements_to_finish_vendas()
            return
        
        except requests.exceptions.ReadTimeout:
            fuction_error(f"Erro: Erro ao emitir a nota")
            final_requirements_to_finish_vendas()
            return

        except requests.exceptions.ConnectionError:
            fuction_error(f"Sem conexão a internet. Não foi possivel emitir a Nota.")
            final_requirements_to_finish_vendas()
            return

        
        print(r.status_code, r.text)
        resposta = r.json()
       
        if "status" in resposta:

            if resposta["status"] == "autorizado":
                
                file = f"{c}\DataBase\config.ini"
                informaçoes = ConfigParser()
                informaçoes.read(file)

                informaçoes["NFE"]["ref"] = str(int(self.ref) + 1)

                with open(file, 'w') as config:
                    informaçoes.write(config)
                    
                from Core.vendas.tela_vendas import produto
                cursor.execute(f"update venda set nfce_emitido = 1 ,ref_nfce = {self.ref} where id = {produto.id_da_venda_atual}")
                banco.commit()

                if f'{informaçoes["Caixa"]["imprimir_nfce"]}' == "True":
                    
                    self.imprimir(resposta["caminho_danfe"],f'{informaçoes["Config_Impressao"]["impressora_cupom"]}',resposta["chave_nfe"],fuction_error)

                final_requirements_to_finish_vendas()
                return

        elif "codigo" in resposta:

            if resposta["codigo"] == "already_processed":
                fuction_error(f'Nota com a referencia "{self.ref}" Já autorizada.')
                final_requirements_to_finish_vendas()
                return

            elif resposta["codigo"] == "erro_validacao_schema":
                fuction_error(f"Nota Não autorizada Erro de Schema.")
                final_requirements_to_finish_vendas()
                return

       

    
    def imprimir(self,url,impressora_nome,chave,fuction_error = None):
        
        web_path = f"https://api.focusnfe.com.br{url}"

        wkh_path = rf"{c}\cupom_vendas\wkhtmltopdf\bin\wkhtmltopdf.exe"

        config = pdfkit.configuration(wkhtmltopdf = wkh_path)

        opcoes = {
            'page-height': '280mm',
            'page-width': '70mm',
            'margin-top': '0',
            'margin-right': '0',
            'margin-bottom': '0',
            'margin-left': '0',
            'minimum-font-size': "15"
            }



        file_output_path = rf"{c}\cupom_vendas\Recibos Fiscais\{chave}.pdf"


        try:
            pdfkit.from_url(f"{web_path}",file_output_path,options= opcoes, configuration =config )
        

        except OSError:
            fuction_error(f"Nota Autorizada, Mas não foi possivel imprimir.")
            return

            
        
        try:
            win32print.SetDefaultPrinterW(impressora_nome)
            win32api.ShellExecute(0,"print",file_output_path,None,".",0)
        except:
            NFCE.menssagem("Nota Autorizada, Mas não foi possivel imprimir.")
            return

    
    def chamar_menssagem(texto):
        menssagemd = NFCE.menssagem()
        menssagemd.final.emit(f"{texto}")


    def menssagem_(texto = ""):
        try:
            msg = QMessageBox()
            msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
            msg.setText(f'''{texto}''')
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)  
            msg = msg.exec_()
        except:
            final_requirements_to_finish_vendas()
            return

        final_requirements_to_finish_vendas()
        


    class menssagem(QtCore.QThread):

        final = QtCore.pyqtSignal(str)


        def __init__(self, parent = None):
            super(NFCE.menssagem,self).__init__(parent)
            self.final.connect(NFCE.menssagem_)


def final_requirements_to_finish_vendas_function():
    from Core.vendas.tela_vendas import produto
    confirmaçao.close()
    widget.setCurrentIndex(4)

    resumo_operacao.label_valor_total.setText(f'R$ {float(str(produto.total).replace(",",".")):.2f}'.replace(".",","))

    for i in range(len(produto.valor_recebido)):
        item = QListWidgetItem(f"{produto.forma_de_pagamento[i][0]}")
        item.setTextAlignment(Qt.AlignRight) 
        resumo_operacao.listWidget_metodo_pagamento.addItem(item)

    for i in range(len(produto.valor_recebido)):
        item = QListWidgetItem(f'R$ {float(str(produto.valor_recebido[i]).replace(",",".")):.2f}'.replace(".",","))
        item.setTextAlignment(Qt.AlignLeft) 
        resumo_operacao.listWidget_valores_recebidos.addItem(item)

    
    valor_recebido = 0
    for i in range(len(produto.valor_recebido)):
        valor_recebido += float(str(produto.valor_recebido[i]).replace(",","."))

    resumo_operacao.label_total_recebido.setText(f'R$ {valor_recebido:.2f}'.replace(".",","))
    resumo_operacao.label_troco.setText(f'R$ {float(str(produto.troco).replace(",",".")):.2f}'.replace(".",","))
    tela_vendas.tableWidget_vendas.clearContents()
    tela_vendas.tableWidget_vendas.setRowCount(0)
    tela_vendas.lineEdit_desconto_ind.setText(f'0%')
    tela_vendas.lineEdit_quantidade.setText(f'0%')
    tela_vendas.lineEdit__quantidade_itens.setText(f'0')
    tela_vendas.lineEdit__quantidade_produtos.setText(f'0')
    tela_vendas.lineEdit__descontoo.setText(f'0%')
    tela_vendas.lineEdit__total.setText(f'0,00')
    produto.resetar_classe()




def final_requirements_to_finish_vendas():
    therad = FuntionsThead( function = final_requirements_to_finish_vendas_function,signal_type = str)
    therad.signal_handler.emit()





