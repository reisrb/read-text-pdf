from dataclasses import dataclass, asdict
from model.columns_pdf import ColumnsPdf

@dataclass
class Pdf:
    n_instalacao: str = ''
    n_cliente: str = ''
    n_medidor: str = ''
    cnpj: str = ''
    endereco: str = ''
    cep: str = ''

    tabela: list = ''

    def to_string(self) -> dict:
        return asdict(self)
