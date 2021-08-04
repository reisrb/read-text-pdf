from model.pdf import Pdf
import pdfplumber
from pprint import pprint

with pdfplumber.open('CDMATR~1.PDF') as pdf:
	texts = list(filter(lambda i: i, (map(lambda it: j.split('\n') if (j := it.extract_text()) else None, pdf.pages))))

pdf = Pdf()

numbers = texts[0][2].split(' ')
pdf.n_instalacao, pdf.n_cliente, pdf.n_medidor = numbers[0], numbers[1], numbers[2]
pdf.cnpj = texts[0][3].split('CPF/CNPJ:')[1].split(' ')[1]

pdf.endereco = texts[0][6]
pdf.cep = texts[0][7].split(' ')[1]

pprint(pdf.to_string())


# linhas = []

# for text in texts[0]:
#   if '0699' in text:
#     linhas.append(text)

# pdf.linhas = linhas
# pprint(pdf)