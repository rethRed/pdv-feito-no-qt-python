


from load import *
from Core.vendas.tela_vendas import *
from Core.vendas.sub_total import *
from Core.Admin.tela_login import *
from Core.Admin.Caixa.caixa import *
from Core.Admin.tela_admin import *
from Core.Admin.Caixa.gerenciamento_caixa import *
from Core.Admin.estatisticas import *

#tela admin

def inicio(button = "nothing"):



    def limpar_config():
        tela_admin.listWidget_permissoes.clear()
        tela_admin.listWidget_usuario.clear()
        
    def limpar_config_analize():
        tela_admin.listWidget_produtos_mais_vendidos.clear()
        tela_admin.listWidget_marcas_mais_vendidas.clear()
        tela_admin.listWidget_grades_mais_vendidas.clear()
        tela_admin.listWidget_variacoes_mais_vendidas.clear()




    if button != "config":
        limpar_config()
        tela_admin.tabWidget_config.setCurrentIndex(0)

    if button == "inicio":
        
        height = tela_admin.pushButton_inicio.height()
        inicio_pos = tela_admin.pushButton_inicio.pos()
        tela_admin.widget_select_nav.setGeometry(inicio_pos.x(),inicio_pos.y(),3,height)
        tela_admin.stackedWidget.setCurrentIndex(0)

    elif button == "analize":



        limpar_config_analize()

        file = f"{c}\DataBase\Config.ini"
        config = ConfigParser()
        config.read(file)

        
        if not config.has_section("config_estatistica"):
            config.add_section("config_estatistica")
            config.set("config_estatistica", "dos_ultimos_x_dias","30")

            with open(file, 'w') as configfile:
                config.write(configfile)
            file = f"{c}\DataBase\Config.ini"
            config = ConfigParser()
            config.read(file)

        limite = config["config_estatistica"]["limite_ver_mais_vendidas"]

        id_caixa = config["Caixa"]["id"]

        dias_atras = config["config_estatistica"]["dos_ultimos_x_dias"]

        ganhos = cursor.execute(f'select ifnull((select sum(replace(total,",",".")) from venda where data BETWEEN datetime("now","LocalTime","-{dias_atras} days") and  datetime("now","LocalTime")),0.00)').fetchall()[0][0]

        media_diaria = cursor.execute(f'select ifnull((select  avg( total) FROM (SELECT sum(replace(total,",",".")) as total from venda where data BETWEEN datetime("now","LocalTime","-{dias_atras} days") and  datetime("now","LocalTime") GROUP by Data)),0.00)').fetchall()[0][0]

        #meu deus, não sei até hoje pq eu  nao usei wiht class, seria tão mais facil
        produtos_mais_vendidos = cursor.execute(f'''
       select cnt ,  ifnull(Produtos.Nome,Nome_prod_venda)     from 
    (select ID_produto as product,count(*) as cnt, Nome as Nome_prod_venda   from produtos_vendidos where ID_venda in
    (select ID from Venda where id_caixa in
    (select ID from caixa where data_fechamento BETWEEN datetime("now","LocalTime","-{dias_atras} days") and  datetime("now","LocalTime"))) group by ID_produto) 

    left outer join Produtos on product = Produtos.ID

    order by cnt desc

    LIMIT {limite}
        ''').fetchall()

        if produtos_mais_vendidos:
            for i in range(len(produtos_mais_vendidos)):
                tela_admin.listWidget_produtos_mais_vendidos.addItem(f"{produtos_mais_vendidos[i][1]} x{produtos_mais_vendidos[i][0]}")


        marcas_mais_vendidas = cursor.execute(f'''
        select ifnull(Produtos.marca,'Sem Marca'), sum(quant) as quant from 
        (select ID_produto, sum(replace(quantidade,'x','')) as quant
        from produtos_vendidos 
        where ID_venda in

        (select ID
        from Venda
        where Data BETWEEN datetime("now","LocalTime","-{dias_atras} days") and  datetime("now","LocalTime"))

        group by ID_produto)

        join Produtos on Produtos.ID = ID_produto

        group by marca order by quant desc

        LIMIT {limite}
        ''').fetchall()


        if marcas_mais_vendidas:
            for i in range(len(marcas_mais_vendidas)):
                tela_admin.listWidget_marcas_mais_vendidas.addItem(f"{marcas_mais_vendidas[i][0]} x{marcas_mais_vendidas[i][1]}")


        grades_mais_vendidas = cursor.execute(f''' 
        
        
        select Grade_de_Produtos.Descricao, quant from
        (select Produtos.ID_Grade as grade_id, sum(quant) as quant from 
        (select ID_produto, sum(replace(quantidade,'x','')) as quant
        from produtos_vendidos 
        where ID_venda in

        (select ID
        from Venda
        where Data BETWEEN datetime("now","LocalTime","-30 days") and  datetime("now","LocalTime"))

        group by ID_produto)

        join Produtos on Produtos.ID = ID_produto

        group by grade_id)

        join Grade_de_Produtos on Grade_de_Produtos.ID = grade_id

        LIMIT {limite}
        
        ''').fetchall()



        if grades_mais_vendidas:
            for i in range(len(grades_mais_vendidas)):
                tela_admin.listWidget_grades_mais_vendidas.addItem(f"{grades_mais_vendidas[i][0]} x{grades_mais_vendidas[i][1]}")


        variacoes_mais_vendidas = cursor.execute(f'''
        
with variation as (
select ID_variacoes, ID_variacoes2 from 
(select ID_Codigo 
from produtos_vendidos where ID_venda in
(select ID
from Venda
where Data BETWEEN datetime("now","LocalTime","-30 days") and  datetime("now","LocalTime")))

join Codigo_Produtos on ID_codigo = Codigo_Produtos.ID),


all_variation(variation_id) as (
select ID_variacoes
from variation

union all
select ID_variacoes2 from variation )



select variacoes.Variacao,count(variacoes.Variacao) as contagem
from all_variation
join Variacoes on Variacoes.ID = all_variation.variation_id
group by variacoes.Variacao order by contagem desc

limit {limite}

         ''').fetchall()

        if variacoes_mais_vendidas:
            for i in range(len(variacoes_mais_vendidas)):
                tela_admin.listWidget_variacoes_mais_vendidas.addItem(f"{variacoes_mais_vendidas[i][0]} x{variacoes_mais_vendidas[i][1]}")


        tela_admin.label_media_diaria.setText(f"{media_diaria:.2f} R$".replace(".",","))
        tela_admin.label_ganhos.setText(f"{ganhos:.2f} R$".replace(".",","))


        tela_admin.label_ganhos_dos_ultimos.setText(f"Dos Últimos {dias_atras} Dias")
        tela_admin.label_ganhos_dos_ultimos_2.setText(f"Dos Últimos {dias_atras} Dias")


        height = tela_admin.pushButton_analize.height()
        inicio_pos = tela_admin.pushButton_analize.pos()
        tela_admin.widget_select_nav.setGeometry(inicio_pos.x(),inicio_pos.y(),3,height)

        tela_admin.stackedWidget.setCurrentIndex(5)
    
    elif button == "visualizar produtos":
        height = tela_admin.pushButton_visualizar_produtos.height()
        inicio_pos = tela_admin.pushButton_visualizar_produtos.pos()
        tela_admin.widget_select_nav.setGeometry(inicio_pos.x(),inicio_pos.y(),3,height)
        tela_admin.stackedWidget.setCurrentIndex(1)

    elif button == "cadastrar produtos":
        height = tela_admin.pushButton_cadastrar_produtos.height()
        inicio_pos = tela_admin.pushButton_cadastrar_produtos.pos()
        tela_admin.widget_select_nav.setGeometry(inicio_pos.x(),inicio_pos.y(),3,height)  
        tela_admin.stackedWidget.setCurrentIndex(2)

    elif button == "cadastrar grades":
        height = tela_admin.pushButton_cadastrar_grades.height()
        inicio_pos = tela_admin.pushButton_cadastrar_grades.pos()
        tela_admin.widget_select_nav.setGeometry(inicio_pos.x(),inicio_pos.y(),3,height)
        tela_admin.stackedWidget.setCurrentIndex(3)

    elif button == "config":

        setar_initial_config()
        height = tela_admin.pushButton_configuracoes.height()
        inicio_pos = tela_admin.pushButton_configuracoes.pos()
        tela_admin.widget_select_nav.setGeometry(inicio_pos.x(),inicio_pos.y(),3,height)
        tela_admin.stackedWidget.setCurrentIndex(4)

        


