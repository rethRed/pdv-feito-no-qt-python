from load import *


def entraTelaEstatisticas():

    dados = Setar_dados_estatisticas("line", Setar_dados_estatisticas.vendas_hoje)

    estatisticas.showMaximized()

def setar_as_estatisticas():

    estatisticas.stackedWidget.setCurrentIndex(0)



def setar_as_vendas():

    estatisticas.stackedWidget.setCurrentIndex(2)
    data_agora=datetime.datetime.now()

    cur_date= data_agora.strftime("%Y-%m-%d")
    last_date = datetime.datetime.today() - datetime.timedelta(days = 90)
    last_date = last_date.strftime("%Y-%m-%d")


    estatisticas.dateTimeEdit.setDateTime(QDateTime.fromString(f"{cur_date}","yyyy-MM-dd"))
    estatisticas.dateTimeEdit_2.setDateTime(QDateTime.fromString(f"{last_date}","yyyy-MM-dd"))

    pesquisar_venda()



    estatisticas.tableWidget.resizeColumnsToContents()



def pesquisar_venda():
    venda_estatistica.data_vendas.clear()

    estatisticas.tableWidget.setRowCount(0)
    fim = estatisticas.dateTimeEdit.dateTime().addDays(1).toString("yyyy-MM-dd HH:mm")
    comeco  = estatisticas.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd HH:mm")

    print("fim ",fim)
    print("comeco ",comeco)


    cursor_estatistica.execute(f'''
select id, strftime('%d/%m/%Y %H:%M:%S',Data || ' '|| Hora) as horario , Quantidade, Total
from Venda
where datetime(Data || ' '|| Hora) BETWEEN datetime('{comeco}') and datetime('{fim}') order by  datetime(Data || ' '|| Hora) desc

    ''')

    info = cursor.execute(f'''

        select ifnull(sum(Total),0.00),ifnull((julianday('{fim}') - julianday('{comeco}')),0)
        from venda Where Data || ' '|| Hora BETWEEN datetime('{comeco}') and datetime('{fim}')

    ''').fetchall()[0]

    print(info)

    estatisticas.label.setText(f"Ganho: {float(info[0]):.2f}".replace(".",","))
    estatisticas.label_3.setText(f"Distância de {int(info[1])} dias")

    setar_venda_table()



def setar_venda_table():

    needed = 60

    cur_data = cursor_estatistica.fetchmany(needed)

    venda_estatistica.data_vendas = venda_estatistica.data_vendas + cur_data

    rowCount = estatisticas.tableWidget.rowCount()
    try:
        for i in range(0, needed):
            estatisticas.tableWidget.setRowCount(rowCount+i+1)
            for j in range(0, 4):
                estatisticas.tableWidget.setItem(rowCount+i, j, QTableWidgetItem(str(cur_data[i][j]).replace(".",",")))

        return


    except IndexError:
        estatisticas.tableWidget.setRowCount( estatisticas.tableWidget.rowCount() - 1)
        print("=====================")
        print("IndexError Because There is No Data to Get From Table")
        print("=====================")
        return



