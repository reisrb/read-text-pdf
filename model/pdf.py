from dataclasses import asdict, dataclass
from typing import List
from copy import deepcopy

from pandas import DataFrame

from model.columns_pdf import ColumnsPdf


@dataclass
class Pdf:
    filename: str = ""
    data_emissao: str = ""
    referente: str = ""
    vencimento: str = ""
    n_instalacao: str = ""
    n_cliente: str = ""
    n_medidor: str = ""
    cnpj: str = ""
    endereco: str = ""
    cep: str = ""
    subgrupo: str = ""
    modalidade: str = ""
    demanda_unica: str = ""
    demanda_hora_ponta: str = ""
    demanda_hora_fora_ponta: str = ""
    aliquota: str = ""

    tabela: List[ColumnsPdf] = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def to_dataframe(self) -> DataFrame:
        tmp = deepcopy(self)
        tmp.tabela = [f"0...{len(self.tabela)}"]
        return DataFrame(tmp.to_dict())

    def tabela_to_dataframe(self) -> DataFrame:
        return DataFrame([i.to_dict() for i in self.tabela])
