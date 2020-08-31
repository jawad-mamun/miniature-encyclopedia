from django.shortcuts import render

from . import util

from django import forms

import random


#imports convertor to convert markdown to html
from markdown2 import Markdown

markdowner = Markdown()

#using Django's form class to create form for entry searches
class EntryForm(forms.Form):
    entry_search = forms.CharField(label='Encyclopedia Search', max_length=100)

#using Django's form class to create form for creating a new page. Also is used for editing pages.
class NewPage(forms.Form):
    entry_name = forms.CharField(label='Page Name', max_length = 100)
    description = forms.CharField(label='Markdown Text (including entry name)', widget=forms.Textarea)

class EditPage(forms.Form):
    description = forms.CharField(label='Markdown Text (including entry name)', widget=forms.Textarea)

#helper method to accept search requests in the encyclopedia
def helper (request,form):
    form = EntryForm(request.POST)
    #this if statement checks for server side validation, client side validation is done automatically
    if form.is_valid():
        search = form.cleaned_data["entry_search"]
        #redirects to the right entry page if the entry exists
        if (util.get_entry(search)!=None):
            return render(request, "encyclopedia/entry.html", {
                "entry": search.capitalize(),
                "description": markdowner.convert(util.get_entry(search)),
                "form": form            
                })
        #redirects to a list of entries that have the query as a substring
        else:
            #what's the opposite of substring??? superstring!
            superstring = []
            #goes through all the entries and checks if query is a substring, adds to a list
            for super in util.list_entries():
                if (search.lower() in super.lower()):
                    superstring.append(super)
            return render(request, "encyclopedia/badsearch.html", {
                "superstring": superstring,
                "form": form
            })
    else:
        #pass in form so that the client can see what went wrong
        return render(request, "encyclopedia/index.html", {
        "form": form
        }) 

#has form to create a new page
def newpage(request):
    #uses form helper method to take entry from search bar 
    form = EntryForm(None)
    if request.method == "POST" and 'search' in request.POST:
        return helper(request, form)
    #form for creating a new page
    new_page = NewPage(request.POST or None)
    #this if statement checks for server side validation, client side validation is done automatically
    if new_page.is_valid():
        entry_name = new_page.cleaned_data["entry_name"]
        description = new_page.cleaned_data["description"]
        #combines the entry_name and description to create proper Markdown content
        #creates a new page with this entry if it does not already exist
        if(util.get_entry(entry_name) == None):
            util.save_entry(entry_name, description)
            return render(request, "encyclopedia/entry.html", {
                "entry": entry_name.capitalize(),
                "description": markdowner.convert(util.get_entry(entry_name)),
                "form": form
            })
        #leads to an error message if the entry already exists
        else:
            return render(request, "encyclopedia/newpage.html", {
                "new_page": new_page,
                "form": form,
                "error": "The page you have tried to create already exists. Please try again."
            })
    else:
        return render(request, "encyclopedia/newpage.html", {
        "new_page": new_page,
        "form": form
        }) 

def index(request):
    #uses form helper method to take entry from search bar 
    form = EntryForm(None)
    if request.method == "POST":
        return helper(request, form)
    #home page of the Encyclopedia 
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": form
    })

def entry(request, entry):
    #uses form helper method to take entry from search bar 
    form = EntryForm(None)
    if request.method == "POST":
        return helper(request, form)
    #if the entry is valid, returns that entry's page. if the entry is not valid, returns an error page
    if util.get_entry(entry) != None:
        #passes the entry name and the entry info to the html page
        return render(request, "encyclopedia/entry.html", {
        "entry": entry.capitalize(),
        "description": markdowner.convert(util.get_entry(entry)),
        "form": form
    })
    else:
        return render(request, "encyclopedia/notfound.html", {
            "form": form
        })

#function to be called when a page is edited that prefills the existing information
def edit(request, entry):
    #uses form helper method to take entry from search bar 
    form = EntryForm(None)
    if request.method == "POST" and 'search' in request.POST:
        return helper(request, form)

    #after the edit page submit button is pressed, updates the entry and goes to entry page
    if request.method == "POST" and 'editpage' in request.POST:
        edit_form = EditPage(request.POST or None)
        if edit_form.is_valid():
            description = edit_form.cleaned_data["description"]
            #saves the new information for the entry
            util.save_entry(entry, description)
            #redirects to the entry's page
            return render(request, "encyclopedia/entry.html", {
                "entry": entry.capitalize(),
                "description": markdowner.convert(util.get_entry(entry)),
                "form": form
            })
    #before the submit button is pressed, prefills the previous data of the page 
    else:
        edit_form = EditPage(initial = {'description':util.get_entry(entry)})
    #provides default view for the edit page
    return render(request, "encyclopedia/editpage.html",{
        "edit_form": edit_form,
        "entry": entry,
        "form": form        
        })

#goes to random page in encyclopedia
def randompage(request):
    #uses form helper method to take entry from search bar 
    form = EntryForm(None)
    if request.method == "POST" and 'search' in request.POST:
        return helper(request, form)
    #stores name of random entry
    n = random.choice(util.list_entries())
    #goes to page of random entry
    return render(request, "encyclopedia/entry.html", {
        "entry": n.capitalize(),
        "description": markdowner.convert(util.get_entry(n)),
        "form": form
    })

