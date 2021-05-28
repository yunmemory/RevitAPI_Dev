import clr

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

Sheets = UnwrapElement(IN[0])
Sheet_numbers_old = IN[1]
Sheet_numbers_new = IN[2]
Sheet_Parameter = "Sheet Number"

Sheets_Failed = []
for sheet in Sheets:
    sheet_number_para = sheet.LookupParameter(Sheet_Parameter)
    sheet_number_old = sheet_number_para.AsString()
    if sheet_number_old in Sheet_numbers_old:
        sheet_index = Sheet_numbers_old.index(sheet_number_old)
        sheet_number_new = Sheet_numbers_new[sheet_index]
        if sheet_number_new != sheet_number_old and sheet_number_new not in Sheet_numbers_old:
            # Start Transaction
            TransactionManager.Instance.EnsureInTransaction(doc)
            sheet_number_para.Set(sheet_number_new)
            TransactionManager.Instance.TransactionTaskDone()
        else:
            Sheets_Failed.append(sheet_number_new)

# out
OUT = Sheets_Failed
