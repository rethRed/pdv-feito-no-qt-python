from load import *





def setar_funcionario():



    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    config["Caixa"]["id_funcionario"] = ""

    with open(file, 'w') as configfile:
        config.write(configfile)




def text_changed_no_line_abrir_caixa():
    

    try:
        if float(abrir_caixa.lineEdit_saldo_inicial.text().replace(",",".")):
            pass
    except:
        text = abrir_caixa.lineEdit_saldo_inicial.text()
        text1= text[:-1]
        text = abrir_caixa.lineEdit_saldo_inicial.setText(f"{text1}")
        return






def get_abrir_caixa_working():

    if  abrir_caixa.lineEdit_saldo_inicial.text() == "":
        msg = QMessageBox(abrir_caixa)
        msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
        msg.setText(f"O Campo de saldo inicial não pode ficar vazio.")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg = msg.exec_()
        return



    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)
    print("working")

    #setando as variaveis data e hora
    cur_data = abrir_caixa.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm").split(" ")
    data = cur_data[0]
    hora = cur_data[1]

    #setando o id

    idd = randint(10000000,99999999)

    while True:
            #verificar se existe um id igual no banco de dados
        cursor.execute(f"select * from caixa where Id = {idd}")
        dados = cursor.fetchall()
        if len(dados) == 0:
            break
        else:
            idd = randint(10000000,99999999)

    saldo_inicial = format(float(abrir_caixa.lineEdit_saldo_inicial.text().replace(",",".").lstrip().rstrip()),".2f")
    idd = str(idd)
    id_funcionario = config["Caixa"]["id_funcionario"]

    #indicar que o caixa esta aberto
    cursor.execute("update config set caixa_aberto = 1 where caixa_aberto not null;")

    #inserir informações iniciais com data e hora de abertura status e id
    v = "'"
    cursor.execute("insert into caixa values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (idd,data,hora,"aguardado","aguardado",f"{saldo_inicial}","aguardado","aguardado","aguardado","aguardado","aguardado","aguardado","aguardado","'aguardado'","aguardado","aguardado","Ativo"))

    #inserir o id do caixa atual nas config do programa

    cursor.execute(f"update config set atual_caixa_id = {idd} where atual_caixa_id not null;")

    banco.commit()


    config["Caixa"]["id"] = idd
    config["Caixa"]["caixa_aberto"] = "True"

    with open(file, 'w') as configfile:
        config.write(configfile)

    abrir_caixa.close()


def refechar_caixa(id_caixa):
    
    verificarSeCaixaEstaAtivo = cursor.execute(f"select ifnull(status,'Ativo') from caixa where id = {id_caixa}").fetchall()[0][0]

    if verificarSeCaixaEstaAtivo == "Ativo":
        print("o caixa esta ativo")
        return
    
    print(id_caixa)
    print("nao ativo")

    valor_total_dinheiro = cursor.execute(f'''
select  
(
select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN 
(SELECT Id from Venda WHere id_caixa = {id_caixa}) and Metodo_Pagamento = "DINHEIRO")), 0.00)) - ifnull(sum(venda.Troco),0.00) 

from venda
where id in (SELECT Id from Venda WHere id_caixa = {id_caixa})
    ''').fetchall()[0][0]
    valor_total_cartao_credito = cursor.execute(f'select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN (SELECT Id from Venda WHere id_caixa = {id_caixa}) and Metodo_Pagamento = "CARTÃO DE CRÉDITO")),0.00)').fetchall()[0][0]
    valor_total_cartao_debito = cursor.execute(f'select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN (SELECT Id from Venda WHere id_caixa = {id_caixa}) and Metodo_Pagamento = "CARTÃO DE DÉBITO")),0.00)').fetchall()[0][0]
    valor_total_pix = cursor.execute(f'select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN (SELECT Id from Venda WHere id_caixa = {id_caixa}) and Metodo_Pagamento = "PIX")),0.00)').fetchall()[0][0]
    valor_total_outros = cursor.execute(f'select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN (SELECT Id from Venda WHere id_caixa = {id_caixa})) and Metodo_Pagamento != "DINHEIRO" AND Metodo_Pagamento != "CARTÃO DE CRÉDITO" AND Metodo_Pagamento != "CARTÃO DE DÉBITO" AND Metodo_Pagamento != "PIX"),0.00) ').fetchall()[0][0]

    total_entradas = cursor.execute(f'select ifnull((select sum(Valor) from Entrada where ID_caixa = {id_caixa}),0.00)').fetchall()[0][0]
    total_saidas = cursor.execute(f'select ifnull((select sum(Valor) from Saida where ID_caixa = {id_caixa}),0.00)').fetchall()[0][0]

    Valor_total = cursor.execute(f'''select (select ifnull((select  
(
select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN 
(SELECT Id from Venda WHere id_caixa = {id_caixa}) )), 0.00) - ifnull(sum(venda.Troco),0.00) 

from venda
where id in (SELECT Id from Venda WHere id_caixa = {id_caixa}))),0.00) + 
      ifnull((select sum(Valor) from Entrada where ID_caixa = {id_caixa} ),0.00) - ifnull((select sum(Valor) from Saida where ID_caixa = {id_caixa} ),0.00)) as valor''').fetchall()[0][0]

    quantidade_itens = cursor.execute(f'select ifnull((select sum(replace(quantidade,"x","")) from produtos_vendidos where ID_venda IN (SELECT ID from Venda where id_caixa = {id_caixa})),0)').fetchall()[0][0]
    quantidade_produtos = cursor.execute(f'select ifnull((select sum(replace(quantidade,"x","")) from Venda where id_caixa = {id_caixa}),0)').fetchall()[0][0]




    cursor.execute(f'''UPDATE caixa SET total_dinheiro = "{valor_total_dinheiro}", total_cartao_debito = "{valor_total_cartao_debito}",
    total_cartao_credito = "{valor_total_cartao_credito}", total_pix = "{valor_total_pix}", total_outros = "{valor_total_outros}", total_entrada = "{total_entradas}", total_saida = "{total_saidas}" ,
    total_itens_vendidos = "{quantidade_itens}",  total_produtos_vendidas = "{quantidade_produtos}", tota_do_dia = "{Valor_total}" where ID = {id_caixa} ''')

    banco.commit()

def fechar_caixa():

    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)


    if cursor.execute(f'select Fechar_Caixa from Acesso_usuario where id = {config["Caixa"]["id_funcionario"]}').fetchall()[0][0] != 1:
        while True:
            permitido = PedirPermissao().return_answer()
            
            if permitido == True:
                break

            else:
                return

    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)


    id_caixa = config["Caixa"]["id"]



    data_agora=datetime.datetime.now()
    data_fechamento = data_agora.strftime("%Y-%m-%d")
    hora_fechamento = data_agora.strftime("%H-%M").replace("-",":")


    

    valor_total_dinheiro = cursor.execute(f'''

select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN 
(SELECT Id from Venda WHere id_caixa = {id_caixa}) and Metodo_Pagamento = "DINHEIRO")), 0.00) - ifnull(sum(venda.Troco),0.00) 
from venda
where id in (SELECT Id from Venda WHere id_caixa = {id_caixa})
    ''').fetchall()[0][0]
    valor_total_cartao_credito = cursor.execute(f'select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN (SELECT Id from Venda WHere id_caixa = {id_caixa}) and Metodo_Pagamento = "CARTÃO DE CRÉDITO")),0.00)').fetchall()[0][0]
    valor_total_cartao_debito = cursor.execute(f'select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN (SELECT Id from Venda WHere id_caixa = {id_caixa}) and Metodo_Pagamento = "CARTÃO DE DÉBITO")),0.00)').fetchall()[0][0]
    valor_total_pix = cursor.execute(f'select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN (SELECT Id from Venda WHere id_caixa = {id_caixa}) and Metodo_Pagamento = "PIX")),0.00)').fetchall()[0][0]
    valor_total_outros = cursor.execute(f'select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN (SELECT Id from Venda WHere id_caixa = {id_caixa})) and Metodo_Pagamento != "DINHEIRO" AND Metodo_Pagamento != "CARTÃO DE CRÉDITO" AND Metodo_Pagamento != "CARTÃO DE DÉBITO" AND Metodo_Pagamento != "PIX"),0.00) ').fetchall()[0][0]

    total_entradas = cursor.execute(f'select ifnull((select sum(Valor) from Entrada where ID_caixa = {id_caixa}),0.00)').fetchall()[0][0]
    total_saidas = cursor.execute(f'select ifnull((select sum(Valor) from Saida where ID_caixa = {id_caixa}),0.00)').fetchall()[0][0]

    Valor_total = cursor.execute(f'''select (select ifnull((select  
(
select ifnull((select sum(replace(Valor_Pago,",",".")) from Pagamento where ID IN ( SELECT ID from Pagamento where ID_venda IN 
(SELECT Id from Venda WHere id_caixa = {id_caixa}) )), 0.00) - ifnull(sum(venda.Troco),0.00) 

from venda
where id in (SELECT Id from Venda WHere id_caixa = {id_caixa}))),0.00) + 
      ifnull((select sum(Valor) from Entrada where ID_caixa = {id_caixa}),0.00) - ifnull((select sum(Valor) from Saida where ID_caixa = {id_caixa} ),0.00)) as valor''').fetchall()[0][0]

    quantidade_itens = cursor.execute(f'select ifnull((select sum(replace(quantidade,"x","")) from produtos_vendidos where ID_venda IN (SELECT ID from Venda where id_caixa = {id_caixa})),0)').fetchall()[0][0]
    quantidade_produtos = cursor.execute(f'select ifnull((select sum(replace(quantidade,"x","")) from Venda where id_caixa = {id_caixa}),0)').fetchall()[0][0]

    total_no_caixa = cursor.execute(f''' 

    with id_das_vendas(id_vendas) as (
select ID from Venda where id_caixa = {id_caixa}
)

select
(select sum(Pagamento.Valor_Pago) 
from Pagamento
where Pagamento.Metodo_Pagamento = "DINHEIRO" and Pagamento.ID_venda in (SELECT id_vendas from  id_das_vendas) ) - 

(SELECT sum(venda.Troco) from venda where  venda.Id in (SELECT id_vendas from  id_das_vendas)) +

(select sum(Valor) from Entrada where id_caixa = {id_caixa} and Pagamento = "DINHEIRO") - 
(select sum(Valor) from Saida where id_caixa = {id_caixa} ) +
(select saldo_inicial from caixa where id = {id_caixa})
    ''').fetchall()[0][0]

    print(total_no_caixa)

    cursor.execute(f'''UPDATE caixa SET data_fechamento = "{data_fechamento}", hora_fechamento = "{hora_fechamento}", total_dinheiro = "{valor_total_dinheiro}", total_cartao_debito = "{valor_total_cartao_debito}",
    total_cartao_credito = "{valor_total_cartao_credito}", total_pix = "{valor_total_pix}", total_outros = "{valor_total_outros}", total_entrada = "{total_entradas}", total_saida = "{total_saidas}" ,
    total_itens_vendidos = "{quantidade_itens}",  total_produtos_vendidas = "{quantidade_produtos}", tota_do_dia = "{Valor_total}", status = "Fechado"  where ID = {id_caixa}               ''')

    banco.commit()

    with open(file, 'w') as configfile:
        config["Caixa"]["caixa_aberto"]  = "False"
        config.write(configfile)

    fecha_caixar.close()

    if cursor.execute(f'select Usuario_Ver_o_Resulmo_De_Caixa_ao_Fechar from Acesso_usuario where id = {config["Caixa"]["id_funcionario"]}').fetchall()[0][0] != 1:
        msg = QMessageBox()
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
        msg.setText(f''' Caixa Fechado''')
        msg.setIcon(QMessageBox.Information )
        msg.setWindowTitle("Caixa Fechado")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)  
        msg.exec_()
        tela_login.lineEdit.clear()
        tela_login.lineEdit_2.clear()
        widget.setCurrentIndex(3)
        return

    data_abertura = cursor.execute(f"select strftime('%d/%m/%Y', data_abertura) from caixa where id = {id_caixa}").fetchall()[0][0]
    hora_abertura = cursor.execute(f"select strftime('%H:%M', hora_abertura) from caixa where id = {id_caixa}").fetchall()[0][0]


    resumo_do_caixa.label_horario_abertura.setText(f"{data_abertura}  {hora_abertura}")
    resumo_do_caixa.label_horario_fechamento.setText(f'{data_agora.strftime("%d/%m/%Y")}  {hora_fechamento}')

    saldo_inicial = cursor.execute(f"select saldo_inicial from Caixa where id = {id_caixa}").fetchall()[0][0]
    resumo_do_caixa.listWidget.clear()
    #todas os valores 
    resumo_do_caixa.label_13.setText(f"Saldo Inicial: {float(saldo_inicial):.2f}".replace(".",","))
    resumo_do_caixa.label_6.setText(f"{float(valor_total_dinheiro):.2f}".replace(".",","))
    resumo_do_caixa.label_10.setText(f"{float(valor_total_cartao_debito):.2f}".replace(".",","))
    resumo_do_caixa.label_12.setText(f"{float(valor_total_cartao_credito):.2f}".replace(".",","))
    resumo_do_caixa.label_8.setText(f"{float(valor_total_pix):.2f}".replace(".",","))
    resumo_do_caixa.label_4.setText(f"{float(valor_total_outros):.2f}".replace(".",","))
    resumo_do_caixa.label_20.setText(f"{float(total_entradas):.2f}".replace(".",","))
    resumo_do_caixa.label_18.setText(f"{float(total_saidas):.2f}".replace(".",","))
    resumo_do_caixa.label_22.setText(f"{float(Valor_total):.2f}".replace(".",","))
    resumo_do_caixa.label_24.setText(f"{float(total_no_caixa):.2f}".replace(".",","))

    entradas = cursor.execute(f"select strftime('%d/%m/%Y',data),hora,pagamento,replace(printf('%.2f',valor),'.',',') from entrada where id_caixa = {id_caixa}").fetchall()
    for i in range(len(entradas)):
        resumo_do_caixa.listWidget.addItem(f"{entradas[i][0]} {entradas[i][1]}   {entradas[i][2]}  {entradas[i][3]}")

    #quantidade de produtos Vendidos

    resumo_do_caixa.label_35.setText(f"{quantidade_itens}".zfill(3))

    fazer_relatorio()

    resumo_do_caixa.exec_()




    tela_login.lineEdit.clear()
    tela_login.lineEdit_2.clear()


    widget.setCurrentIndex(3)



