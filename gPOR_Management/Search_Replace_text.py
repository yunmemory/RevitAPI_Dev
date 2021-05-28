import clr

clr.AddReference("RevitAPIUI")
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

text_notes = UnwrapElement(IN[0])
Sheet_numbers_old = IN[1]
Sheet_numbers_new = IN[2]
Run = IN[3]

# FIND AND REPLACE TEXT
text = []
text_id = []
view_id = []

if Run:
    for t in text_notes:
        text_formatted = t.GetFormattedText()
        text_contents = t.Text
        for s_old in Sheet_numbers_old:
            if s_old in text_contents:
                text_range = text_formatted.Find(s_old, 0, False, False)
                text_plain = text_formatted.GetPlainText(text_range)
                # text_plain = text_contents.Substring(text_range.Start, text_range.Length)
                s_index = Sheet_numbers_old.index(s_old)
                s_new = Sheet_numbers_new[s_index]
                # Start Transaction
                TransactionManager.Instance.EnsureInTransaction(doc)
                text_plain = text_plain.Replace(s_old, s_new)
                text_formatted.SetPlainText(text_range, text_plain)
                t.SetFormattedText(text_formatted)
                TransactionManager.Instance.TransactionTaskDone()
                # End Transaction
                text.append(text_plain)
                text_id.append(t.Id)
                view_id.append(t.OwnerViewId)

# out
OUT = text, text_id, view_id
