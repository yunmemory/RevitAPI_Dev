import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

# Category
cat = [BuiltInCategory.OST_Sheets]

Ele = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()

# Get ordered parameter
ps_name = []
ps_valuestring = []
ps_sheets = []

for e in Ele:
    p_name = []
    p_valuestring = []
    p_sheet = []
    ps = e.GetOrderedParameters()
    for p in ps:
        p_name.append(p.Definition.Name)
        p_sheet.append(e.Id)
        if p.AsValueString() is not None:
            p_valuestring.append(p.AsValueString())
        else:
            p_valuestring.append(p.AsString())
    ps_name.append(p_name)
    ps_valuestring.append(p_valuestring)
    ps_sheets.append(p_sheet)

# for e in Ele:
#     p_name = []
#     p_valuestring = []
#     p_string = []
#     ps = e.GetOrderedParameters()
#     for p in ps:
#         p_name.append(p.Definition.Name)
#         p_valuestring.append(p.AsValueString())
#         p_string.append(p.AsString())
#     ps_name.append(p_name)
#     ps_valuestring.append(p_valuestring)
#     ps_string.append(p_string)



# Output
OUT = Ele, ps_sheets, ps_name, ps_valuestring