inicio("inicio")
tela_admin.pushButton_inicio.clicked.connect(lambda:inicio("inicio"))
tela_admin.pushButton_analize.clicked.connect(lambda:inicio("analize"))
tela_admin.pushButton_visualizar_produtos.clicked.connect(lambda:inicio("visualizar produtos"))
tela_admin.pushButton_cadastrar_produtos.clicked.connect(lambda:inicio("cadastrar produtos"))
tela_admin.pushButton_cadastrar_grades.clicked.connect(lambda:inicio("cadastrar grades"))
tela_admin.pushButton_configuracoes.clicked.connect(lambda:inicio("config"))


# tela estatistica



estatisticas.vendasBtn.clicked.connect(setar_as_vendas)
estatisticas.estatisticasBtn.clicked.connect( setar_as_estatisticas)
estatisticas.ganhosBtn.clicked.connect(lambda: estatisticas.stackedWidget.setCurrentIndex(1))
estatisticas.configBtn.clicked.connect(ir_config_estatisticas)


resumo_do_caixa.pushButton_imprimir_relatorio.clicked.connect(lambda: ImprimirArquivo(url = fr"{c}\relatorio.pdf"))
resumo_do_caixa.pushButton_salvar_relatorio.clicked.connect(lambda: SalvarArquivo(url_arquivo = fr"{c}\relatorio.pdf"))

