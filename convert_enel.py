# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pprint
import pdfplumber
import pandas as pd 
import numpy as np

from typing import List
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


# %%
from copy import deepcopy
from pandas import DataFrame
from dataclasses import asdict, dataclass

@dataclass
class Pdf():
    numero_instalacao: str = ""
    numero_cliente: str = ""
    numero_medidor: str = ""
    grupo_tarifario: str = ""
    modalidade_tarifaria: str = ""
    dem_cont_ep: str = ""
    dem_cont_efp: str = ""
    valor_fat_acl: str = ""
    pis: str = ""
    cofins: str = ""
    icms: str = ""
    usd_ep: str = ""
    usd_efp: str = ""
    ufer_ep: str = ""
    ufer_efp: str = ""
    ufdr_ep: str = ""
    ufdr_efp: str = ""
    cip_cosip: str = ""
    subv_tar: str = ""
    cde_covid_ep: str = ""
    cde_covid_efp: str = ""
    fat_car_ep: str = ""
    fat_car_efp: str = ""

    def to_csv(self):
        self.to_dataframe().to_csv('exportando_enel.csv')

    def to_dict(self) -> dict:
        return asdict(self)

    def to_dataframe(self) -> DataFrame:
        return DataFrame(self.to_dict())


# %%
class Converter(metaclass=ABCMeta):
    table = ...

    def convert_table(self, vertical: list, horizontal: list, page: int):
        _df = pd.DataFrame(self.pdf.pages[page].extract_tables({
            "vertical_strategy": "explicit", "horizontal_strategy": "explicit", "snap_tolerance": 3,
            "explicit_vertical_lines": vertical, "explicit_horizontal_lines": horizontal,
        })[0])
        _df.replace('', np.nan, inplace=True)
        _df.dropna(how="all", inplace=True)
        _df.replace(np.nan, '', inplace=True)
        return _df

    def to_img(self, vertical: list, horizontal: list, page: int, resolution=120):
        return self.pdf.pages[page].to_image(resolution=resolution).debug_tablefinder({
            "vertical_strategy": "explicit", "horizontal_strategy": "explicit", "snap_tolerance": 3,
            "explicit_vertical_lines": vertical, "explicit_horizontal_lines": horizontal,
        })

    def get_dataframe(self) -> Pdf:
        df = [[] for x in range(len(self.pdf.pages))]

        for table in self.tables:
            page = int(table[-1])
            df[page].append(self.convert_table(self.tables[table][0], self.tables[table][1], page))

        return df
    

    @abstractmethod
    def to_dataclass(self):
        ...


# %%
@dataclass
class CpflConverter(Converter):
    tables = {
        # {
        #     f"endereco_{i}": ([1, ..., 99], [1, ..., 99]) for i in range(2)
        # },
        **{ #0
            f"roteiro_de_leitura_{i}": ([45, 170, 220, 320, 550], [150, 162, 175]) for i in range(2)
        },
        **{ #1
            f"dados_do_seu_codigo_{i}": ([45, 280, 550], [190, 205, 215, 225, 240]) for i in range(2)
        },
        **{ #2
            f"atendimento_cpfl_{i}": ([45, 143, 195, 260, 350, 440, 550], [255, 280]) for i in range(2)
        },
        **{ #3
            f"discriminacao_da_operacao_{i}": ([45, 62, 150, 175, 220, 255, 270, 305, 350, 390, 410, 440, 490, 520, 550], [290, 312, *[322+(10*x) for x in range(23)]]) for i in range(2)
        },
        **{ #  ultima pagina
            "demanda_contratada_2": ([47, 80, 167], [148, 156, 163, 170, 180])
        },
        **{ #  ultima pagina
            "tarifa_aneel_2": ([193, 255, 312, 372, 432, 490, 548], [193, *[201+(6.6*i) for i in range(5)], 237])
        },
    }

    # TODO: arrumar o __init__
    def __init__(self, file_path: str):
        self.pdf = pdfplumber.open(file_path)

    def __enter__(self):
        print("Reading PDF")
        return self    

    def __exit__(self):
        print("Closing PDF")
        self.pdf.close()
        
    # TODO: abrir o arquivo ao usar a função e fechar a porta ao sair 
    def to_dataclass(self):
        pdf = Pdf()
        df = self.get_dataframe()

        pdf.numero_instalacao = df[0][0][1]
        pdf.grupo_tarifario = df[0][1][1][0].split("-")[1][0:2]
        pdf.modalidade_tarifaria = "Verde" if "VERDE" in df[0][1][1][0].upper() else "Azul"
        pdf.n_medidor = df[0][2][1]
        pdf.numero_cliente = df[0][2][2]

        pos_desconto_acl = [pos for pos, char in enumerate(df[0][3][1]) if 'DESCONTO ENERGIA ACL' in char.upper()][0]
        pdf.valor_fat_acl = df[0][3][7][pos_desconto_acl]

        #vem com %
        pdf.pis = df[0][3][12][0].split('\n')[1]
        #vem com %
        pdf.cofins = df[0][3][13][0].split('\n')[1]
        #icms vem sem %
        pdf.icms = df[1][3][9][1]

        if pdf.modalidade_tarifaria == "Azul":

            pos_usd_p = [pos for pos, char in enumerate(df[1][3][1]) if 'USO SIST DISTR PONTA' in char.upper()][0]
            pdf.usd_ep = df[1][3][4][pos_usd_p]

            pos_usd_fp = [pos for pos, char in enumerate(df[1][3][1]) if 'USO SIST DISTR F PONTA' in char.upper()][0]
            pdf.usd_efp = df[1][3][4][pos_usd_fp]

        else:
            pos_cde_p = [pos for pos, char in enumerate(df[2][1][2]) if 'CDE COVID PONTA' in char.upper()][0]
            pdf.cde_covid_ep = df[2][1][3][pos_cde_p]
            pos_cde_fp = [pos for pos, char in enumerate(df[2][1][2]) if 'CDE COVID FPONT' in char.upper()][0]
            pdf.cde_covid_ep = df[2][1][3][pos_cde_fp]


        pdf.dem_cont_ep = df[2][0][1][1]
        pdf.dem_cont_efp = df[2][0][1][2]

        return pdf


# %%
cpfl = CpflConverter("in/cpfl/MAGSAC EMPRESA JUNHO 2.pdf")#azul


# %%
cpfl = CpflConverter("in/cpfl/CPFL colorflex.pdf") #verde


# %%
cpfl.to_dataclass().to_dataframe()
