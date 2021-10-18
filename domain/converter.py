from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd
from domain.pdf import Pdf

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

    def get_dataframe(self) -> pd.DataFrame:
        df = [[] for x in range(len(self.pdf.pages))]

        for table in self.tables:
            page = int(table[-1])
            df[page].append(self.convert_table(
                self.tables[table][0], self.tables[table][1], page))

        return df

    @abstractmethod
    def to_dataclass(self):
        ...
