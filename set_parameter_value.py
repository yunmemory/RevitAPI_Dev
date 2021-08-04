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
# app = DocumentManager.Instance.CurrentUIApplication.Application

# Parameter
element_id = IN[0]
parameters = IN[1]


# # get elements by id
# def get_elements(e_id):
#     elements_set = []
#     for i in e_id:
#         ele_id = ElementId(int(i))
#         elements_set.append(doc.GetElement(ele_id))
#     return elements_set


# # set parameter value
# def set_value(data_list, para_name):
#     para_output = []
#     for i in range(1, len(para_name)):
#         id_list = data_list[0]
#         para_value_list = data_list[i]
#         for e in range(len(id_list)):
#             ele_id = ElementId(int(id_list[e]))
#             elem = doc.GetElement(ele_id)
#             para = elem.LookupParameter(para_name[i])
#             if para is not None:
#                 if para.IsShared:
#                     TransactionManager.Instance.EnsureInTransaction(doc)
#                     para.Set(str(para_value_list[e]))
#                     TransactionManager.Instance.TransactionTaskDone()
#                     para_output.append([ele_id,
#                                       para_name[i],
#                                       str(para_value_list[e])])
#     return para_output


# set parameter value
def set_value(data_list, para_name):
    para_output = []
    id_list = data_list[0]
    for e in range(len(id_list)):
        ele_id = ElementId(int(id_list[e]))
        elem = doc.GetElement(ele_id)
        for i in range(1, len(para_name)):
            para_value_list = data_list[i]
            para = elem.LookupParameter(para_name[i])
            if para is not None and para.IsShared:
                TransactionManager.Instance.EnsureInTransaction(doc)
                para.Set(str(para_value_list[e]))
                TransactionManager.Instance.TransactionTaskDone()
                para_output.append([ele_id,
                                    para_name[i],
                                    str(para_value_list[e])])
    return para_output


setvalue = set_value(element_id, parameters)

# Assign your output to the OUT variable.
OUT = setvalue
