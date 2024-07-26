# -*- coding: utf-8 -*-

import csv
import codecs
from pyrevit import DB, revit, forms

# csvFilePath = r'C:\Users\User\Desktop\CENTRO\DAVI\000 - GERAL\revit\TLMarcenaria\Panel.extension\TLMarcenaria.tab\Comandos.Panel\Importar.pushbutton\file.csv'
familyName = 'Painel'
typeName = 'Painel'

doc = revit.doc

PES = 30.48

def find_family_and_type(doc, family_name, type_name):
    fam_symbol = None
    for fam in DB.FilteredElementCollector(doc).OfClass(DB.Family):
        if fam.Name == family_name:
            for symbolId in fam.GetFamilySymbolIds():
                fam_symbol = doc.GetElement(symbolId)
                return fam_symbol

def set_parameter(instance, param_name, value):
    param = instance.LookupParameter(param_name)
    if param and param.IsReadOnly == False:
        param.Set(value)

def create_family_instances(doc, fam_symbol, locations, parameters):
    with revit.Transaction('Create Family Instances'):
        if not fam_symbol.IsActive:
            fam_symbol.Activate()
            doc.Regenerate()
        for loc, params in zip(locations, parameters):
            instance = doc.Create.NewFamilyInstance(DB.XYZ(loc[0], loc[1], 0), fam_symbol, doc.ActiveView)

            set_parameter(instance, 'Comprimento', params['comprimento'] / PES)  
            set_parameter(instance, 'Largura', params['largura'] / PES)  
            set_parameter(instance, 'Espessura', params['espessura'] / PES)  
            set_parameter(instance, 'Cod', params['cod']) 

def main():
    locations = []
    parameters = []
    x_offset = 0

    csvFilePath = forms.pick_file(file_ext='csv',init_dir=r'C:\Users\User\Desktop\CENTRO\DAVI')

    with codecs.open(csvFilePath, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        print(reader.fieldnames)
        for row in reader:
            comprimento = float(row['Comprimento'].replace(',', '.'))
            largura = float(row['Largura'].replace(',', '.'))
            espessura = float(row['Espessura'].replace(',', '.'))
            cod = row['Cod'].replace(',', '.')
            quantidade = int(row['Quantidade'])

            # Calculando o deslocamento para cada instância
            for _ in range(quantidade):
                locations.append((x_offset, 0))
                parameters.append({'comprimento': comprimento, 'largura': largura, 'espessura': espessura, 'cod':cod})
                x_offset += comprimento / PES  # Convertendo para pés

    fam_symbol = find_family_and_type(doc, familyName, typeName)

    if fam_symbol:
        create_family_instances(doc, fam_symbol, locations, parameters)
    else:
        forms.alert('Família ou tipo não encontrado.')

main()
