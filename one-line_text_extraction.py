import csv
import os
import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import System
from System.Collections.Generic import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

view_filter = ElementCategoryFilter(BuiltInCategory.OST_TextNotes)

if isinstance(IN[0], list):
    sheets = UnwrapElement(IN[0])
else:
    sheets = [UnwrapElement(IN[0])]

sheet_number = IN[1]

file_path = IN[2]

overall = []

for views in sheets:
    draft_set = [v for v in views if str(v.ViewType) == "DraftingView"]
    # get the vieid and elements

    view_id = [Element.Id.__get__(s) for s in draft_set]

    all_text = []

    for each in view_id:
        View_ele = FilteredElementCollector(doc, each).WherePasses(view_filter).ToElements()
        text = [ele.Text.strip() for ele in View_ele]
        # replace space
        text = [t.replace(" ", "-") for t in text]
        # replace newline
        text = [t.replace("\r\n", "-") for t in text]
        text = [t.encode('ascii', "ignore").decode('ascii') for t in text]
        all_text.extend(text)
    overall.append(all_text)

# CREATE A DIC FOR NUMBER AND CONTENT
dictionary = {}
for n in range(len(sheet_number)):
    dictionary[sheet_number[n]] = overall[n]

# for n in range(len(sheet_number)):
#     # dictionary[sheet_number[n]] = overall[n]
#     file_name = file_path + sheet_number[n]
#     with open(file_path, 'wb') as output:
#         writer = csv.writer(output)
#         writer.writerows(overall[n])

OUT = dictionary
