import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.Exceptions import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitNodes")
import Revit
from Revit.Elements import *

clr.ImportExtensions(Revit.Elements)

doc = DocumentManager.Instance.CurrentDBDocument

Elements = UnwrapElement(IN[0])
Elements_dyn = IN[0]

# ---The check below is for Transactions---
# transaction start
# TransactionManager.Instance.EnsureInTransaction(doc)
# TransactionManager.Instance.TransactionTaskDone()

trans = TransactionManager.Instance
trans.ForceCloseTransaction()

# Type to Elements
total = []
nested_ele = []
n = 0

# ---The check below is for nested shared families---
# for e in Elements_dyn:
#     try:
#         l = len(Element.GetChildElements(e))
#         if l > 0:
#             nested_ele.append(e.Id)
#     except:
#         pass

# ---The check below is for CAD link---
for e in Elements:
    try:
        collect_ele = e.Symbol.Family
        famdoc = doc.EditFamily(collect_ele)
        ele = FilteredElementCollector(famdoc).OfCategory(
            BuiltInCategory.OST_ImportObjectStyles).WhereElementIsElementType().ToElementIds()
        if len(ele) > 0:
            total.append(e.Id)
        else:
            n += 1
    except InvalidOperationException:
        pass
# ---The check below is for CAD link - 02---
family_collector = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
families = [f for f in family_collector]

for f in families:
    # collect_ele = f.Symbol.Family
    famdoc = doc.EditFamily(f)
    ele = FilteredElementCollector(famdoc).OfCategory(BuiltInCategory.OST_ImportObjectStyles).WhereElementIsElementType().ToElementIds()
    if len(ele) > 0:
        total.append(f.Id)
    else:
        n += 1

# ---Collect the family type---
# family = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
#
# output = [] for e in family: try: famdoc = doc.EditFamily(e.Family) ele = FilteredElementCollector(
# famdoc).OfCategory(BuiltInCategory.OST_ImportObjectStyles).WhereElementIsElementType().ToElementIds() if len(ele) >
# 0: output.append(e) else: n += 1 except: pass


# Output
OUT = total, n