class venda_estatistica():

    data_vendas = []
    cur_id_venda = 0
    function_excluir = None

    def __init__(self,row = 0 ,function_excluir = None):

        venda_estatistica.function_excluir = function_excluir
        venda_estatistica.cur_id_venda = self.data_vendas[row][0]
        self.setar_info()


    @classmethod
    def execute(cls):

        estastiticas_venda.exec_()
        venda_estatistica.function_excluir = None
        estastiticas_venda.listWidget.clear()



    def setar_info(self):

        venda_info = cursor.execute(f'''

        select ifnull(Usuario.usuario,'Sem Usuário'),quantidade,Desconto, strftime('%d/%m/%Y %H:%M:%S',Data ||' '|| Hora)
        ,Total, Troco

        from Venda
        left join Usuario  on venda.ID_usuario = Usuario.ID

        where Venda.id = {self.cur_id_venda}
        ''').fetchall()[0]


        pagamento_info = cursor.execute(f'''
        SELECT Metodo_Pagamento, Valor_Pago ,Parcelas
        from Pagamento
        where ID_venda = {self.cur_id_venda}
        ''').fetchall()


        produtos_vendidos_info = cursor.execute(f'''
        SELECT ifnull(Codigo_Produtos.Codigo,produtos_vendidos.Codigo) codigo,
		ifnull(Produtos.Nome,produtos_vendidos.Nome),
		produtos_vendidos.Quantidade,produtos_vendidos.preco,
		produtos_vendidos.Desconto,produtos_vendidos.Total


from produtos_vendidos
left join Codigo_Produtos on produtos_vendidos.ID_Codigo = Codigo_Produtos.ID
left join Produtos on produtos_vendidos.ID_produto = Produtos.ID

where produtos_vendidos.ID_venda = {self.cur_id_venda}
        ''').fetchall()


        valor_pago_info = cursor.execute(f'''
        SELECT sum(Valor_Pago)
        from Pagamento
        where ID_venda = {self.cur_id_venda}
        ''').fetchall()[0][0]



        #setar os produtos vendidos na table widget
        estastiticas_venda.tableWidget.setRowCount(len(produtos_vendidos_info))
        estastiticas_venda.tableWidget.setColumnCount(6)

        for i in range(0, len(produtos_vendidos_info)):
            for j in range(0,6):
                estastiticas_venda.tableWidget.setItem(i,j , QtWidgets.QTableWidgetItem(str(produtos_vendidos_info[i][j])))

        #setar as info de vendas e de pagamento

        estastiticas_venda.label_5.setText(f"{venda_info[0]}")
        estastiticas_venda.label_2.setText(f"{venda_info[3]}")
        estastiticas_venda.label_8.setText(f"{float(venda_info[4]):.2f}".replace(".",","))
        estastiticas_venda.label_7.setText(f"{venda_info[2]}")
        estastiticas_venda.label_13.setText(f"{float(valor_pago_info):.2f}".replace(".",","))
        estastiticas_venda.label_10.setText(f"{float(venda_info[5]):.2f}".replace(".",","))

        #setar os metodos de pagamentos usados

        for i in range(len(pagamento_info)):
            if pagamento_info[i][2] != None:
                estastiticas_venda.listWidget.addItem(f"{pagamento_info[i][0]} {pagamento_info[i][2]} {float(pagamento_info[i][1]):.2f}".replace(".",",") )
                continue
            estastiticas_venda.listWidget.addItem(f"{pagamento_info[i][0]} {float(pagamento_info[i][1]):.2f}".replace(".",","))

        estastiticas_venda.tableWidget.resizeColumnsToContents()


    def excluir_vendas(self):
        from Core.Admin.Caixa.caixa import refechar_caixa

        id_caixa = cursor.execute(f"select id_caixa from venda where id = {venda_estatistica.cur_id_venda}").fetchall()[0][0]
        cursor.execute(f"delete from venda where id = { venda_estatistica.cur_id_venda}")
        banco.commit()


        estastiticas_venda.close()

        refechar_caixa(id_caixa)

        if venda_estatistica.function_excluir != None:
            venda_estatistica.function_excluir()



        msg = QMessageBox(Tela_registro_vendas)
        msg.setStyleSheet('background-color:#34495e;font: 75 10pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);')
        msg.setText(f'''Venda Cancelada com sucesso''')
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Cancelado.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg = msg.exec_()


    def trocar_venda(self):

        class ProdutosTrocar:
            
            def __init__(self):
                self.produtos_info = cursor.execute(f'''
                SELECT ifnull(Codigo_Produtos.Codigo,produtos_vendidos.Codigo) codigo,
                ifnull(Produtos.Nome,produtos_vendidos.Nome),
                produtos_vendidos.Quantidade,produtos_vendidos.preco,
                produtos_vendidos.Desconto,produtos_vendidos.Total


            from produtos_vendidos
            left join Codigo_Produtos on produtos_vendidos.ID_Codigo = Codigo_Produtos.ID
            left join Produtos on produtos_vendidos.ID_produto = Produtos.ID

            where produtos_vendidos.ID_venda = {venda_estatistica.cur_id_venda}
                    ''').fetchall()

                trocar_venda_vendas_view_estatisticas.tableWidget.setRowCount(len(self.produtos_info))
                trocar_venda_vendas_view_estatisticas.tableWidget.setColumnCount(6)
                
                for i in range(0, len(self.produtos_info)):
                    for j in range(0,6):
                        trocar_venda_vendas_view_estatisticas.tableWidget.setItem(i,j , QtWidgets.QTableWidgetItem(str(self.produtos_info[i][j])))

                trocar_venda_vendas_view_estatisticas.tableWidget.resizeColumnsToContents()

                trocar_venda_vendas_view_estatisticas.tableWidget.itemClicked.connect(self.selecionar_produtos)
                trocar_venda_vendas_view_estatisticas.lineEdit.returnPressed.connect(self.pesquisar_produtos)
                trocar_venda_vendas_view_estatisticas.pushButton_pesquisar.clicked.connect(self.pesquisar_produtos)
                trocar_venda_vendas_view_estatisticas.pushButton_adicionar.clicked.connect(self.adicionar_produtos)
                trocar_venda_vendas_view_estatisticas.listWidget.itemDoubleClicked.connect(self.apagar)
                trocar_venda_vendas_view_estatisticas.pushButton_2.clicked.connect(self.salvar)

                self.produtos_selecionados = []
                self.produtos_adicionados = []
                self.produtos_a_adicionar = None
                self.valor_total_produtos_a_trocar = 0.00
                self.valor_total_produtos = 0.00


            def selecionar_produtos(self):
                self.produtos_selecionados.clear()
                len_produtos = trocar_venda_vendas_view_estatisticas.tableWidget.rowCount()

                for i in range(len_produtos):
                    if trocar_venda_vendas_view_estatisticas.tableWidget.item(i,0).isSelected(): 
                        self.produtos_selecionados.append(i)

                self.valor_total_produtos = 0.00
                for i in range(len(self.produtos_selecionados)):
                    self.valor_total_produtos += float(str(self.produtos_info[self.produtos_selecionados[i]][3]).replace(",","."))

                distancia_valor = self.valor_total_produtos_a_trocar - self.valor_total_produtos

                trocar_venda_vendas_view_estatisticas.label.setText(f"{self.valor_total_produtos:.2f}".replace(".",","))
                trocar_venda_vendas_view_estatisticas.label_15.setText(f"{distancia_valor:.2f}".replace(".",","))

            def apagar(self):
                index = trocar_venda_vendas_view_estatisticas.listWidget.currentRow()
                trocar_venda_vendas_view_estatisticas.listWidget.takeItem(index)
                del self.produtos_adicionados[index]
                distancia_valor = self.valor_total_produtos_a_trocar - self.valor_total_produtos

                self.valor_total_produtos_a_trocar = 0.00
                for i in range(len(self.produtos_adicionados)):
                    self.valor_total_produtos_a_trocar += float(self.produtos_adicionados[i][2])

                self.valor_total_produtos = 0.00
                for i in range(len(self.produtos_selecionados)):
                    self.valor_total_produtos += float(str(self.produtos_info[self.produtos_selecionados[i]][3]).replace(",","."))


                distancia_valor = self.valor_total_produtos_a_trocar - self.valor_total_produtos
                trocar_venda_vendas_view_estatisticas.label_15.setText(f"{distancia_valor:.2f}".replace(".",","))
                trocar_venda_vendas_view_estatisticas.label_4.setText(f"{self.valor_total_produtos_a_trocar:.2f}".replace(".",","))

            def pesquisar_produtos(self):
                asp = "'"
                try:

                    codigo = trocar_venda_vendas_view_estatisticas.lineEdit.text()

                    #buscar no banco de dados
                    sql=f"select Codigo_Produtos.codigo, Produtos.Nome,Produtos.preco from Codigo_Produtos join Produtos on Codigo_Produtos.id_produtos = Produtos.id where codigo = {asp+str(codigo)+asp}"
                    dados = cursor.execute(sql).fetchall()
                    print(dados)
                    # se codigo não esta cadastrado, o tamanho de "dados" sera 0
                    # e será informado que o codigo não existe
                    if len(dados) == 0:
                        trocar_venda_vendas_view_estatisticas.textEdit.setStyleSheet("color: rgb(255, 0, 0);border:none;")
                        trocar_venda_vendas_view_estatisticas.textEdit.setText("Código não encontrado :(")
                        self.produtos_a_adicionar = None
                    else:
                        trocar_venda_vendas_view_estatisticas.textEdit.setStyleSheet("color: rgb(85, 255, 0);border:none;")
                        self.produtos_a_adicionar = dados.copy()[0]
                        trocar_venda_vendas_view_estatisticas.textEdit.setText(f"{dados[0][0]}   {dados[0][1]} {dados[0][2]}")

                except:
                    return

            def adicionar_produtos(self):

                if self.produtos_a_adicionar == None:
                    return
                trocar_venda_vendas_view_estatisticas.stackedWidget.setCurrentIndex(0)
                self.produtos_adicionados.append(self.produtos_a_adicionar)

                self.valor_total_produtos_a_trocar = 0.00
                for i in range(len(self.produtos_adicionados)):
                    self.valor_total_produtos_a_trocar += float(self.produtos_adicionados[i][2])

                distancia_valor = self.valor_total_produtos_a_trocar - self.valor_total_produtos

                trocar_venda_vendas_view_estatisticas.listWidget.addItem(f"{self.produtos_a_adicionar[0]}   {self.produtos_a_adicionar[1]} {self.produtos_a_adicionar[2]}")

                trocar_venda_vendas_view_estatisticas.label_4.setText(f"{self.valor_total_produtos_a_trocar:.2f}".replace(".",","))
                trocar_venda_vendas_view_estatisticas.label_15.setText(f"{distancia_valor:.2f}".replace(".",","))

            def salvar(self):
                print(self.produtos_info)
                for i in range(len(self.produtos_selecionados)):
                    cursor.execute(f''' 
                    {self.produtos_selecionados}
                    ''')

                banco.commit()


        produto = ProdutosTrocar()
        trocar_venda_vendas_view_estatisticas.exec_()