caixa_estatistica_view.pushButton_imprimir.clicked.connect(lambda: ImprimirArquivo(url = fr"{c}\relatorio.pdf"))
caixa_estatistica_view.pushButton_salvar.clicked.connect(lambda: SalvarArquivo(url_arquivo = fr"{c}\relatorio.pdf"))

Tela_registro_vendas.pushButton_cancelar_venda.clicked.connect(VisualizarVendas.cancelar_produtos)



def gerar_codigo_aleatorio():
    #buscar no banco de dados
    asp = "'"
    id = randint(100000000,999999999)

    while True:
        sql=f"select codigo from Codigo_Produtos where codigo = {asp+str(id)+asp}"
        dado =  cursor.execute(sql).fetchall()
        
        if len(dado) > 0:
            id = randint(100000000,999999999)

        else:
            tela_admin.lineEdit_codigo.setText(f"{id}")
            return
            

tela_admin.pushButton_gerar_codigo.clicked.connect(gerar_codigo_aleatorio)


tela_vendas.keyPressEvent = produto.keyPressCodigo


tela_sub_total.keyPressEvent = sub_total_KeyPress






tela_admin.VerEstatisticasBtn.clicked.connect(entraTelaEstatisticas)


def verificar_se_codigo_editavel():

    if produto.editavel == True:
        text = tela_vendas.lineEdit_codigo.text()
     
        tela_vendas.lineEdit_codigo.clear()

        tela_vendas.lineEdit_codigo.setText(f"{text[-1:]}")

    produto.editavel = False


tela_vendas.lineEdit_codigo.textChanged.connect(verificar_se_codigo_editavel)


    #caracteristicas
tela_admin.lineEdit_caracteristicas.returnPressed.connect(criar_caracteristica)

tela_admin.pushButton_remover_caracteristicas.clicked.connect(remover_caracteristica)

tela_admin.pushButton_adicionar_caracteristicas.clicked.connect(criar_caracteristica)

    #variações

tela_admin.lineEdit_variacoes.returnPressed.connect(Grade.insert_variacoes)

tela_admin.pushButton_adicionar_variacoes.clicked.connect(Grade.insert_variacoes)

tela_admin.pushButton_remover_variacoes.clicked.connect(remover_variacao)

tela_admin.listWidget_caracteristicas.currentRowChanged.connect(Grade.Row_chaged)


    #adicionar para o banco de dados

tela_admin.pushButton_adicionar.clicked.connect(Grade.add_to_dataBase)


    #menssagem 
