# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
#from Autodesk.Revit.UI import *
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

# Current document
doc = DocumentManager.Instance.CurrentDBDocument

# Collect the filtered elements
family = FilteredElementCollector(doc).OfClass(FamilyType).ToElements()


# Place your code below this line

# Assign your output to the OUT variable.
OUT = family