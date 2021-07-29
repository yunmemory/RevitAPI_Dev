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

# Linked instance
revit_link_ins = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()

# Run linked model or not
run_link_model = IN[0]

para_elements = FilteredElementCollector(doc).OfClass(ParameterElement).ToElements()


def GetAllProjectParameters(doc):
    project_paras = []
    collector = FilteredElementCollector(doc).OfClass(ParameterElement).ToElements()
    for para in collector:
        if para.ToString() == "Autodesk.Revit.DB.ParameterElement":
            project_paras.append(para.Name)
    return project_paras


def GetAllSharedParameters(doc):
    collector = FilteredElementCollector(doc).OfClass(SharedParameterElement)
    return collector


# Check binding
def ParamBindingExists(doc, paramId):
    para_type = ""
    categories = []
    map = doc.ParameterBindings
    iterator = map.ForwardIterator()
    iterator.Reset()
    while iterator.MoveNext():
        if iterator.Key.Id == paramId:
            elemBind = iterator.Current
            if elemBind.ToString() == "Autodesk.Revit.DB.InstanceBinding":
                para_type = "Instance"
            else:
                para_type = "Type"
            for cat in elemBind.Categories:
                categories.append(cat.Name)
            break
    return categories, para_type


def GetSharedParameterReportData(doc):
    parameter_def_list = []
    doc_name = doc.Title
    for p in para_elements:
        pdef = p.GetDefinition()
        para_id = pdef.Id
        pbindings = ParamBindingExists(doc, para_id)
        para_cat = pbindings[0]
        para_typ = pbindings[1]
        if para_typ != "Instance" and para_typ != "Type":
            para_typ = "Not on PP list"
        if pdef.Id.IntegerValue > 0:
            parameter_def = p.GetDefinition()
            parameter_def_name = parameter_def.Name
            parameter_def_group = parameter_def.ParameterGroup.ToString()
            parameter_def_type = parameter_def.ParameterType.ToString()
            parameter_def_unit = parameter_def.UnitType.ToString()
            try:
                parameter_def_guid = p.GuidValue.ToString()
            except:
                parameter_def_guid = "Project Parameter"
            parameter_def_list.append([doc_name,
                                       parameter_def_name,
                                       para_typ,
                                       parameter_def_group,
                                       parameter_def_type,
                                       parameter_def_unit,
                                       parameter_def_guid,
                                       str(para_cat)])
        elif para_id.IntegerValue == -1:
            parameter_def_name = field.GetName()
            parameter_def_group = "NONE"
            parameter_def_type = "NONE"
            parameter_def_unit = "NONE"
            parameter_def_guid = "Combined/Formula Parameter"
            parameter_def_list.append([doc_name,
                                       parameter_def_name,
                                       para_typ,
                                       parameter_def_group,
                                       parameter_def_type,
                                       parameter_def_unit,
                                       parameter_def_guid])
        else:
            parameter_def_name = field.GetName()
            parameter_def_group = "NONE"
            parameter_def_type = "NONE"
            parameter_def_unit = "NONE"
            parameter_def_guid = "Built-In Parameter"
            parameter_def_list.append([doc_name,
                                       parameter_def_name,
                                       para_typ,
                                       parameter_def_group,
                                       parameter_def_type,
                                       parameter_def_unit,
                                       parameter_def_guid])
    return parameter_def_list


schedules_from_models = []

# Check to determine whether or not to run the linked models
if run_link_model:
    # Get schedules from linked instance
    for link in revit_link_ins:
        linked_doc = link.GetLinkDocument()
        if linked_doc is not None:
            schedules_from_models.append(GetSharedParameterReportData(linked_doc))

# Collect schedules from current model
schedules_from_models.append(GetSharedParameterReportData(doc))

# Output
OUT = schedules_from_models
