import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.Exceptions import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitNodes")
import Revit
from Revit.Elements import *

# Path
fam_path = "C:\\Users\\Yunze's\\Downloads\\fam"

doc = DocumentManager.Instance.CurrentDBDocument
family_collector = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
families = [f for f in family_collector]

for f in families:
    famDoc = doc.EditFamily(f)
    famDoc.SaveAs(fam_path)
    famDoc.Close(False)