def er1():
    tela_admin.label_menssa_grade.clear()

def er2():
    tela_admin.label_menssa_grade.clear()

def er3():
    tela_admin.label_menssa_grade.clear()

tela_admin.lineEdit_nome_grade.textChanged.connect(er1)
tela_admin.lineEdit_caracteristicas.textChanged.connect(er2)
tela_admin.lineEdit_variacoes.textChanged.connect(er3)


Tela_exportar.pushButton_caminho.clicked.connect(escolher_folder)
tela_admin.actionsalvar_SQL.triggered.connect(open_choose_exportar)
Tela_exportar.pushButton_ok.clicked.connect(exportar)

#cadastrar marcas 


tela_admin.pushButton_Marca.clicked.connect(abrir_tela_marcas)
tela_add_marcas.pushButton_adicionar_marca_to_data_base.clicked.connect(Tela_Marca.add_marcas_dataBase)
tela_add_marcas.pushButton_deletar_marca.clicked.connect(Tela_Marca.deletar_marca)
tela_add_marcas.pushButton_escolher_marca.clicked.connect(Tela_Marca.escolher_marca)
tela_add_marcas.lineEdit.textChanged.connect(Tela_Marca.pesquisar_marcas)
tela_add_marcas.lineEdit.returnPressed.connect(Tela_Marca.pesquisar_marcas)

mudar_variacao.pushButton_salvar.clicked.connect(VisualizarProduto.MudarVariacao.adicionar_nova_variacao)
mudar_variacao.listWidget.itemClicked.connect(VisualizarProduto.MudarVariacao.pegar_nova_variacao) 

#cadastrar produtos

visualizar_grade.pushButton_adicionar.clicked.connect(GradeView.adicionar_variacao)
visualizar_grade.lineEdit_variacao.returnPressed.connect(GradeView.adicionar_variacao)



tela_admin.pushButton_adicionar_produto_ins.clicked.connect(adicionar_itens)


tela_admin.pushButton_pesquisar_grade.clicked.connect(abrir_tela_pesquisar_grade)


escolher_grade.pushButton_pesquisar.clicked.connect(pesquisar_grade)
escolher_grade.lineEdit.returnPressed.connect(pesquisar_grade)
escolher_grade.listWidget_pesquiasar_grade.itemClicked.connect(selecionar_grade)

tela_admin.lineEdit_preco.textChanged.connect(only_float_preco_cadastrar)

tela_admin.lineEdit_quantidade_cadastro.textChanged.connect(only_int_quantidade_cadastro)

tela_admin.lineEdit_codigo.returnPressed.connect(adicionar_itens)
tela_admin.lineEdit_quantidade_cadastro.returnPressed.connect(adicionar_itens)

tela_admin.lineEdit_codigo.textChanged.connect(code_no_only_int)

confirmar_trocar_grade.pushButton_nao.clicked.connect(Trocar_grade_no)

confirmar_trocar_grade.pushButton_sim.clicked.connect(Trocar_grade_sim)

tela_admin.pushButton_pesquisar_ncm.clicked.connect(abrir_pesquisar_ncm)

tela_admin.pushButton_add_dataBase.clicked.connect(CadastrarProdutos.add_to_dataBase)


tela_admin.comboBox_2.currentIndexChanged.connect(ban)

########################   pesquisar produtos

tela_admin.pushButton_recarregar.clicked.connect(ban)

tela_admin.comboBox.currentIndexChanged.connect(Pesquisar_itens_navegar_dados)


tela_admin.tableWidget_produtos.itemClicked.connect(abrir_navegar_produto)


tela_produtos.lineEdit_produto_preco.textChanged.connect(only_int_preco_pesquisar_produtos)



tela_produtos.pushButton_salvar.clicked.connect(VisualizarProduto.salvar_alteracoes)


tela_produtos.pushButton_deletar.clicked.connect(VisualizarProduto.deletar_produto)

tela_produtos.pushButton_adicionar.clicked.connect(abrir_tela_add_produtos_na_visualizacao)


cadastrar_produtos_linked_tela_produtos.lineEdit_quantidade.textChanged.connect(controle_de_zero_na_tela_liked_tela_produto)


