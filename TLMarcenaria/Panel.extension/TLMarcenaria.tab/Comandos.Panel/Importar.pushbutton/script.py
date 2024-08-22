# -*- coding: utf-8 -*-

import csv
import codecs
from pyrevit import revit, forms
from export_csv import export_from_table
from family_manager import find_family_and_type, create_family_instances
from table import codify

doc = revit.doc
family_name = 'Painel'
PES = 30.48

def main():
    locations = []
    parameters = []
    x_offset = 0

    [view, csv_file_path] = export_from_table()
    # codify(view)

    if csv_file_path:
        with codecs.open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                comprimento = float(row['Comprimento'].replace(',', '.'))
                largura = float(row['Largura'].replace(',', '.'))
                espessura = float(row['Espessura'].replace(',', '.'))
                cod = row['Cod'].replace(',', '.')
                quantidade = int(row['Quantidade'])

                # Calculando o deslocamento para cada instância
                for _ in range(quantidade):
                    locations.append((x_offset, 0))
                    parameters.append(
                        {'comprimento': comprimento,
                         'largura': largura,
                         'espessura': espessura,
                         'cod': cod})
                    x_offset += comprimento / PES  # Convertendo para pés

        fam_symbol = find_family_and_type(doc, family_name)

        if fam_symbol:
            create_family_instances(doc, fam_symbol, locations, parameters)
        else:
            forms.alert('Família ou tipo não encontrado.')


main()
