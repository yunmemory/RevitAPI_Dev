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

# Test 1
parameter_def_list = []
for s in schedule_type:
    definition = s.Definition
    field_count = definition.GetFieldCount()
    for i in range(field_count):
        field = definition.GetField(i)
        para_id = field.ParameterId
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
                parameter_def_guid = "None"
            parameter_def_list.append(s.Name + "--" + parameter_def_name + "--" + parameter_def_group + "--" +
                                      parameter_def_type + "--" + parameter_def_unit + "--" + parameter_def_guid)
        elif para_id.IntegerValue < 0:
            parameter_def_name = field.GetName()
            parameter_def_group = "NONE"
            parameter_def_type = "NONE"
            parameter_def_unit = "NONE"
            parameter_def_guid = "NONE"
            parameter_def_list.append(s.Name + "--" + parameter_def_name + "--" + parameter_def_group + "--" +
                                      parameter_def_type + "--" + parameter_def_unit + "--" + parameter_def_guid)

        # parameter_ele = doc.GetElement(p)
        # if parameter_ele is not None:
        #     parameter_def = parameter_ele.GetDefinition()
        #     try:
        #         parameter_def_name = parameter_def.Name
        #         parameter_def_group = parameter_def.ParameterGroup
        #         parameter_def_type = parameter_def.ParameterType
        #         parameter_def_unit = parameter_def.UnitType
        #         parameter_def_list.append(parameter_def_name + "--" + parameter_def_group + "--" +
        # #                                   parameter_def_type + "--" + parameter_def_unit)
        #     except:
        #         parameter_def_list.append("null")

OUT = parameter_def_list
