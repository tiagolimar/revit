from pyrevit import revit, DB

PES = 30.48

def find_family_and_type(doc, family_name):
    fam_symbol = None
    for fam in DB.FilteredElementCollector(doc).OfClass(DB.Family):
        if fam.Name == family_name:
            for symbol_id in fam.GetFamilySymbolIds():
                fam_symbol = doc.GetElement(symbol_id)
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
            instance = doc.Create.NewFamilyInstance(
                DB.XYZ(loc[0], loc[1], 0), fam_symbol, doc.ActiveView)

            set_parameter(instance, 'Comprimento', params['comprimento'] / PES)
            set_parameter(instance, 'Largura', params['largura'] / PES)
            set_parameter(instance, 'Espessura', params['espessura'] / PES)
            set_parameter(instance, 'Cod', params['cod'])