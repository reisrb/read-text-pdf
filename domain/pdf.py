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