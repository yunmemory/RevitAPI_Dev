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

pipe = UnwrapElement(IN[0])
fittings = UnwrapElement(IN[1])

n = 0
# transaction start
TransactionManager.Instance.EnsureInTransaction(doc)
for p in pipe:
    p = Element.SetParameterByName(p, "Type Mark", n)

TransactionManager.Instance.TransactionTaskDone()