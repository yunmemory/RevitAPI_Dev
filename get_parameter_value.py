# Load the Python Standard and DesignScript Libraries
import sys
import clr
import csv

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# from Autodesk.Revit.UI import *
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Current document
doc = DocumentManager.Instance.CurrentDBDocument

# Get model categories
EX_LIST = ["Lines", "Detail Items", "RVT Links", "Imports in Families", "Project Information", "Sheets", "Coordination Model"]
cat = doc.Settings.Categories
cat_Ids = [t.Id for t in cat if str(t.CategoryType) == "Model" and t.Name not in EX_LIST]

# Get elements for model categories
ele = []
for cat_id in cat_Ids:
    ele.extend(FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategoryId(cat_id))

# Parameter
parameter = IN[0]
tp_parameters = IN[1]
FILE = IN[2]
Separator = IN[3]


# function: get parameter value
def get_value(element, parameters):
    sub_group = []
    sub_group.append(element.Id)
    sub_group.append(element.Category.Name)
    sub_group.append(Element.Name.__get__(element))

    # Get Family Name
    try:
        # ele_type = doc.GetElement(element.GetTypeId())
        ele_type = element.Symbol.Family
        ele_type_name = Element.Name.__get__(ele_type)
        sub_group.append(ele_type_name)
    except:
        sub_group.append("null")

    # Get Phase_Created Name
    try:
        sub_group.append(doc.GetElement(element.CreatedPhaseId).Name)
    except:
        sub_group.append("null")

    # Get Phase_Demo Name
    try:
        sub_group.append(doc.GetElement(element.DemolishedPhaseId).Name)
    except:
        sub_group.append("null")

    # # Get Workset Name
    sub_group.append(doc.GetWorksetTable().GetWorkset(element.WorksetId).Name)

    # Get Level Name
    try:
        sub_group.append(doc.GetElement(element.LevelId).Name)
    except:
        sub_group.append("null")

    # Get Parameter value
    for p in parameters:
        para = element.LookupParameter(p)
        if para is None:
            sub_group.append("null")
        else:
            sub_group.append(para.AsString())

    # Get Type Value
    for tp in tp_parameters:
        try:
            #ele_type = doc.GetElement(element.GetTypeId())
            ele_type = element.Symbol
            para = ele_type.LookupParameter(tp)
            sub_group.append(para.AsString())
        except:
            sub_group.append("null")

    # Get Location_Point
    try:
        sub_group.append(round(element.Location.Point.X, 4))
        sub_group.append(round(element.Location.Point.Y, 4))
        sub_group.append(round(element.Location.Point.Z, 4))
    except:
        pass

    # Get Location_Curve
    try:
        sub_group.append(round(element.Location.Curve.GetEndPoint(0).X, 4))
        sub_group.append(round(element.Location.Curve.GetEndPoint(0).Y, 4))
        sub_group.append(round(element.Location.Curve.GetEndPoint(0).Z, 4))
    except:
        pass

    return sub_group


# get parameter value for all elements
out = []
ele_name = ["Element_Id", "Category", "Type_Name", "Element_Name", "Phase_Created", "Phase_demolished", "Workset", "Level"]
location = ["Locatin_X", "Locatin_Y", "Locatin_Z"]
for e in ele:
    p_value = get_value(e, parameter)
    out.append(p_value)
parameter = ele_name + parameter + tp_parameters + location
out.insert(0, parameter)

with open(FILE, "w") as csvfile:
    writer = csv.writer(csvfile, delimiter=Separator)
    writer.writerows(out)

# Assign your output to the OUT variable.
OUT = out
