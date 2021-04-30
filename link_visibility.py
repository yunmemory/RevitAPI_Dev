# link reference:
# https://forums.autodesk.com/t5/revit-api-forum/hide-unhide-revitlinkinstance-in-visibility-settings/td-p/8194955

"""
C# code:
/// Sample , Hide/Unhide a Revit Linked File
            UIApplication uiApp = commandData.Application;
            Document doc = uiApp.ActiveUIDocument.Document;

            //find the linked files
            FilteredElementCollector collector = new FilteredElementCollector(doc);
            ICollection<ElementId> elementIdSet =
              collector
              .OfCategory(BuiltInCategory.OST_RvtLinks)
              .OfClass(typeof(RevitLinkInstance))
              .ToElementIds();

            using (Transaction trans = new Transaction(doc, "LinkedFileVisibility"))
            {
                trans.Start();
                foreach (ElementId linkedFileId in elementIdSet)
                {
                    if (linkedFileId != null)
                    {
                        if (true == doc.GetElement(linkedFileId).IsHidden(doc.ActiveView))
                        {
                            if (true == doc.GetElement(linkedFileId).CanBeHidden(doc.ActiveView))
                            {
                                doc.ActiveView.UnhideElements(elementIdSet);
                            }
                        }
                        else
                        {
                            doc.ActiveView.HideElements(elementIdSet);
                        }
                    }
                }
                trans.Commit();
            }
            return Autodesk.Revit.UI.Result.Succeeded;
"""
