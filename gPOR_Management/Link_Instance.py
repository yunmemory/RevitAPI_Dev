import clr

clr.AddReference("RevitAPIUI")
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Collect all the views on the sheets
sheet_views = UnwrapElement(IN[0])

# Exclude the drafting/schedule/Legend etc, views
Revit_viewtype = ["FloorPlan", "CeilingPlan", "Elevation", "ThreeD", "EngineeringPlan", "AreaPlan", "Section", "Detail"]
filtered_view = []
for v in sheet_views:
    if v.ViewType.ToString() in Revit_viewtype:
        filtered_view.append(v)

# Get the Revit link type
revit_elements = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_RvtLinks).WhereElementIsElementType().ToElements()
revit_non_nest = []
link_vi = []
link_uvi = []
view_link = []
full_list = []

# Get all Worksets and WorksetIds
worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
workset_id = [i.Id for i in worksets]
workset_visibility = []
workset_defalt = []
defaultVisibility = WorksetDefaultVisibilitySettings.GetWorksetDefaultVisibilitySettings(doc)
for w in worksets:
    w_id = w.Id
    w_name = w.Name
    setting = defaultVisibility.IsWorksetVisible(w_id)
    workset_defalt.append(w_name + "--" + setting.ToString())

# Remove the nested link type
for l in revit_elements:
    if not l.IsNestedLink:
        revit_non_nest.append(l.Id)
        full_list.append(Element.Name.__get__(l))

# Get the visibility status
for lid in revit_non_nest:
    link_name = Element.Name.__get__(doc.GetElement(lid))
    for view in filtered_view:
        if doc.GetElement(lid).IsHidden(view):
            link_vi.append(link_name + "--hide--" + view.Name)
        else:
            link_vi.append(link_name + "--show--" + view.Name)

# Get workset visibility
for v in filtered_view:
    v_name = v.Name
    for w in worksets:
        w_id = w.Id
        w_visibility = v.GetWorksetVisibility(w_id)
        w_name = w.Name
        workset_visibility.append(w_name + "--" + w_visibility.ToString() + "--" + v_name)

# for lid in revit_non_nest:
#     link_ele = doc.GetElement(lid)
#     link_name = Element.Name.__get__(doc.GetElement(lid))
#     if not link_ele.IsHidden(doc.ActiveView):
#         link_vi.append(link_name)
#     else:
#         link_uvi.append(link_name)
# # if "show" in link_vi:
# #     view_link.append(Element.Name.__get__(doc.GetElement(lid)))
# view_link.append(link_vi)


OUT = link_vi, workset_visibility, workset_defalt
