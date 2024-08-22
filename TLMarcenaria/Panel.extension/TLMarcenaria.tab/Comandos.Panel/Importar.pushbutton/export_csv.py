# -*- coding: utf-8 -*-
#Exports selected schedules to CSV files.

import os.path as op

from pyrevit import coreutils
from pyrevit import revit, DB
from pyrevit import forms


def export_from_table():
    basefolder = op.expandvars('%temp%')

    try:
        sched = forms.select_schedules(title="Selecione uma tabela", multiple=False)
        vseop = DB.ViewScheduleExportOptions()
        vseop.ColumnHeaders = DB.ExportColumnHeaders.OneRow
        vseop.TextQualifier = DB.ExportTextQualifier.DoubleQuote

        csv_sp = ';'

        vseop.FieldDelimiter = csv_sp
        vseop.Title = False
        vseop.HeadersFootersBlanks = False

        fname = \
            coreutils.cleanup_filename(revit.query.get_name(sched)) \
            + '.csv'
        sched.Export(basefolder, fname, vseop)
        op.join(basefolder, fname)
        
        return [sched, basefolder + '\\' + fname]
    
    except Exception as error:
        forms.alert('{}'.format(error))
        