def temp_erase_linked():
    cadastrar_produtos_linked_tela_produtos.label.clear()
cadastrar_produtos_linked_tela_produtos.lineEdit_codigo.textChanged.connect(temp_erase_linked)


cadastrar_produtos_linked_tela_produtos.pushButton.clicked.connect(adicionar_mercadoria_linked_tela_produtos)


def scroll_at_the_bottom():

    if tela_admin.tableWidget_produtos.verticalScrollBar().maximum() == tela_admin.tableWidget_produtos.verticalScrollBar().value():
        list_thread = threading.enumerate()
        if len(list_thread) == 2:
            print("batata")
            print(list_thread)
            return
     
        threadPesquisar = threading.Thread(target=setar_itens_TableWidget)
        threadPesquisar.daemon = True
        threadPesquisar.start()
        threadPesquisar.join()
        
        return


tela_admin.tableWidget_produtos.verticalScrollBar().valueChanged.connect(scroll_at_the_bottom)


def vendas_scroll_bottom():
    if tela_admin.tableWidget_produtos.verticalScrollBar().maximum() == tela_admin.tableWidget_produtos.verticalScrollBar().value():
        setar_venda_table()
estatisticas.tableWidget.verticalScrollBar().valueChanged.connect(vendas_scroll_bottom)

def tela_produtos_closeEvent(event):
    VisualizarProduto.limpar_data()

tela_produtos.closeEvent = tela_produtos_closeEvent


visualizar_grade.closeEvent = GradeView.limpar_dados
#tela_login

tela_login.pushButton.clicked.connect(logar)
tela_login.lineEdit.textChanged.connect(clear_login)
tela_login.lineEdit_2.textChanged.connect(clear_login)
tela_login.lineEdit_2.returnPressed.connect(logar)


visualizar_grade.listWidget_carc.itemClicked.connect(lambda: GradeView.alterar_variacao(99))
visualizar_grade.pushButton_remover.clicked.connect(GradeView.excluir_variacao)



visualizar_grade.lineEdit_nome_grade.returnPressed.connect(GradeView.trocar_nome_grade)

visualizar_grade.lineEdit_caracteristica.returnPressed.connect(GradeView.trocar_nome_carac)



tela_produtos.pushButton_Marca.clicked.connect(VisualizarProduto.abrir_tela_marcas)
tela_produtos.pushButton_remover_marca.clicked.connect(VisualizarProduto.remover_marca)

#opções tela admin

tela_admin.pushButton_remover_marca.clicked.connect(remover_marca)


tela_add_marcas.listWidget.itemDoubleClicked.connect(lambda: MudarNomeMarca(f"{tela_add_marcas.listWidget.currentItem().text()}",Tela_Marca.pesquisar_marcas))

    #opções de cadastros de produtos

tela_admin.actionsair.triggered.connect(sair_do_admin_to_login)


tela_admin.lineEdit_pesquisar.textChanged.connect(ban)


#tela fiscal 

def abrir_tela_para_adicionar_config_fiscal():
    fiscal_cadastro.show()

tela_admin.pushButton_fiscal.clicked.connect(abrir_tela_para_adicionar_config_fiscal)


#opções da tela de vendas





    #voltar login

tela_vendas.pushButton_voltar_login.clicked.connect(voltar_vendas_to_login)
    #only int nas line edits

# tela_vendas.lineEdit_codigo.textChanged.connect(only_int_codigo_vendas)
# tela_vendas.lineEdit_quantidade.textChanged.connect(only_int_quantidade_vendas)
# tela_vendas.lineEdit_desconto.textChanged.connect(only_int_desconto_vendas)

    #cadastro de produtos na tela de vendas



    #adicionar desconto


tela_desconto.pushButton.clicked.connect(add_desconto)
tela_desconto.lineEdit.textChanged.connect(only_int_desconto)
    #remover produtos

tela_remover.lineEdit.textChanged.connect(only_int_cancelar)
tela_remover.pushButton.clicked.connect(cancelar_produtos)
    #pesquisar produtos


pesquisar_produtos.lineEdit.textChanged.connect(pesquisar_produtos_vendas)
#salvar 

#tela subtotal


