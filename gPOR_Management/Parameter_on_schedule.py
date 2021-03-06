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

# Get current document --------------------------------------------------
doc = DocumentManager.Instance.CurrentDBDocument

# Collect schedules from current model
schedule_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules).ToElements()

# Linked instance
revit_link_ins = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()

# Run linked model or not
run_link_model = IN[0]


# Schedule filter
def schedule_filter(schedule_set):
    filter_schedule = []
    for s in schedule_set:
        if not s.IsInternalKeynoteSchedule:
            if not s.IsTitleblockRevisionSchedule:
                if not s.IsTemplate:
                    filter_schedule.append(s)
    return filter_schedule


# Check binding
def ParamBindingExists(document, paramId):
    para_type = ""
    categories = []
    map = document.ParameterBindings
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


# Get the parameter details
def get_para_details(document, schedule):
    parameter_def_list = []
    doc_name = document.Title
    for s in schedule:
        para_def = s.Definition
        field_count = para_def.GetFieldCount()
        for i in range(field_count):
            field = para_def.GetField(i)
            para_id = field.ParameterId
            p_bindings = ParamBindingExists(document, para_id)
            para_cat = p_bindings[0]
            para_typ = p_bindings[1]
            if para_typ != "Instance" and para_typ != "Type":
                para_typ = "Not on PP list"
            if para_id.IntegerValue > 0:
                parameter_ele = document.GetElement(para_id)
                parameter_def = parameter_ele.GetDefinition()
                parameter_def_name = parameter_def.Name
                parameter_def_group = parameter_def.ParameterGroup.ToString()
                parameter_def_type = parameter_def.ParameterType.ToString()
                parameter_def_unit = parameter_def.UnitType.ToString()
                try:
                    parameter_def_guid = parameter_ele.GuidValue.ToString()
                except:
                    parameter_def_guid = "Project Parameter"
                parameter_def_list.append([doc_name,
                                           s.Name,
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
                                           s.Name,
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
                                           s.Name,
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
            schedules = FilteredElementCollector(linked_doc).OfCategory(BuiltInCategory.OST_Schedules).ToElements()
            f_schedule = schedule_filter(schedules)
            schedules_from_models.append(get_para_details(linked_doc, f_schedule))

# Collect schedules from current model
f_schedule_current = schedule_filter(schedule_collector)
schedules_from_models.append(get_para_details(doc, f_schedule_current))

# Output
OUT = schedules_from_models
