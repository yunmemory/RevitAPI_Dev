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
schedule_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules).ToElements()

schedule_type = []
schedule_field_para = []
schedule_field_name = []
schedule_name = []

for s in schedule_collector:
    if not s.IsInternalKeynoteSchedule:
        if not s.IsTitleblockRevisionSchedule:
            if not s.IsTemplate:
                schedule_type.append(s)


# for s in schedule_type:
#     field = s.Definition.GetSchedulableFields()
#     for d in field:
#         schedule_field_para.append(d.ParameterId)
#         schedule_field_name.append(d.GetName(doc))
#
# # Get sharedparameter elements
# shared_para_ele = []
# shared_para_ele_failed = []
# for e in schedule_field_para:
#     parameter_ele = doc.GetElement(e)
#     if parameter_ele is not None:
#         shared_para_ele.append(parameter_ele.GuidValue + parameter_ele.Name)
#     else:
#         shared_para_ele_failed.append(e)

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


# Test 1
parameter_def_list = []
for s in schedule_type:
    pdef = s.Definition
    field_count = pdef.GetFieldCount()
    for i in range(field_count):
        field = pdef.GetField(i)
        para_id = field.ParameterId
        pbindings = ParamBindingExists(doc, para_id)
        para_cat = pbindings[0]
        para_typ = pbindings[1]
        if para_typ != "Instance" and para_typ != "Type":
            para_typ = "Not on PP list"
        if para_id.IntegerValue > 0:
            parameter_ele = doc.GetElement(para_id)
            parameter_def = parameter_ele.GetDefinition()
            parameter_def_name = parameter_def.Name
            parameter_def_group = parameter_def.ParameterGroup.ToString()
            parameter_def_type = parameter_def.ParameterType.ToString()
            parameter_def_unit = parameter_def.UnitType.ToString()
            try:
                parameter_def_guid = parameter_ele.GuidValue.ToString()
            except:
                parameter_def_guid = "Project Parameter"
            parameter_def_list.append([s.Name,
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
            parameter_def_list.append([s.Name,
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
            parameter_def_list.append([s.Name,
                                       parameter_def_name,
                                       para_typ,
                                       parameter_def_group,
                                       parameter_def_type,
                                       parameter_def_unit,
                                       parameter_def_guid])

OUT = parameter_def_list
