import pandas as pd
import random

#extrae datos
def gettingData():
    _route = 'https://docs.google.com/spreadsheets/d/'
    _sheet_id='1w6Lr3cO7rQ8G-D9DpIgIzf4DC28eDbtuy8c_y-zgyRU'
    _sheet_name='Parte_Piero'

    url=f'https://docs.google.com/spreadsheet/ccc?key={_sheet_id}&output=xlsx'
    df = pd.read_excel(url,sheet_name=_sheet_name)

    _titles = df.titulo
    _summary = df.resumen_limpio
    _keywords = df.palabras_clave
    _full_article = df.articulo_completo_limpio

    return _titles, _summary, _keywords, _full_article, len(_titles)


def getTitle(value):
    _titles, _summary, _keywords, _full_article, _size = gettingData()
    value = random.randint(0, _size)
    return _titles[value], value
