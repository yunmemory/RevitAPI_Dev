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
    project_shared_para = []
    family_shared_para = []
    paras = GetAllSharedParameters(doc)
    for p in paras:
        pdef = p.GetDefinition()
        pbindings = ParamBindingExists(doc, pdef.Id)
        para_cat = pbindings[0]
        para_typ = pbindings[1]
        if len(pbindings[0]) > 0:
            project_shared_para.append([
                p.GuidValue.ToString(),
                str(p.Id.IntegerValue),
                Element.Name.GetValue(p),
                para_typ,
                pdef.ParameterType.ToString(),
                pdef.ParameterGroup.ToString(),
                pdef.UnitType.ToString(),
                str(para_cat)
            ])
        else:
            family_shared_para.append([
                p.GuidValue.ToString(),
                str(p.Id.IntegerValue),
                Element.Name.GetValue(p),
                para_typ,
                pdef.ParameterType.ToString(),
                pdef.ParameterGroup.ToString(),
                pdef.UnitType.ToString(),
                str("None")
            ])
    return project_shared_para, family_shared_para


shared_parameters = GetSharedParameterReportData(doc)
project_shared_parameters = shared_parameters[0]
family_shared_parameters = shared_parameters[1]
project_para = GetAllProjectParameters(doc)

OUT = project_shared_parameters, family_shared_parameters
