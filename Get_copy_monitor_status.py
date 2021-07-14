import clr
import sys

sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import System
from System import Array
from System.Collections.Generic import *

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

doc = DocumentManager.Instance.CurrentDBDocument

# Get model categories
EX_LIST = ["Air terminals", "Communication devices", "Data devices", "Electrical equipment", "Electrical fixtures",
           "Fire alarm devices", "Lighting devices", "Lighting fixtures", "Mechanical equipment", "Nurse call devices",
           "Plumbing fixtures", "Security devices", "Sprinklers", "Telephone devices", "Levels", "Grids", "Columns",
           "Walls", "Floors", "Openings"]
cat = doc.Settings.Categories
cat_Ids = [t.Id for t in cat if t.Name in EX_LIST]

# Get elements for model categories
ele = []
for cat_id in cat_Ids:
    ele.extend(FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategoryId(cat_id))

OUT = cat_Ids, ele