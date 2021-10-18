from domain.cpfl_converter import CpflConverter

if __name__ == '__main__':
    # cpfl = CpflConverter("in/cpfl/MAGSAC EMPRESA JUNHO 2.pdf")#azul
    cpfl = CpflConverter("in/cpfl/CPFL colorflex.pdf") #verde
    pdf = cpfl.to_dataclass()
    # print(cpfl.get_dataframe())
    pdf.to_csv()