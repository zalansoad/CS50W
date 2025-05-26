from django.shortcuts import render, redirect
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    MD_entry = util.get_entry(title)
    if not MD_entry:
        return render(request, "encyclopedia/error.html",{
            "entry": "Page not found"
        })
    else:
        entry = markdown2.markdown(MD_entry)
        return render(request, "encyclopedia/entry.html", {
        "entry": entry
        })
    
def search(request):
    q = request.GET.get("q")
    entries = [entry.casefold() for entry in util.list_entries()]
    if q.casefold() in entries:
        return redirect("entry", title=q)
    else:
        results = []
        for item in entries:
            if q in item:
                results.append(item)
                            
        return render(request, "encyclopedia/results.html", {
        "results": results
        })



