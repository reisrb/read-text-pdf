from dataclasses import dataclass, asdict


@dataclass
class ColumnsPdf:
    cci: str = ""
    descricao: str = ""
    leitura_alterior: str = ""
    leitura_atual: str = ""
    registrado: str = ""
    faturado: str = ""
    tarifa_com_icms: str = ""
    base_icms: str = ""
    aliq_icms: str = ""
    icms: str = ""
    valor: str = ""
    tarifa_sem_impostos: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