def fazer_relatorio(caixa_id = False):
    from Core.Admin.Caixa.cupom_recibo import PDF

    #pegar o atual id do caixa ou o id passado pelo usuario

    if not caixa_id:
        id_caixa = get_cur_caixa_id()
    else:
        id_caixa = caixa_id


    banco = sqlite3.connect(fr"{os.getcwd()}\\DataBase\\produtos.db",check_same_thread=False)
    cursor = banco.cursor()

    tabela_teste = cursor.execute(f''' 
    select venda.id,strftime('%d/%m/%Y %H:%M:%S',Data|| ' ' || Hora) ,
ifnull(usuario.usuario,"usuário não informado") as usuario,

(select sum(replace(produtos_vendidos.Quantidade,'x','')) from produtos_vendidos where produtos_vendidos.ID_venda = venda.ID ) as quantidade

,replace(printf("%.2f", venda.Total),'.',',') as total,

replace(printf("%.2f",sum(Pagamento.Valor_Pago)),".",",") as valor_pago ,

replace(printf("%.2f", Troco),'.',',')  as troco from venda

    left join usuario on venda.ID_usuario = usuario.ID
	left join Pagamento on venda.ID = pagamento.ID_venda
	
    where id_caixa = {id_caixa} group by venda.id 
    ''').fetchall()


    ### CRIANDO O OBJETO PDF ###
    pdf = PDF("P", "mm", "Letter", "Relatório de Vendas",id_caixa = id_caixa)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.alias_nb_pages()
    ### Adicionando uma página ###
    pdf.add_page()

    pdf.setar_metodo_mais_vendido()
    pdf.entradas_saidas()

    pdf.set_font("helvetica", "", 20)



    headers =  (0, "Data e Hora", "Usuário", "QTD.", "Total","Valor Pago", "Troco")
    pdf.montador_de_tabela_alunos(tabela_teste, headers,'Vendas')


    pdf.output("relatorio.pdf")






