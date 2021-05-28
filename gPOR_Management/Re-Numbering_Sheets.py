import clr
import sys

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitAPIUI")
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

Sheets = IN[0]
Sheet_numbers_old = IN[1]
Sheet_numbers_new = IN[2]
Sheet_Parameter = "SHEET_NUMBER"

for sheet in Sheets:
    sheet_number_para = sheet.LookupParameter(Sheet_Parameter)
    sheet_number_old = sheet_number_para.AsString()
    sheet_index = Sheet_numbers_old.index(sheet_number_old)
    sheet_number_new = Sheet_numbers_new[sheet_index]
    # Start Transaction
    TransactionManager.Instance.EnsureInTransaction(doc)
    sheet_number_para.Set(sheet_number_new)
    TransactionManager.Instance.TransactionTaskDone()

# out
out = Sheet_numbers_new
