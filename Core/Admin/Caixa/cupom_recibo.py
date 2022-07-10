from load import *



class Recibo:


    def __init__(self,quantidade_itens,quantidade_produtos,Total,Troco,id,forma_de_pagamento,total_recebido,desconto):
        
        self.lista_itens = []

        self.quantidade_itens = quantidade_itens
        self.quantidade_produtos = quantidade_produtos
        self.Total = Total
        self.Troco =Troco
        self.id = id
        self.total_recebido = total_recebido
        self.desconto = desconto
        self.forma_de_pagamento = forma_de_pagamento

        file = f"{c}\DataBase\config.ini"
        informaçoes = ConfigParser()
        informaçoes.read(file)

        #cofig sobre a pagina
        self.page_width = f'{informaçoes["Recibo"]["page_width"]}'
        self.page_height = f'{informaçoes["Recibo"]["page_height"]}'
        self.page_left_margin = f'{informaçoes["Recibo"]["page_left_margin"]}'
        self.page_right_margin = f'{informaçoes["Recibo"]["page_right_margin"]}'
        self.page_top_margin = f'{informaçoes["Recibo"]["page_top_margin"]}'
        self.loja_titulo_font = f'{informaçoes["Recibo"]["loja_titulo_font"]}'
        self.loja_titulo_font_size = f'{informaçoes["Recibo"]["loja_titulo_font_size"]}'
        self.loja_titulo = f'{informaçoes["Recibo"]["loja_titulo"]}'
        self.informacoes_adicionais =json.loads(informaçoes.get("Recibo","informacoes_adicionais"))


        #config sobre as informações da loja
        self.nome_empresa = f'{informaçoes["Recibo"]["nome_empresa"]}'
        self.endereco = f'{informaçoes["Recibo"]["endereco"]}'
        self.endereco_completo = f'{informaçoes["Recibo"]["endereco_completo"]}'
        self.cep = f'{informaçoes["Recibo"]["cep"]}'
        self.tel  = f'{informaçoes["Recibo"]["tel"]}'



    def criar_recibo(self):

        data_agora=datetime.datetime.now()
        data = data_agora.strftime("%d-%m-%y").replace("-","/")
        hora = data_agora.strftime("%H-%M-%S").replace("-",":")
        


        cdir =os.getcwd()
        #logo loja moda do dia
        pdf = FPDF("p","mm",(int(self.page_width),int(self.page_height)))
        pdf.set_left_margin(margin = int(self.page_left_margin))
        pdf.set_right_margin(margin = int(self.page_right_margin))
        pdf.set_top_margin(margin= int(self.page_top_margin))
        tim = "-"

        pdf.add_page()

        #informações sobre a loja

        #logo loja moda do dia
        pdf.set_font(f"arial","b",int(self.loja_titulo_font_size),)
        pdf.cell(0,5,f"{self.loja_titulo}",ln=True,align="C")

        #linha separadora
        pdf.set_font("helvetica","",8,)
        pdf.cell(0,5,f"{tim * 100}",ln=True,align="C")


        #endereço

        pdf.set_font("helvetica","",8,)
        pdf.cell(0,3,f"{self.nome_empresa}",ln=True,align="l")
        pdf.cell(0,3,f"{self.endereco}",ln=True,align="l")
        pdf.cell(0,3,f"{self.endereco_completo}",ln=True,align="l")
        pdf.cell(0,3,f"{self.cep}",ln=True,align="l")
        pdf.cell(0,3,f"{self.tel}",ln=True,align="l")
        pdf.cell(0,3,f"DATA: {data}  {hora}",ln=True,align="l")

        #colocar as categorias para o produto
        pdf.set_font("helvetica","",7,)
        pdf.cell(0,5,f"{tim * 100}",ln=True,align="C")
        pdf.cell(0,8,f"        Cód.         Descrição       QTD    VALOR     DES    TOTAL",ln=True,align="l")
        pdf.cell(0,5,f"{tim * 120}",ln=True,align="C")


        #adicionar os produtos
        i = 0
         #fonte
        pdf.set_font("helvetica","",7)
        for i in range(len(self.lista_itens)):
            codigo = self.lista_itens[i][0]
            codigo = [codigo[index: index + 10 ] for index in range(0,len(codigo),10)]
            
            if len(codigo) == 0:
                codigo.append("")

            pdf.cell(15,4,f"{codigo[0]}",align="L")
            #não deixar o tamanho do nome ser muito alto

            nome = self.lista_itens[i][1]
            nome = [nome[index: index + 15 ] for index in range(0,len(nome),15)]
            
            if len(nome) == 0:
                nome.append("")
                #nome
            pdf.cell(20,4,f"{nome[0]}",align="L")



                #preparando a quantidade de itens
            quan = str(self.lista_itens[i][2].replace("X",""))
            quan = quan.zfill(3)
                #quantidade de itens
            pdf.cell(7,4,f"{quan}",align="L")
                #valor unitario do produto
            pdf.cell(11,4,f"{self.lista_itens[i][3]}",align="L")
                #desconto
            pdf.cell(6,4,f"{self.lista_itens[i][4]}",align="L")
                #valor total do produto
            pdf.cell(19,4,f"{self.lista_itens[i][5]}",ln=True,align="L")

            if len(codigo) > 1 or len(nome) > 1:
                parar = []
                for i in range(1,100):

                    if "code" not in parar:
                        if i < len(codigo):
                            pdf.cell(15,4,f"{codigo[i]}",align="L")
                        else:
                            parar.append("code")
                            pdf.cell(15,4,f"",align="L")
                    else:
                        pdf.cell(15,4,f" ",align="L")

                    if "nome" not in parar:
                        if i < len(nome):
                            pdf.cell(8,4,f"{nome[i]}".lstrip(),align="L")
                        else:
                            parar.append("nome")



                    if len(parar) > 1:
                        pdf.cell(8,4,f"",ln=True,align="L")
                        break
                    pdf.cell(8,4,f"",ln=True,align="L")

            i += 1
            #linha para separar
        pdf.cell(0,5,f"{tim * 150}",ln=True,align="C")

        #final
            #   quantidade total de itens
        pdf.set_font("helvetica","B",7)
        pdf.cell(50,4,f"Qtd.Total de Itens",align="L")
        pdf.set_font("helvetica","",7)
        pdf.cell(0,4,f"{str(self.quantidade_itens).zfill(3)}",ln=True,align="L")
            #   valor total
        pdf.set_font("helvetica","B",7)
        pdf.cell(50,4,f"Valor Total",align="L")
        pdf.set_font("helvetica","",7)
        pdf.cell(0,4,f"{self.Total}",ln=True,align="L")

        #desconto
        pdf.set_font("helvetica","B",7)
        pdf.cell(50,4,f"Desconto",align="L")
        pdf.set_font("helvetica","",7)
        pdf.cell(0,4,f"{self.desconto}",ln=True,align="L")

        pdf.ln(5)

        pdf.cell(50,4,f"Forma de Pagamento",align="L")
        pdf.cell(0,4,f"Valor Pago",ln=True,align="L")

        for i in range(len(self.total_recebido)):
            pdf.cell(50,4,f"-{self.forma_de_pagamento[i][0]}",align="L")
            pdf.cell(0,4,f'R${float(str(self.total_recebido[i]).replace(",",".")):.2f}'.replace(".",","),ln=True,align="L")


        pdf.cell(50,4,f"Troco",align="L")
        pdf.cell(0,4,f"{self.Troco}",ln=True,align="L")
        pdf.cell(0,4,f"ID:{self.id}",ln=True,align="L")
        pdf.cell(0,5,f"{tim * 100}",ln=True,align="C")
        pdf.set_font("helvetica","b",8,)

        pdf.cell(0,4,"Recibo Para Troca",ln=True,align="C")
        pdf.ln(5)
        pdf.set_font("helvetica","b",7,)

        for i in range(len(self.informacoes_adicionais)):
            pdf.cell(0,4,f"*{self.informacoes_adicionais[i]}",ln=True,align="L")
        # pdf.cell(0,4,"*O Produto Deve Estar Em Perfeito Estado",ln=True,align="L")
        # pdf.cell(0,4,"*Apresentar Este Recibo ou Algun Documento Fiscal",ln=True,align="L")
        # pdf.cell(0,4,"*Prazo em Apenas 3 Dias",ln=True,align="L")

        #colocar no final "sem valor fiscal" de cada nota
        pdf.set_font("helvetica","b",8,)
        pdf.cell(0,30,"-------SEM VALOR FISCAL-------",ln=True,align="C")

        output_path = fr"{cdir}\cupom_vendas\Recibos\{self.id}.pdf"
        pdf.output(output_path)

        return output_path

    def add_itens(self,codigo,nome,qtd,valor,des,total):

        self.lista_itens.append([codigo,nome,qtd,valor,des,total])



    def imprimir_cupom(url,impressora = None):

        if impressora == None:
            file = f"{c}\DataBase\config.ini"
            informaçoes = ConfigParser()
            informaçoes.read(file)
            impressora = informaçoes["Config_Impressao"]["impressora_cupom"]

        try:
                              
            win32print.SetDefaultPrinterW(f'{impressora}')
            win32api.ShellExecute(0,"print",url,None,".",0)

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
        


    @classmethod
    def converter_pdf_jpeg(cls,file):
        file = rf"{c}\cupom_vendas\Recibos\{file}.pdf"
        poppler = rf"{c}\cupom_vendas\poppler-0.68.0\bin"

        images = convert_from_path(file,500,poppler_path=poppler) #dpi=200, grayscale=True, size=(300,400), first_page=0, last_page=3)

        for image in images:
            image.save(rf"{file}.jpeg","JPEG")