trocar_venda_vendas_view_estatisticas.pushButton.clicked.connect(lambda:trocar_venda_vendas_view_estatisticas.stackedWidget.setCurrentIndex(1))
trocar_venda_vendas_view_estatisticas.pushButton_3.clicked.connect(lambda:trocar_venda_vendas_view_estatisticas.stackedWidget.setCurrentIndex(0))

class Setar_dados_estatisticas():

    def __init__(self,tipo,function = None):

        for i in range(estatisticas.gridLayout_3.count()): estatisticas.gridLayout_3.itemAt(i).widget().close()


        if tipo == "line":

            self.canvas = FigureCanvas(plt.Figure(figsize=(15,6),facecolor= "#2e3349"))
            estatisticas.gridLayout_3.addWidget(self.canvas)
            function(self)
            return

        elif tipo == "pie":

            function(self)
            return

        else:
            print("tipo nao indentificado")
            return


        estatisticas.gridLayout_3.addWidget( self.canvas)


    def show_annotation(sel):
        pass

    def vendas_hoje(self):

        vendas = self.retornar_vendas("hoje")

        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][2]))

        ax =  self.canvas.figure.subplots()
        ax.plot(week, valores, marker="o")

        mplcursors.cursor(ax,hover=True)

    def vendas_semana(self):
        vendas = self.retornar_vendas("semana")

        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][2]))

        ax =  self.canvas.figure.subplots()
        ax.plot(week, valores, marker="o")

        mplcursors.cursor(ax,hover=True)


    def vendas_mes(self):
        vendas = self.retornar_vendas("mes")



        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][1]))

        ax =  self.canvas.figure.subplots()
        ax.plot(week, valores, marker="o")

        mplcursors.cursor(ax,hover=True)



    def vendas_ano(self):
        vendas = self.retornar_vendas("ano")

        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][2]))

        ax =  self.canvas.figure.subplots()

        ax.plot(week, valores, marker="o")

        ##ax.bar(week, valores) usar barras

        mplcursors.cursor(ax,hover=True)


    def vendas_usuario_hoje(self):
        vendas = self.retornar_vendas_usuario("hoje")

        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][1]))

        ax =  self.canvas.figure.subplots()

        ax.bar(week, valores)

        mplcursors.cursor(ax,hover=True)



    def vendas_usuario_semana(self):
        vendas = self.retornar_vendas_usuario("semana")

        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][1]))

        ax =  self.canvas.figure.subplots()

        ax.bar(week, valores)

        mplcursors.cursor(ax,hover=True)

    def vendas_usuario_mes(self):
        vendas = self.retornar_vendas_usuario("mes")

        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][1]))

        ax =  self.canvas.figure.subplots()

        ax.bar(week, valores)

        mplcursors.cursor(ax,hover=True)


    def vendas_usuario_ano(self):
        vendas = self.retornar_vendas_usuario("ano")

        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][1]))

        ax =  self.canvas.figure.subplots()

        ax.bar(week, valores)

        cur = mplcursors.cursor(ax,hover=True)







    def pagamento_hoje(self):
        vendas = self.retornar_pagamento("hoje")

        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][1]))

        ax =  self.canvas.figure.subplots()

        ax.bar(week, valores)

        mplcursors.cursor(ax,hover=True)

    def pagamento_semana(self):
        vendas = self.retornar_pagamento("semana")

        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][1]))

        ax =  self.canvas.figure.subplots()

        ax.bar(week, valores)

        mplcursors.cursor(ax,hover=True)


    def pagamento_mes(self):
        vendas = self.retornar_pagamento("mes")

        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][1]))

        ax =  self.canvas.figure.subplots()

        ax.bar(week, valores)

        mplcursors.cursor(ax,hover=True)


    def pagamento_ano(self):
        vendas = self.retornar_pagamento("ano")

        valores = []
        week = []

        for i in range(len(vendas)):
            week.append(vendas[i][0])
            valores.append(float(vendas[i][1]))

        ax =  self.canvas.figure.subplots()

        ax.bar(week, valores)

        mplcursors.cursor(ax,hover=True)


    def retornar_vendas(self,data = "hoje"):


        dias = cursor.execute('''

        with RECURSIVE Total_caixa (total_do_caixa,data_fechamento) as (

            SELECT replace(ifnull(tota_do_dia,0.00),",","."),data_fechamento
            from caixa where data_fechamento BETWEEN datetime("now","LocalTime","-6 days") and  datetime("now","LocalTime") GROUP by data_fechamento


        ),

        dates(cur_date) AS (
        VALUES(date("now","localtime"))
        UNION ALL
        SELECT date(cur_date, '-1 day')
        FROM dates
        WHERE cur_date > date("now","localtime", '-6 days')
        ) ,


        week_days(dias_das_semanas,cur_date) AS (

            SELECT case cast(strftime('%w',  cur_date) as interger)

            when 0 then 'Dom'
            when 1 then 'Seg'
            when 2 then 'Ter'
            when 3 then 'Qua'
            when 4 then 'Qui'
            when 5 then 'Sex'
            else 'Sáb' end  , cur_date

            from dates

        ),

        dados as (

        select week_days.dias_das_semanas,strftime('%d/%m/%Y', week_days.cur_date) as cur_date,
        ifnull(Total_caixa.total_do_caixa,0.00) as total_do_caixa,Total_caixa.data_fechamento from week_days
        left outer join  Total_caixa on cur_date = data_fechamento
        )




        select * from dados order by cur_date

            ''').fetchall()


        if data == "hoje":

            hoje = '''

	with dates(cur_date) AS (
        VALUES(datetime("now","localtime", 'start of day','+23 hours'))
        UNION ALL
        SELECT datetime(cur_date, '-1 hour')
        FROM dates
        WHERE cur_date > datetime("now","localtime", 'start of day')
        ) ,


	 Total_caixa(hora_venda,total_do_caixa) as (

			select dates.cur_date as cur_vendas_date,sum(Venda.Total) as venda_total from Venda
			left outer join dates on strftime('%H',Venda.Hora) = strftime('%H',dates.cur_date)

			where Data = date('now',"localtime")
			group by dates.cur_date

        ),





        dados as (

        select strftime('%H',dates.cur_date) || "H" as horas,dates.cur_date,ifnull(Total_caixa.total_do_caixa,0.00),Total_caixa.hora_venda from dates
        left outer join  Total_caixa on strftime('%H',dates.cur_date) = strftime('%H',Total_caixa.hora_venda)
        )




        select * from dados order by horas


                    '''

            return cursor.execute(hoje).fetchall()


        elif data == "semana":
            semana = '''
            with RECURSIVE Total_caixa (total_do_caixa,data_fechamento) as (

            SELECT sum(replace(ifnull(Total,0.00),",",".")),Data
            from Venda where Data BETWEEN datetime("now","LocalTime","-7 days") and  datetime("now","LocalTime") GROUP by Data


        ),

        dates(cur_date) AS (
        VALUES(date("now","localtime"))
        UNION ALL
        SELECT date(cur_date, '-1 day')
        FROM dates
        WHERE cur_date > date("now","localtime", '-6 days')
        ) ,


        week_days(dias_das_semanas,cur_date) AS (

            SELECT case cast(strftime('%w',  cur_date) as interger)

            when 0 then 'Dom'
            when 1 then 'Seg'
            when 2 then 'Ter'
            when 3 then 'Qua'
            when 4 then 'Qui'
            when 5 then 'Sex'
            else 'Sáb' end  , cur_date

            from dates

        ),

        dados as (

        select week_days.dias_das_semanas,strftime('%d/%m/%Y', week_days.cur_date) as cur_date,
        ifnull(Total_caixa.total_do_caixa,0.00) as total_do_caixa,Total_caixa.data_fechamento from week_days
        left outer join  Total_caixa on cur_date = data_fechamento
        )




        select * from dados order by cur_date
                    '''


            return cursor.execute(semana).fetchall()


        elif data == "mes":

            mes = '''

     with  data_mes(cur_date) AS (
        VALUES(date("now","localtime",'start of month','+1 month','-1 second'))
        UNION ALL
        SELECT date(cur_date, '-1 day')
        FROM  data_mes
        WHERE cur_date > date("now","localtime", 'start of month')

        ),


total_dia(data,total) as (

select Data,sum(total)
from Venda
where Data BETWEEN date("now","start of month") and date("now","start of month","+1 month")
GROUP by Data

)
select strftime("%d",data_mes.cur_date),ifnull(total_dia.total,0.00)
from data_mes
left join total_dia on total_dia.data = data_mes.cur_date order by data_mes.cur_date



                    '''


            return cursor.execute(mes).fetchall()



        elif data == "ano":
            ano = '''


with venda_range as (
select date('now','localtime','start of year') as data_search

UNION ALL

select date(data_search,'+1 month') from venda_range where data_search < date('now','localtime','start of year','+11 months')
)

select case cast(strftime('%m' , data_search) as INTEGER)

when 1 then 'Jan'
when 2 then 'Fev'
when 3 then 'Mar'
when 4 then 'Abr'
when 5 then 'Maio'
when 6 then 'jun'
when 7 then 'Jul'
when 8 then 'Ago'
when 9 then 'Set'
when 10 then 'Out'
when 11 then 'Nov'
when 12 then 'Dez'

end as meses,

resultados.mes, ifnull(resultados.total_do_mes,0.00)

from venda_range

left join
(select case cast(strftime('%m' , Venda.Data) as INTEGER)

when 1 then 'Jan'
when 2 then 'Fev'
when 3 then 'Mar'
when 4 then 'Abr'
when 5 then 'Maio'
when 6 then 'jun'
when 7 then 'Jul'
when 8 then 'Ago'
when 9 then 'Set'
when 10 then 'Out'
when 11 then 'Nov'
when 12 then 'Dez'

end as mes

,sum(Total)  as total_do_mes

from Venda
group by strftime('%m' , Venda.Data)) as resultados on resultados.mes = meses





                    '''


            return cursor.execute(ano).fetchall()


    @classmethod
    def retornar_vendas_usuario(cls,data = "hoje"):



        if data == "hoje":
            hoje = '''

            select Usuario.usuario,user_info.total
        from Usuario
        join
        (select ID_usuario, sum(Total) as total
        from venda where Data = date("now","localtime")

        group by ID_usuario) as user_info

        on usuario.ID = user_info.ID_usuario


            '''


            return cursor.execute(hoje).fetchall()


        elif data == "semana":
            semana = '''select Usuario.usuario,user_info.total
        from Usuario
        join
        (select ID_usuario, sum(Total) as total
        from venda where Data BETWEEN datetime("now","LocalTime","-7 days") and  datetime("now","LocalTime")

        group by ID_usuario) as user_info

        on usuario.ID = user_info.ID_usuario'''

            return cursor.execute(semana).fetchall()


        elif data == "mes":
            mes = '''

            select Usuario.usuario,user_info.total
        from Usuario
        join
        (select ID_usuario, sum(Total) as total
        from venda where Data BETWEEN date('now','localtime','start of month') and date('now','localtime','start of month','+1 month','-1 second')

        group by ID_usuario) as user_info

        on usuario.ID = user_info.ID_usuario


            '''

            return cursor.execute(mes).fetchall()


        elif data == "ano":

            ano = '''

            select Usuario.usuario,user_info.total
        from Usuario
        join
        (select ID_usuario, sum(Total) as total
        from venda where Data BETWEEN date('now','localtime','start of year') and date('now','localtime','start of year','+1 year','-1 second')

        group by ID_usuario) as user_info

        on usuario.ID = user_info.ID_usuario



            '''


            return cursor.execute(ano).fetchall()


    @classmethod
    def retornar_pagamento(cls,data = "hoje"):

        if data == "hoje":

            hoje = '''
            select Metodo_Pagamento,count(Metodo_Pagamento)
    from Pagamento
    where ID_venda in (

    select ID
    from venda
    where Data = date('now','localtime')
    )
    group by Metodo_Pagamento


            '''

            return cursor.execute(hoje).fetchall()


        elif data == "semana":
            semana = '''select Metodo_Pagamento,count(Metodo_Pagamento)
from Pagamento
where ID_venda in (

select ID
from venda
where Data BETWEEN datetime("now","LocalTime","-6 days") and  datetime("now","LocalTime")
)
group by Metodo_Pagamento'''


            return cursor.execute(semana).fetchall()

        elif data == "mes":

            mes = '''

select Metodo_Pagamento,count(Metodo_Pagamento)
from Pagamento
where ID_venda in (

select ID
from venda
where Data BETWEEN date('now','localtime','start of month') and date('now','localtime','start of month','+1 month','-1 second')
)
group by Metodo_Pagamento



            '''

            return cursor.execute(mes).fetchall()
        elif data == "ano":

            ano = '''
            select Metodo_Pagamento,count(Metodo_Pagamento)
from Pagamento
where ID_venda in (

select ID
from venda
where Data BETWEEN date('now','localtime','start of year') and date('now','localtime','start of year','+1 year','-1 second')
)
group by Metodo_Pagamento



            '''


            return cursor.execute(ano).fetchall()




