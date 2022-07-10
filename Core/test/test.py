from fpdf import FPDF
import datetime , sqlite3,os



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

        metodos_pagamento = cursor.execute(f'''select Metodo_Pagamento, replace(printf("%.2f",sum(Valor_Pago)),".",",")  as valor from Pagamento where ID_venda in 
(select ID from venda where ID_caixa = {self.id_caixa})
group by Metodo_Pagamento''').fetchall()

        self.set_font('helvetica','B',14.0) 
        self.cell(0, 0, "Métodos De Pagameto", align='C')
        self.ln(10)

        self.set_font('helvetica','',10.0) 
        for i in range(len(metodos_pagamento)):
            self.cell(0, 0, f"{metodos_pagamento[i][0]}: {metodos_pagamento[i][1]}", ln = True, align='L')
            self.ln(5)

        self.ln(10)

    def entradas_saidas(self):

        todas_as_coisas = cursor.execute(f''' 
        

with Valor_Pago as (

select ifnull(pagamento.Metodo_Pagamento,"Sem Pagamentos") as Metodo_Pagamento,ifnull(printf("%.2f",sum(Valor_Pago)),0.00) as valor from Pagamento where ID_venda in 
        (select ID from venda where ID_caixa = {self.id_caixa})
		group by Pagamento.Metodo_Pagamento
		
		),
		
Saldo_inicial(saldo) as (
select ifnull(printf("%.2f",Saldo_inicial),0.00) as Saldo_inicial from caixa where id = {self.id_caixa}
),
		

		
total as (
select ifnull(printf("%.2f",sum(Entrada.Valor)),0.00) as entradas , ifnull(printf("%.2f",sum(Saida.Valor)),0.00) as saidas
        from Entrada
        join Saida
        where Entrada.ID_caixa = {self.id_caixa}),

total_do_dia(total) as (

select sum(Valor_Pago.valor) + total.entradas - total.saidas
from Valor_Pago
join total
),

total_no_caixa(valor) as (

select  sum(Valor_Pago.valor) +Saldo_inicial.saldo+ 
total.Entradas - total.saidas
from Valor_Pago
join total
join Saldo_inicial
where Valor_Pago.Metodo_Pagamento = "DINHEIRO"
group by Valor_Pago.Metodo_Pagamento

)
		
select printf("%.2f",sum(Valor_Pago.valor)),total.entradas, total.saidas,Saldo_inicial.saldo,printf("%.2f",total_do_dia.total),printf("%.2f",total_no_caixa.valor) from Valor_Pago
join total
join Saldo_inicial
join total_do_dia
join total_no_caixa

        
        
        
        ''').fetchall()[0]

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




if __name__ == '__main__':

    id_caixa = 96010456
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

