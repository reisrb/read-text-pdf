# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from os import listdir
from pprint import pprint

from tqdm import tqdm
from wand.image import Image
from IPython.display import display, clear_output
import pdfplumber
import pandas as pd

from model.columns_pdf import ColumnsPdf
from model.pdf import Pdf


# %%
def read_pdf(path: str):
    with pdfplumber.open(path) as pdf:
        texts = []
        table = []
        for page in pdf.pages:
            extracted = page.extract_text(y_tolerance=4)
            if extracted is None:
                continue
            texts += filter(lambda i: i, extracted.split("\n"))
            table += page.extract_table(table_settings={
                "vertical_strategy": "lines",
                "horizontal_strategy": "text",
                "snap_tolerance": 2,
            }) or []
    return texts, table

# DEBUG
texts1, table1 = read_pdf("in/Barbosa ENEL_SP loja 19 abr21.pdf") # Azul normal
texts2, table2 = read_pdf("in/Barbosa ENEL_SP loja 38 abr21.pdf") # Verde sem valores
texts3, table3 = read_pdf("in/Barbosa ENEL_SP loja 37 mai21.pdf") # Verde normal
# pd.DataFrame(
#     data=table
# )
# list(enumerate(texts))
# texts[-4].split()[:3]
# texts[-4].split()[3:5]
# texts[-4].split()[5:]
#.split()[6]


# %%
pd.DataFrame(texts1)[:30]


# %%
def convert_table(texts: list, table: list):
    list_lines = []
    list_exists = []
    for line in table:
        for j, text in enumerate(texts):
            if line[0] in text:
                if j in list_exists:
                    continue
                else:
                    list_exists.append(j)
                
                columns_pdf = ColumnsPdf()
                columns_pdf.cci = text.split()[0] if text.split()[0].isdigit() else ""
                columns_pdf.descricao = line[0]
                columns_pdf.leitura_alterior = line[1]
                columns_pdf.leitura_atual = line[2]
                columns_pdf.registrado = line[3]
                columns_pdf.faturado = line[4]
                columns_pdf.tarifa_com_icms = line[5]
                columns_pdf.base_icms = line[6]
                columns_pdf.aliq_icms = line[7]
                columns_pdf.icms = line[8]
                columns_pdf.valor = line[9]
                columns_pdf.tarifa_sem_impostos = text.split()[-1] if line[-1] and text.split()[-1] != line[-1] else ""
                list_lines.append(columns_pdf)
                break
    columns_pdf = ColumnsPdf()
    columns_pdf.cci = texts[j+1].split()[0]
    columns_pdf.descricao = " ".join(texts[j+1].split()[1:-1])
    columns_pdf.valor = texts[j+1].split()[-1]
    list_lines.append(columns_pdf)
    return list_lines

# DEBUG
# convert_table(texts, table)


# %%
def convert(texts: list, table: list):
    pdf = Pdf()

    numbers = texts[2].split(' ')
    pdf.n_instalacao, pdf.n_cliente, pdf.n_medidor = numbers[0], numbers[1], numbers[2]
    pdf.cnpj = texts[3].split('CPF/CNPJ:')[1].split(' ')[1]
    pdf.endereco = texts[6]
    pdf.subgrupo = texts[9].split()[1]
    pdf.data_emissao= " ".join(texts[-4].split()[:3])
    pdf.referente= " ".join(texts[-4].split()[3:5])
    pdf.vencimento= " ".join(texts[-4].split()[5:])
    if "Azul" in texts[12]:
        pdf.modalidade = "Azul"
        pdf.demanda_hora_ponta = texts[13].split()[1]
        pdf.demanda_hora_fora_ponta = texts[13].split()[4]
    elif "Verde" in texts[12]:
        pdf.modalidade = "Verde"
        pdf.demanda_unica = texts[13].split()[0]
    
    for text in texts:
        if 'CEP' in text:
            pdf.cep = text.split(' ')[1]
            break

    pdf.tabela = convert_table(texts, table)

    for line in pdf.tabela:
        if line.aliq_icms[:-1].isdigit() and line.aliq_icms[:-1] != "0" :
            pdf.aliquota = line.aliq_icms
            break
    else:
        pdf.aliquota = "0%"
            
    return pdf

# DEBUG
# TODO
# table.insert(33, ['PIS/PASEP (0,59%)', '', '', '', '', '', '0,00', '0%', '0,00', '77,21-']) # teste
# texts[0].insert(54, '0699 PIS/PASEP (0,59%) 0,00 0% 0,00 77,27-') # teste


# %%
def full(path: str):
    texts, table = read_pdf(path)
    pdf = convert(texts, table)
    pdf.filename = path.split("/")[-1]
    return pdf

# DEBUG
# example = full("in/Barbosa ENEL_SP loja 28 mai21.pdf")
# example = full("in/Barbosa ENEL_SP loja 37 abr21.pdf")
# example.to_dataframe()
# example.tabela_to_dataframe().to_csv('t.csv')


# %%
extracted = []
path = "in"
for file in tqdm(listdir(path)):
    try:
        extracted.append(full("/".join([path, file])))
    except Exception as e:
        print(file)
        raise e


# %%
for text in tqdm(extracted):
    pd.concat([text.to_dataframe(), text.tabela_to_dataframe()]).to_csv('out/' + text.filename.replace('.pdf', '.csv'))


# %%

# for t in tqdm(extracted):
#     clear_output()
#     display(t.to_dataframe())
#     display(Image(filename="/".join([path, t.filename]), resolution=200))
#     display(t.tabela_to_dataframe())
#     input('Press enter to skip')
# img
# %%