def setar_historico_caixa():


    estatisticas.stackedWidget.setCurrentIndex(0)
    data_agora=datetime.datetime.now()

    cur_date= data_agora.strftime("%Y-%m-%d")
    last_date = datetime.datetime.today() - datetime.timedelta(days = 90)
    last_date = last_date.strftime("%Y-%m-%d")


    estatisticas.dateTimeEdit_4.setDateTime(QDateTime.fromString(f"{cur_date}","yyyy-MM-dd"))


    estatisticas.dateTimeEdit_3.setDateTime(QDateTime.fromString(f"{last_date}","yyyy-MM-dd"))


    pesquisar_caixa()

    estatisticas.tableWidget_2.resizeColumnsToContents()






def pesquisar_caixa():
    caixa_estatistica.data_caixa.clear()

    estatisticas.tableWidget_2.setRowCount(0)
    fim = estatisticas.dateTimeEdit_4.dateTime().addDays(1).toString("yyyy-MM-dd HH:mm")
    comeco  = estatisticas.dateTimeEdit_3.dateTime().toString("yyyy-MM-dd HH:mm")

    print("fim ",fim)
    print("comeco ",comeco)


    cursor_estatistica.execute(f'''

select caixa.id, strftime('%d/%m/%Y %H:%M',data_abertura || ' '|| hora_abertura) ,ifnull(strftime('%d/%m/%Y %H:%M',data_fechamento || ' '|| hora_fechamento),'Caixa Ativo'),
ifnull(count(Venda.id),0),ifnull(sum(Venda.Quantidade),0), caixa.tota_do_dia
from caixa
join Venda on Venda.id_caixa = caixa.ID
where datetime(data_abertura || ' '|| hora_abertura) BETWEEN datetime('{comeco}') and datetime('{fim}')
group by caixa.id order by
datetime(data_abertura || ' '|| hora_abertura) desc

    ''')

    info = cursor.execute(f'''

        select ifnull(sum(tota_do_dia),0.00),ifnull((julianday('{fim}') - julianday('{comeco}')),0)
        from caixa Where data_abertura || ' '|| hora_abertura BETWEEN datetime('{comeco}') and datetime('{fim}')

    ''').fetchall()[0]

    print(info)

    estatisticas.label_5.setText(f"Ganho: {float(info[0]):.2f}".replace(".",","))
    estatisticas.label_6.setText(f"Distância de {int(info[1])} dias")

    setar_caixa_table()



