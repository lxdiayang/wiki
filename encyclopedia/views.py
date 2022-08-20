from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown2
import random
from django import forms

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput())
    content= forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":50}))

class EditForm(forms.Form):
    edits = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":50}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    page = util.get_entry(title)
    if page == None:
        page = markdown2.markdown(f'## \"{title.capitalize()}\" page not found')
    else:
        page = markdown2.markdown(page)

    return render(request, "encyclopedia/entry_page.html", {
        "title": title,
        "page": page
    })

def search(request):
    pages = util.list_entries()
    query = request.GET.get("q", "")
    if query in pages:
        return HttpResponseRedirect(reverse('entry_page', args=(query,)))
    results = []
    for page in pages:
        if query.lower() in page.lower():
            results.append(page)
    return render(request, "encyclopedia/index.html", {
        "entries": results
    })

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry_page", args=(title,)))
            else:
                return render(request, "encyclopedia/new_entry.html", {
                    "form": form,
                    "exists": True,
                    "entry_page": title
                })

        return render(request, "encyclopedia/new_entry.html", {
            "form": form,
            "exists": False
        })
    else:
        return render(request, "encyclopedia/new_entry.html", {
            "form": NewEntryForm(),
            "exists": False
        })

def edit(request, title): 
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            edits = form.cleaned_data["edits"]
            util.save_entry(title, edits)
            return HttpResponseRedirect(reverse("entry_page", args=(title,)))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "title": title
            })
    else:
        data = {"edits": util.get_entry(title)}
        return render(request, "encyclopedia/edit.html", {
            "form": EditForm(initial=data),
            "title":title
        })



def random_entry(request):
    entries = util.list_entries()
    rando = random.choice(entries)
    return HttpResponseRedirect(reverse("entry_page", args=(rando,)))