#tela_sub_total.pushButton_voltar.clicked.connect(voltar_tela_vendas)
tela_sub_total.comboBox.currentIndexChanged.connect(forma_pagamento)
tela_sub_total.lineEdit_valor.textChanged.connect(inserir_valor)
#tela_sub_total.pushButton_Finalizar.clicked.connect(finalizar_venda)
tela_sub_total.lineEdit_valor.returnPressed.connect(adicionar_pagamento)
tela_sub_total.lineEdit_parcelas.returnPressed.connect(adicionar_pagamento)


    #forma de pagamento na tela sub total
tela_sub_total.lineEdit_forma_de_pagamento.textChanged.connect(only_int_forma_de_pagamento)
tela_sub_total.lineEdit_forma_de_pagamento.returnPressed.connect(inserir_forma_pagamento)
    
     
#abrir caixa

    #cancelar abrir caixa
abrir_caixa.pushButton_cancelar.clicked.connect(cancelar_abrir_caixa)

    #abrir caixa
abrir_caixa.pushButton_abrir.clicked.connect(get_abrir_caixa_working)


#adicional



#gerenciamento



    #only int

def voltar_gerenciamento_vendas():
    widget.setCurrentIndex(0)
gerenciamento_caixa.pushButton_voltar_vendas.clicked.connect(voltar_gerenciamento_vendas)



##################################################    ************** USUARIOS************    ######################################################################

       

tela_admin.tabWidget_config.currentChanged.connect(setar_initial_config)
tela_admin.listWidget_usuario.currentItemChanged.connect(index_changed_usuarios)
tela_admin.pushButton_add_usuario.clicked.connect(adicionar_usuario)


estatisticas.pushButton.clicked.connect(setar_config_dias_atras)
estatisticas.pushButton_19.clicked.connect(setar_config_limite_estatistica)

######################################### ********************* EMPRESA ************************* ##############################


tela_admin.lineEdit_ref_nota.setValidator(QIntValidator())
gerenciamento_caixa.lineEdit_referencia_nfce.setValidator(QIntValidator())
tela_admin.pushButton_salvar_dados_empresa.clicked.connect(salvar_dados_empresa)


estatisticas.lineEdit.setValidator(QIntValidator())
estatisticas.lineEdit_2.setValidator(QIntValidator())


############################################# ********   Personalizar cumpom não fiscal  ******** ############################################# 






############################################# ********   Vendas  ******** ############################################# 



def sub_para_venda():
    widget.setCurrentIndex(0)
    produto.troco = 0.00
    produto.forma_de_pagamento.clear()
    produto.valor_recebido.clear()
    tela_sub_total.listWidget_pagamento.clear()

tela_sub_total.pushButton_voltar_vendas.clicked.connect(sub_para_venda)




################################*************** Gerenciamento********************** ########################



gerenciamento_caixa.dateTimeEdit_filtrar_vendas.dateTimeChanged.connect(start_pesquisar_vendas)
gerenciamento_caixa.dateTimeEdit_filtrar_vendas_limite.dateTimeChanged.connect(start_pesquisar_vendas)
gerenciamento_caixa.lineEdit_filtrar_vendas.textChanged.connect(start_pesquisar_vendas)


def scroll_at_the_bottom_para_pesquisar_vendas():

    if gerenciamento_caixa.tableWidget_produtos_vendidos.verticalScrollBar().maximum() == gerenciamento_caixa.tableWidget_produtos_vendidos.verticalScrollBar().value():
        PesquisarVendasGerenciamento.mostrar_na_table()
        return


gerenciamento_caixa.tableWidget_produtos_vendidos.verticalScrollBar().valueChanged.connect(scroll_at_the_bottom_para_pesquisar_vendas)
gerenciamento_caixa.tableWidget_produtos_vendidos.itemClicked.connect(abrir_navegar_vendas)







estatisticas.estatisticasBtn.clicked.connect(setar_historico_caixa)



abrir_caixa.lineEdit_saldo_inicial.textChanged.connect(text_changed_no_line_abrir_caixa)



fecha_caixar.pushButton_fechar_caixa.clicked.connect(fechar_caixa)

