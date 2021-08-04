from dataclasses import dataclass, asdict

@dataclass
class Pdf:
    n_instalacao: str = None
    n_cliente: str = None
    n_medidor: str = None
    cnpj: str = None
    endereco: str = None
    cep: str = None

    tabela: list = None

    def to_string(self) -> dict:
        return asdict(self)
