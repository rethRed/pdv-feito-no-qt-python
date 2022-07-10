import os
import pdfkit,win32print,win32api,time,multiprocessing

start = time.time()

c = os.getcwd()

wkh_path = rf"{c}\cupom_vendas\wkhtmltopdf\bin\wkhtmltopdf.exe"

web_path = "https://api.focusnfe.com.br/notas_fiscais_consumidor/NFe16220237480491000206650010000000351974122830.html"

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



file_output_path = rf"{c}\cupom_vendas\Recibos Fiscais\batata2.pdf"


try:
    pdfkit.from_url(f"{web_path}",file_output_path,options= opcoes, configuration =config )
   

except OSError:
    print("error conexao")
    
lista_impressoras = win32print.EnumPrinters(2)


impressora = lista_impressoras[5]

win32print.SetDefaultPrinterW(impressora[2])



win32api.ShellExecute(0,"print",file_output_path,None,".",0)

end = time.time()

print("para isso acontecer demorou : ", start - end)

#EPSON TM-T20 Receipt5
#MP-2500 TH (Copy 1)