estatisticas.tableWidget.itemClicked.connect(lambda: venda_estatistica(estatisticas.tableWidget.currentRow(),function_excluir= pesquisar_venda).execute())
estatisticas.tableWidget_2.itemClicked.connect(lambda: caixa_estatistica(estatisticas.tableWidget_2.currentRow()).execute())

estastiticas_venda.pushButton_cancelar_vendas.clicked.connect(venda_estatistica.excluir_vendas)
estastiticas_venda.pushButton_trocar.clicked.connect(venda_estatistica.trocar_venda)

estastiticas_venda.pushButton_trocar.setVisible(False)
registrar_entrada.lineEdit.textChanged.connect(lambda: fazer_line_para_colocar_valor("registrar_entrada.lineEdit"))
resgistrar_saida.lineEdit.textChanged.connect(lambda: fazer_line_para_colocar_valor("resgistrar_saida.lineEdit"))

registrar_entrada.pushButton.clicked.connect(lambda: registrar_entradas_saidas("Entrada"))
resgistrar_saida.pushButton.clicked.connect(lambda: registrar_entradas_saidas("Saida"))



estatisticas.pushButton_2.clicked.connect(Setar_dados_estatisticas.vendas_hoje)


#os push button da estatisticas

#vendas hoje

estatisticas.pushButton_2.clicked.connect(lambda: Setar_dados_estatisticas("line", Setar_dados_estatisticas.vendas_hoje))

estatisticas.pushButton_13.clicked.connect(lambda: Setar_dados_estatisticas("line", Setar_dados_estatisticas.vendas_semana))

estatisticas.pushButton_5.clicked.connect(lambda: Setar_dados_estatisticas("line", Setar_dados_estatisticas.vendas_mes))

estatisticas.pushButton_4.clicked.connect(lambda: Setar_dados_estatisticas("line", Setar_dados_estatisticas.vendas_ano))

estatisticas.pushButton_18.clicked.connect(lambda : Setar_dados_estatisticas("line", Setar_dados_estatisticas.vendas_usuario_hoje))

estatisticas.pushButton_17.clicked.connect(lambda : Setar_dados_estatisticas("line", Setar_dados_estatisticas.vendas_usuario_semana))

estatisticas.pushButton_16.clicked.connect(lambda : Setar_dados_estatisticas("line", Setar_dados_estatisticas.vendas_usuario_mes))

estatisticas.pushButton_15.clicked.connect(lambda : Setar_dados_estatisticas("line", Setar_dados_estatisticas.vendas_usuario_ano))

estatisticas.pushButton_11.clicked.connect(lambda : Setar_dados_estatisticas("line", Setar_dados_estatisticas.pagamento_hoje))

estatisticas.pushButton_12.clicked.connect(lambda : Setar_dados_estatisticas("line", Setar_dados_estatisticas.pagamento_semana))

estatisticas.pushButton_10.clicked.connect(lambda : Setar_dados_estatisticas("line", Setar_dados_estatisticas.pagamento_mes))

estatisticas.pushButton_9.clicked.connect(lambda : Setar_dados_estatisticas("line", Setar_dados_estatisticas.pagamento_ano))



estatisticas.dateTimeEdit.dateTimeChanged.connect(pesquisar_venda)
estatisticas.dateTimeEdit_2.dateTimeChanged.connect(pesquisar_venda)


estatisticas.dateTimeEdit_3.dateTimeChanged.connect(pesquisar_caixa)
estatisticas.dateTimeEdit_4.dateTimeChanged.connect(pesquisar_caixa)



visualizar_produtos_nas_vendas.lineEdit_pesquisar.textChanged.connect(TelaViewProdutosNasVendas.pesquisar)

def scroll_at_the_bottom_para_pesquisar_vendas_na_tela_vendas():

    if visualizar_produtos_nas_vendas.tableWidget_produtos.verticalScrollBar().maximum() == visualizar_produtos_nas_vendas.tableWidget_produtos.verticalScrollBar().value():
        TelaViewProdutosNasVendas.SetarTable()
        return

visualizar_produtos_nas_vendas.tableWidget_produtos.verticalScrollBar().valueChanged.connect(scroll_at_the_bottom_para_pesquisar_vendas_na_tela_vendas)



app.exec()


