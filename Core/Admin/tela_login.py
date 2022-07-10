from load import *


def cancelar_abrir_caixa():
    global fechar_tela_abrir_caixa
    fechar_tela_abrir_caixa = True
    widget.setCurrentIndex(3)
    abrir_caixa.close()
    abrir_caixa.hide()

def clear_login():
    tela_login.label_2.setText("")

def logar():

    global fechar_tela_abrir_caixa
    tela_login.label_2.setText("")
    usuario_input = tela_login.lineEdit.text().lstrip().rstrip()
    senha_input = tela_login.lineEdit_2.text().lstrip().rstrip()


    try:
        id = cursor.execute(f"select ID from Usuario where usuario = '{usuario_input}' and Senha_login = '{senha_input}'").fetchall()[0][0]
        
        if id == 1000000000:
            widget.setCurrentIndex(1)
            return
        widget.setCurrentIndex(0)

        file = f"{c}\DataBase\Config.ini"
        config = ConfigParser()
        config.read(file)

        config["Caixa"]["id_funcionario"] = f"{id}"

        with open(file, 'w') as configfile:
            config.write(configfile)


        abrir_caixa.dateTimeEdit.setDateTime(QDateTime.currentDateTime()) 


        if config["Caixa"]["caixa_aberto"] == "False":
        

            if cursor.execute(f"select Abrir_Caixa from Acesso_usuario where id = {id}").fetchall()[0][0] != 1:
                msg = QMessageBox(visualizar_grade)
                msg.setStyleSheet('background-color:#34495e;font: 75 14pt "MS Shell Dlg 2" bold;color: rgb(255, 255, 255);font-weight: bold;')
                msg.setText(f'''Você Não tem permisão Para abrir o caixa, Insira a senha de Acesso para continuar.''')
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Aviso.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)
                msg = msg.exec_()
            
                while True:
                    permitido = PedirPermissao().return_answer()
                    
                    if permitido == True:
                        break

                    else:
                        widget.setCurrentIndex(3)
                        return

            while True:
                abrir_caixa.exec()
                file = f"{c}\DataBase\Config.ini"
                config = ConfigParser()
                config.read(file)
                if config["Caixa"]["caixa_aberto"] == "True" or fechar_tela_abrir_caixa == True:
                    abrir_caixa.close()
                    fechar_tela_abrir_caixa = False
                    break

        
        

        print("entrou")

        return

    except IndexError:
        tela_login.label_2.setText("Usuario ou Senha São Invalidos.")
        print("invalido")
        return
        
        cursor.execute("select caixa_aberto from config where caixa_aberto not null;")
        caixa = cursor.fetchall()

        if int(caixa[0][0]) == 0:
            abrir_caixa.show()

        else:
            pass
        

        widget.setCurrentIndex(widget.currentIndex()-3)
        return
    
    tela_login.label_2.setText("o usuario ou a senha estar errado.")


def sair_do_admin_to_login():
    widget.setCurrentIndex(widget.currentIndex()+2)
    tela_login.lineEdit.clear()
    tela_login.lineEdit_2.clear()
    tela_login.lineEdit.setFocus()
