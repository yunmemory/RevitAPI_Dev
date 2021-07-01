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
schedule_definition = []
schedule_field_name = []
schedule_name = []

for s in schedule_collector:
    if not s.IsInternalKeynoteSchedule:
        if not s.IsTitleblockRevisionSchedule:
            if not s.IsTemplate:
                schedule_type.append(s)

for s in schedule_type:
    field = s.Definition.GetSchedulableFields()
    for d in field:
        schedule_definition.append(d.ParameterId)
        schedule_field_name.append(d.GetName(doc))

# Get sharedparameter elements
shared_para_ele = []
shared_para_ele_failed = []
for e in schedule_definition:
    parameter_ele = doc.GetElement(e)
    if parameter_ele is not None:
        shared_para_ele.append(parameter_ele.GuidValue + parameter_ele.Name)
    else:
        shared_para_ele_failed.append(e)

# Test 1
for s in schedule_type:
    field = s.Definition.GetSchedulableFields()
    for d in field:
        schedule_definition.append(d.ParameterId)
        schedule_field_name.append(d.GetName(doc))


OUT = shared_para_ele, shared_para_ele_failed