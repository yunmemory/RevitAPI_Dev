# Load the Python Standard and DesignScript Libraries
import sys
import clr

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
cat = doc.Settings.Categories
cat_Ids = [t.Id for t in cat if str(t.CategoryType) == "Model"]

# Get elements for model categories
ele = []
for cat_id in cat_Ids:
    ele.extend(FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategoryId(cat_id))

# Parameter
parameter = IN[0]
tp_parameters = IN[1]


# function: get parameter value
def get_value(element, parameters):
    sub_group = []
    sub_group.append(element.Id)
    sub_group.append(Element.Name.__get__(element))

    # Get Type Name
    try:
        ele_type = doc.GetElement(element.GetTypeId())
        sub_group.append(ele_type)
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
            ele_type = doc.GetElement(element.GetTypeId())
            para = ele_type.LookupParameter(tp)
            sub_group.append(para.AsString())
        except:
            sub_group.append("null")

    # Get Location_Point
    try:
        sub_group.append(element.Location.Point)
    except:
        sub_group.append("null")

    # Get Location_Curve
    try:
        sub_group.append(element.Location.Curve.GetEndPoint(0))
    except:
        sub_group.append("null")

    return sub_group


# get parameter value for all elements
out = []
ele_name = ["Element_Id", "Element_Name", "Type_Name", "Phase_Created", "Phase_demolished", "Workset", "Level"]
location = ["Locatin_Point", "Location_Curve"]
for e in ele:
    p_value = get_value(e, parameter)
    out.append(p_value)
parameter = ele_name + parameter + tp_parameters + location
out.insert(0, parameter)

# Assign your output to the OUT variable.
OUT = out