class PDF(FPDF):
    def __init__(self, orientation='P',unit='mm',format='A4', title="Sem titulo", id_caixa = 1):
        super().__init__(orientation, unit, format)
        self.id_caixa = id_caixa
        self.title = title

    def header(self):
        pass
        # self.set_font("helvetica", "B", 20)
        # self.cell(0, 5, ln=1)
        # self.cell(0, 10, self.title, border=False, ln=1, align="C")
        # self.ln()

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 10)
        self.set_text_color(169,169,169)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', align="C")
        self.set_font("helvetica", "B", 10)
        data = datetime.datetime.now().strftime("Relatório gerado: %d/%m/%Y %H:%M:%S")
        self.cell(0, 10, data, border=False, ln=1, align="R")


    def montador_de_tabela_alunos(self, data2, headers=(), title=""):
        data = data2.copy()
        data.insert(0,headers)

        epw = self.w - 2*self.l_margin
        col_width = epw/4
        th = self.font_size
        self.set_font('helvetica','B',14.0) 
        self.cell(epw, 0.0, title, align='C')
        self.set_font('Times','',10.0) 
        self.ln(4)
        for j, row in enumerate(data):
            for i, datum in enumerate(row):
                if i >= 1:
                    if j == 0:
                        self.set_font('helvetica','B',10.0) 
                    else:
                        self.set_font('Times','',9.0)

                    if i == 2:
                        self.cell(45, 2*th, str(datum), border=1)
                    elif i == 3:
                        self.cell(25, 2*th, str(datum), border=1)

                    elif i == 4:
                        self.cell(35, 2*th, str(datum), border=1)
                    
                    elif i == 5:
                        if len(str(datum)) > 30:
                            self.set_font('Times','',6.7)
                        else:
                            self.set_font('Times','',10.0)
                        if j == 0: 
                            self.set_font('helvetica','B',10.0) 
                        self.cell(30, 2*th, str(datum), border=1)
                    else:
                        self.cell(30, 2*th, str(datum), border=1)
        
            self.ln(2*th)
        self.cell(epw, 6, f'Total de Vendas: {len(data)-1}', align='C')
        self.ln(25)


    def setar_metodo_mais_vendido(self):

        metodos_pagamento = cursor.execute(f'''select  Pagamento.Metodo_Pagamento 
        
        , printf("%.2f",case Pagamento.Metodo_Pagamento  when 'DINHEIRO' then printf("%.2f",sum(Valor_Pago))   -  sum(venda.Troco) else printf("%.2f",sum(Valor_Pago)) end)
		
		from Pagamento 
		left join venda on venda.id = Pagamento.ID_venda
		where ID_venda in 
(select ID from venda where ID_caixa = {self.id_caixa} )
group by Pagamento.Metodo_Pagamento''').fetchall()

        self.set_font('helvetica','B',14.0) 
        self.cell(0, 0, "Métodos De Pagameto", align='L')

        self.set_font('helvetica','B',14.0) 
        self.cell(-35, 0, "Entradas", align='R')
        self.ln(10)

        entradas = cursor.execute(f"select strftime('%d/%m/%Y',data),hora,pagamento,replace(valor,'.',',') from entrada where id_caixa = {self.id_caixa}").fetchall()

        self.set_font('helvetica','',10.0) 

        list_size = len(metodos_pagamento) if len(metodos_pagamento) >= len(entradas) else len(entradas)

        print(list_size)

        for i in range(list_size):

            if i < len(metodos_pagamento):
                self.cell(105, 0, f"{metodos_pagamento[i][0]}: {metodos_pagamento[i][1]}", align='L')
            else:
                self.cell(105, 0,align='L')
            if i < len(entradas):
                self.cell(0, 0, f"{entradas[i][0]} {entradas[i][1]} :  {entradas[i][2]} {entradas[i][3]}", align='L')
            self.ln(5)

        self.ln(10)

    def entradas_saidas(self):

        todas_as_coisas = cursor.execute(f''' 
        

with Valor_Pago as (

select  Pagamento.Metodo_Pagamento 
        
        , case Pagamento.Metodo_Pagamento  when 'DINHEIRO' then ifnull(printf("%.2f",sum(Valor_Pago)),0.00)   -  sum(venda.Troco) else printf("%.2f",sum(Valor_Pago)) end as valor
		
		from Pagamento 
		left join venda on venda.id = Pagamento.ID_venda
		where ID_venda in 
(select ID from venda where ID_caixa = {self.id_caixa} )
group by Pagamento.Metodo_Pagamento
		),
		
Saldo_inicial(saldo) as (
select ifnull(printf("%.2f",Saldo_inicial),0.00) as Saldo_inicial from caixa where id = {self.id_caixa}
),
		

		
total as (
select (select ifnull(printf("%.2f",sum(Entrada.Valor)),0.00) 
        from Entrada
        where Entrada.ID_caixa =  {self.id_caixa}) as entradas ,
        (select ifnull(printf("%.2f",sum(Saida.Valor)),0.00) 
        from Saida
        where Saida.ID_caixa =  {self.id_caixa}) as saidas
        
        ),

total_do_dia(total) as (

select sum(Valor_Pago.valor) + total.entradas - total.saidas
from Valor_Pago
join total
),

total_no_caixa(valor) as (

select  ifnull((select ifnull(sum(Valor_Pago.valor),0.00)
from Valor_Pago
where Valor_Pago.Metodo_Pagamento = "DINHEIRO"
group by Valor_Pago.Metodo_Pagamento
),0.00) + ifnull(Saldo_inicial.saldo,0.00)+ 
ifnull((select sum(Valor) from Entrada where id_caixa = {self.id_caixa} and Pagamento = "DINHEIRO"),0.00) - ifnull(total.saidas,0.00)
from total
join Saldo_inicial)
		
select printf("%.2f",sum(Valor_Pago.valor)),total.entradas, total.saidas,Saldo_inicial.saldo,printf("%.2f",total_do_dia.total),printf("%.2f",total_no_caixa.valor) from Valor_Pago
join total
join Saldo_inicial
join total_do_dia
join total_no_caixa

        
        
        
        ''').fetchall()[0]

        print("todas ", todas_as_coisas)

        self.set_font('helvetica','B',14.0) 
        self.cell(0, 0, "Caixa", align='C')
        self.ln(10)

        self.set_font('helvetica','',10.0) 
        self.cell(0, 0, f"Saldo Inicial: {todas_as_coisas[3]}".replace(".",","), ln = True, align='L')
        self.ln(5)

        self.set_font('helvetica','',10.0) 
        self.cell(0, 0, f"Valor Total Das Vendas: {todas_as_coisas[0]}".replace(".",","), ln = True, align='L')
        self.ln(5)

        self.set_font('helvetica','',10.0) 
        self.cell(0, 0, f"Entradas: {todas_as_coisas[1]}".replace(".",","), ln = True, align='L')
        self.ln(5)

        self.set_font('helvetica','',10.0) 
        self.cell(0, 0, f"Saidas: {todas_as_coisas[2]}".replace(".",","), ln = True, align='L')
        self.ln(5)

        self.set_font('helvetica','',10.0) 
        self.cell(0, 0, f"Total: {todas_as_coisas[4]}".replace(".",","), ln = True, align='L')
        self.ln(5)

        self.set_font('helvetica','',10.0) 
        self.cell(0, 0, f"No Caixa Em Dinheiro: {todas_as_coisas[5]}".replace(".",","), ln = True, align='L')
        self.ln(10)


    