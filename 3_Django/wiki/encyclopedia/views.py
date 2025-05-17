from django.shortcuts import render
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
    