def registrar_entradas_saidas(tipo):

    data_agora=datetime.datetime.now()
    data = data_agora.strftime("%Y-%m-%d")
    hora = data_agora.strftime("%H-%M-%S").replace("-",":")
    id = randint(10000000,99999999)

    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    id_caixa = config["Caixa"]["id"]


    if tipo == "Entrada":
        while True:
    
            if len(cursor.execute(f"select * from Entrada where ID = {id}").fetchall()) == 0:
                break
            else:
                id = randint(1000000000,99999999999)

        if registrar_entrada.lineEdit.text() == "":
            valor = 0.00
        else:
            valor = format(float(registrar_entrada.lineEdit.text().replace(",",".")),".2f")
        pagamento = registrar_entrada.comboBox_2.currentText().upper()
        descricao = registrar_entrada.textEdit.toPlainText()

        cursor.execute("insert into Entrada values(?,?,?,?,?,?,?)",(id,id_caixa,data,hora,pagamento,descricao,valor))
        banco.commit()
        msg = QMessageBox(registrar_entrada)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
        msg.setText(f''' Entrada registrado com sucesso.''')
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Resgistrado")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)  
        msg = msg.exec_()
        registrar_entrada.lineEdit.clear()
        registrar_entrada.textEdit.clear()
        registrar_entrada.close()
        return

    

    elif tipo == "Saida":
        while True:
            if len(cursor.execute(f"select * from Saida where ID = {id}").fetchall()) == 0:
                break
            else:
                id = randint(1000000000,99999999999)

        if resgistrar_saida.lineEdit.text() == "":
            valor = 0.00
        else:
            valor = format(float(resgistrar_saida.lineEdit.text().replace(",",".")),".2f")
        descricao = resgistrar_saida.textEdit.toPlainText()
        cursor.execute("insert into Saida values(?,?,?,?,?,?)",(id,id_caixa,data,hora,descricao,valor))
        banco.commit()

        msg = QMessageBox(resgistrar_saida)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
        msg.setText(f'''  Saida registrado com sucesso.''')
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Resgistrado")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)  
        msg = msg.exec_()
        resgistrar_saida.lineEdit.clear()
        resgistrar_saida.textEdit.clear()
        resgistrar_saida.close()
        return









