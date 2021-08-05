from model.pdf import Pdf
from model.columns_pdf import ColumnsPdf
import pdfplumber
from pprint import pprint

with pdfplumber.open('CDMATR~1.PDF') as pdf:
    page = pdf.pages[0]
    texts = list(filter(lambda i: i, (map(lambda it: j.split('\n') if (j := it.extract_text()) else None, pdf.pages))))

    table = page.extract_table(table_settings={"vertical_strategy": "lines", 
                                         "horizontal_strategy": "text", 
                                         "snap_tolerance": 2,})
    
pdf = Pdf()
columns_pdf = ColumnsPdf()

numbers = texts[0][2].split(' ')
pdf.n_instalacao, pdf.n_cliente, pdf.n_medidor = numbers[0], numbers[1], numbers[2]
pdf.cnpj = texts[0][3].split('CPF/CNPJ:')[1].split(' ')[1]
pdf.endereco = texts[0][6]

for text in texts[0]:
	if 'CEP' in text:
		pdf.cep = text.split(' ')[1]
		break
	
pprint(pdf.to_string())



# linhasTabela = []
# for text in texts[0]:
# 	if  'CCI' in text:
# 		grava = True
		
# 	if 'Valor dos Tributos:' in text:
# 		grava = False

# 	if grava:
# 		linhasTabela.append(text)
		

# pdf.tabela = linhasTabela

# pprint(pdf.to_string(), width=150)
		