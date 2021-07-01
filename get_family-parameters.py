import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

p_name = []
p_shared = []

mgr = doc.FamilyManager

for fp in mgr.Parameters:
    p_name.append(fp.Name)
    p_shared.append(GetFamilyParamGuid(fp))