def setar_caixa_table():

    needed = 60

    cur_data = cursor_estatistica.fetchmany(needed)

    caixa_estatistica.data_caixa = caixa_estatistica.data_caixa + cur_data

    rowCount = estatisticas.tableWidget_2.rowCount()
    try:
        for i in range(0, needed):
            estatisticas.tableWidget_2.setRowCount(rowCount+i+1)
            for j in range(0, 6):
                estatisticas.tableWidget_2.setItem(rowCount+i, j, QTableWidgetItem(str(cur_data[i][j]).replace(".",",")))

        return


    except IndexError:
        estatisticas.tableWidget_2.setRowCount( estatisticas.tableWidget_2.rowCount() - 1)
        print("=====================")
        print("IndexError Because There is No Data to Get From Table")
        print("=====================")
        return

class caixa_estatistica():

    data_caixa = []
    cur_id_caixa = 0
    row = 0

    def __init__(self,row = None ):

        if row != None:
            caixa_estatistica.row = row

        caixa_estatistica.cur_id_caixa = self.data_caixa[caixa_estatistica.row][0]
        caixa_estatistica.setar_info()


    @classmethod
    def execute(cls):
        from Core.Admin.Caixa.caixa import fazer_relatorio

        fazer_relatorio(caixa_estatistica.cur_id_caixa)

        caixa_estatistica_view.exec_()
        caixa_estatistica.limpar()

    @classmethod
    def limpar(cls):
        caixa_estatistica_view.listWidget_pagamentos.clear()
        caixa_estatistica_view.listWidget_vendas.clear()
        venda_estatistica.data_vendas.clear()

    @classmethod
    def setar_info(cls):

        info_caixa = cursor.execute(f'''

        select strftime('%d/%m/%Y %H:%M',data_abertura||" "||hora_abertura), strftime('%d/%m/%Y %H:%M',data_fechamento||" "||hora_fechamento),
        total_dinheiro,total_cartao_debito,total_cartao_credito,total_pix,total_outros,total_entrada,total_saida,
        total_itens_vendidos,tota_do_dia
        from caixa where id = {caixa_estatistica.cur_id_caixa}
        ''').fetchall()[0]

        try:
            caixa_estatistica_view.label_abertura.setText(f"Abertura: {info_caixa[0]}")
            caixa_estatistica_view.label_fechamento.setText(f"Fechamento: {info_caixa[1]}")
            caixa_estatistica_view.label_total_entradas.setText(f"Entradas: {float(info_caixa[7]):.2f}".replace(".",","))
            caixa_estatistica_view.label_total_saidas.setText(f"Saidas: {float(info_caixa[8]):.2f}".replace(".",","))
            caixa_estatistica_view.label_total_de_tudo.setText(f"Total: {float(info_caixa[10]):.2f}".replace(".",","))
            # caixa_estatistica_view..setText(f"{info_caixa[0]}")
            
            caixa_estatistica_view.listWidget_pagamentos.addItem(f"DINHEIRO: {float(info_caixa[2]):.2f}".replace(".",","))
            caixa_estatistica_view.listWidget_pagamentos.addItem(f"CARTÃO DE DÉBITO: {float(info_caixa[3]):.2f}".replace(".",","))
            caixa_estatistica_view.listWidget_pagamentos.addItem(f"CARTTÃO DE CRÉDITO: {float(info_caixa[4]):.2f}".replace(".",","))
            caixa_estatistica_view.listWidget_pagamentos.addItem(f"PIX: {float(info_caixa[5]):.2f}".replace(".",","))
            caixa_estatistica_view.listWidget_pagamentos.addItem(f"OUTROS: {float(info_caixa[6]):.2f}".replace(".",",")) 
        except ValueError:
            pass

        
        venda_estatistica.data_vendas = cursor.execute(f'''
        
        select Id,strftime('%d/%m/%Y %H:%M',Data||" "||Hora), quantidade, replace(total,'.',',' )
        from venda where id_caixa = {caixa_estatistica.cur_id_caixa}
        ''').fetchall()

        for i in range(len(venda_estatistica.data_vendas)):
            caixa_estatistica_view.listWidget_vendas.addItem(f"{venda_estatistica.data_vendas[i][1]}| Qtd. {venda_estatistica.data_vendas[i][2]}| Total: {venda_estatistica.data_vendas[i][3]}")

        total_vendidos = cursor.execute(f"select ifnull(sum(total),0.00) from venda where id_caixa = {caixa_estatistica.cur_id_caixa}").fetchall()[0][0]

        caixa_estatistica_view.label_total_todas_vendas.setText(f"Total: {float(total_vendidos):.2f}".replace(".",","))
        caixa_estatistica_view.label_total_vendas.setText(f"Total Das Vendas: {float(total_vendidos):.2f}".replace(".",","))


    @classmethod
    def reseta_janela(cls):
        from Core.Admin.Caixa.caixa import fazer_relatorio
        fazer_relatorio(caixa_estatistica.cur_id_caixa)
        pesquisar_caixa()
        caixa_estatistica.limpar()
        caixa_estatistica.setar_info()


caixa_estatistica_view.listWidget_vendas.itemClicked.connect(lambda: venda_estatistica(caixa_estatistica_view.listWidget_vendas.currentRow(),function_excluir= caixa_estatistica.reseta_janela).execute())




def ir_config_estatisticas():
    estatisticas.stackedWidget.setCurrentIndex(3)
    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    estatisticas.lineEdit.setText(f'{config["config_estatistica"]["dos_ultimos_x_dias"]}')
    estatisticas.lineEdit_2.setText(f'{config["config_estatistica"]["limite_ver_mais_vendidas"]}')



def setar_config_dias_atras():
    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    if estatisticas.lineEdit.text() == "":
        return

    config["config_estatistica"]["dos_ultimos_x_dias"] =  estatisticas.lineEdit.text()

    with open(file, 'w') as configfile:
        config.write(configfile)

def setar_config_limite_estatistica():
    file = f"{c}\DataBase\Config.ini"
    config = ConfigParser()
    config.read(file)

    if estatisticas.lineEdit_2.text() == "":
        return

    config["config_estatistica"]["limite_ver_mais_vendidas"] =  estatisticas.lineEdit_2.text()

    with open(file, 'w') as configfile:
        config.write(configfile)
















