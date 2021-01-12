import markdown2 as md
from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

from . import util

class NewPage(forms.Form):
    page = forms.CharField(label="New Page")

class NewSearch(forms.Form):
    search = forms.CharField(label="New Search")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    mark = md.Markdown()
    if request.method == "POST":
        title = request.POST['t']
        content = request.POST['c']
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "title": title,
                "already": True
            })
        util.save_entry(title, content)
        return render(request, "encyclopedia/title.html", {
                "title": title,
                "content": mark.convert(content)
            })
    return render(request, "encyclopedia/create.html")

def randomPage(request):
    mark = md.Markdown()
    entries = util.list_entries()
    entry = random.choice(entries)
    return render(request, "encyclopedia/title.html", {
        "title": entry,
        "content": mark.convert(util.get_entry(entry))
    })

def search(request):
    mark = md.Markdown()
    if request.method == "POST":
        query = request.POST['q']
        entries = util.list_entries()
        matches = []
        for entry in entries:
            if query.lower() == entry.lower():
                return render(request, "encyclopedia/title.html", {
                    "title": entry,
                    "content": mark.convert(util.get_entry(entry))
            })
        else:
            for entry in entries:
                if query.lower() in entry.lower():
                    matches.append(entry)
            if len(matches) == 0:
                return render(request, "encyclopedia/error.html", {
                    "title": query,
                    "already": False
                })
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "matches": matches
            })

def title(request, title):
    entries = util.list_entries()
    lEntries= [entry.lower() for entry in entries]
    mark = md.Markdown()
    for x in range(len(entries)):
        if title.lower() == lEntries[x]:
            return render(request, "encyclopedia/title.html", {
                "title": entries[x],
                "content": mark.convert(util.get_entry(entries[x]))
            })
    return render(request, "encyclopedia/error.html", {
            "title": title,
            "already": False
        })
    
def edit(request, title):
    mark = md.Markdown()
    if request.method == "POST":
        title = request.POST['t']
        content = request.POST['q']
        util.save_entry(title, content)
        return render(request, "encyclopedia/title.html", {
                "title": title,
                "content": mark.convert(content)
            })
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title)
    })
