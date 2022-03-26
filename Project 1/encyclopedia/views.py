from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from markdown2 import Markdown
from django.contrib import messages
from . import util
import random


class SearchForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search Encyclopedia"
    }))


class Create(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "placeholder": "Entry Title",
        'style': 'width: 30%;' 'margin-bottom: 10px;',
        'class': "form-control"
    }))

    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        "placeholder": "Enter page Content using Markdown",
        'style': 'width: 80%;' 'margin-bottom: 10px;',
        'class': "form-control"
    }))


class EditForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        "placeholder": "Enter page Content using Markdown",
        'style': 'width: 80%;' 'margin-bottom: 10px;',
        'class': "form-control"
    }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form" : SearchForm()
    })

def title(request, title):

    data = util.get_entry(title)

    if data != None:
        data_in_html = Markdown().convert(data)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "search_form" : SearchForm(),
            "entry": data_in_html
        })
    else:
        related_titles = util.related_titles(title)
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "related_titles": related_titles,
            "search_form" : SearchForm()
        })


def search(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        
        #if form is valid, use the view "title" to get to the page
        if form.is_valid():
            title = form.cleaned_data['title']
            data = util.get_entry(title)

            #print('search request: ', title)

            if data:
                return redirect(reverse('title', args=[title]))
            else:
                related_titles = util.related_titles(title)

                return render(request, "encyclopedia/search.html", {
                "search_form": SearchForm(),
                "related_titles": related_titles,
                "title": title})
    return redirect(reverse('index'))


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html",{
            "search_form": SearchForm(),
            "create": Create()
            })

    elif request.method == "POST":
        form = Create(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
        else:
            messages.error(request, 'Form not valid, please try again!')
            return render(request, "encyclopedia/create.html",{
            "search_form": SearchForm(),
            "create": Create()
            })

        #if file already exits, refill
        if util.get_entry(title):
            messages.error(request, 'This page already exists!')
            return render(request, "encyclopedia/create.html",{
            "search_form": SearchForm(),
            "create": Create()
            })
        
        else:
            util.save_entry(title, content)
            messages.success(request, f'New page "{title}" created sucessfully!')
            return redirect(reverse ('title', args=[title]))

def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)

        if content == None:
            messages.error(request, f'"{title}" page does not exist and can\'t be edited, please create a new page instead!')
        
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "search_form": SearchForm(),
            "edit_form": EditForm(initial={'content':content})
        })

    elif request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            messages.success(request, f'Entry "{title}" updated successfully!')
            return redirect(reverse('title', args=[title]))

        else:
            messages.error(request, f'Editing form not valid, please try again!')
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "edit_form": form,
                "search_form": SearchForm()
            })

def random_title(request):

    titles = util.list_entries()
    title = random.choice(titles)
    return redirect(reverse('title', args=[title]))
