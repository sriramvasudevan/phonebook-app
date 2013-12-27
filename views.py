from django import forms
#from django.contrib.auth.forms import UserCreationForm
from phsite.forms import UserCreationForm, ContactForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from phonebook.models import Contact
from django.db.models import Q
from django import forms
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                password1 = form.cleaned_data.get("password1", "")
                password2 = form.cleaned_data["password2"]
                if password1 != password2:
                    raise forms.ValidationError(_("The two password fields didn't match."))
                first_name=form.cleaned_data["first_name"]
                last_name=form.cleaned_data["last_name"]
                email=form.cleaned_data["email"]
                password=form.cleaned_data["password1"]
                u=User(username=username,first_name=first_name,last_name=last_name,email=email)
                u.set_password(password)
                u.save()
                return render_to_response("registration/register_success.html")
            raise forms.ValidationError(_("A user with that username already exists."))
            #new_user = form.save()

    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {'form': form,},context_instance=RequestContext(request))
    
def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    contact_edited = request.GET.get('ced', None)
    contact_added = request.GET.get('cad', None)
    contact_exists = request.GET.get('cex', None)
    contact=Contact.objects.filter(user=request.user)
    if request.user.is_superuser:
        contact=Contact.objects.all()
    count=contact.count()
    return render_to_response("home.html",locals())

def del_contact(request, userid):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    try:
        contact=Contact.objects.get(pk=userid)
    except Contact.DoesNotExist:
        return HttpResponseRedirect('/')
    if not request.user in contact.user.all() and not request.user.is_superuser:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        if 'yes' in request.POST:
            if request.user.is_superuser:
                contact.delete()
            else:
                contact.user.remove(request.user)
                if not contact.user.all(): #remove empty contacts
                    contact.delete()
            return HttpResponseRedirect('/home/')
        if 'no' in request.POST:
            return HttpResponseRedirect('/home/')
    return render_to_response("del_contact.html", locals(),context_instance=RequestContext(request))
    
def search_contact(request):    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    contact=Contact.objects.filter(pk=0)
    if request.method == 'POST':
        query=request.POST["search"]
        contact=Contact.objects.filter(Q(user=request.user),
                                       Q(name__icontains=query) | Q(ph_no__contains=query) | Q(email__icontains=query))
        if request.user.is_superuser:
            contact=Contact.objects.filter(Q(name__icontains=query) | Q(ph_no__contains=query) | Q(email__icontains=query))
        count=contact.count()
    return render_to_response("search_contact.html", locals(),context_instance=RequestContext(request))

def add_contact(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    contact=Contact.objects.filter(pk=0)
    create_contact=1
    edit_contact=0
    form=ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if not request.user.is_superuser:
                name=form.cleaned_data['name']
                ph_no=form.cleaned_data['ph_no']
                email=form.cleaned_data['email']
                timestamp=datetime.datetime.now()
                try:
                    c1=Contact.objects.get(ph_no=ph_no, name=name, email=email)
                except Contact.DoesNotExist:
                    c=Contact(name=name,ph_no=ph_no,email=email,timestamp=timestamp)
                    c.save()
                    c.user.add(request.user)
                    
                    return HttpResponseRedirect("/home/?cad=1")
                if  request.user in c1.user.all():
                    
                    return HttpResponseRedirect("/home/?cex=1")
                else:
                    c1.user.add(request.user)
                    
                    return HttpResponseRedirect("/home/?cad=1")
            else:
                name=form.cleaned_data['name']
                ph_no=form.cleaned_data['ph_no']
                email=form.cleaned_data['email']
                timestamp=datetime.datetime.now()
                users=form.cleaned_data['user']
                try:
                    c1=Contact.objects.get(ph_no=ph_no, name=name, email=email)
                except Contact.DoesNotExist:
                    c=Contact(name=name,ph_no=ph_no,email=email,timestamp=timestamp)
                    c.save()
                    for u in users:
                        c.user.add(u)
                    
                    return HttpResponseRedirect("/home/?cad=1")
                
                return HttpResponseRedirect("/home/?cex=1")
    return render_to_response("add_contact.html", locals(),context_instance=RequestContext(request))

def edit_contact(request, userid):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    try:
        contact=Contact.objects.get(pk=userid)
    except Contact.DoesNotExist:
        return HttpResponseRedirect('/')
    if not request.user in contact.user.all() and not request.user.is_superuser:
        return HttpResponseRedirect('/')
    form=ContactForm(instance=contact)
    create_contact=0
    edit_contact=1
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if not request.user.is_superuser:
                name=form.cleaned_data['name']
                ph_no=form.cleaned_data['ph_no']
                email=form.cleaned_data['email']
                timestamp=datetime.datetime.now()
                try:
                    c1=Contact.objects.get(ph_no=ph_no, name=name, email=email)
                except Contact.DoesNotExist:
                    contact.user.remove(request.user)
                    if not contact.user.all():#remove empty contacts
                        contact.delete()
                    c=Contact(name=name,ph_no=ph_no,email=email,timestamp=timestamp)
                    c.save()
                    c.user.add(request.user)
                    
                    return HttpResponseRedirect("/home/?ced=1")
                if c1==contact:
                    
                    return HttpResponseRedirect("/home/?ced=1")
                if request.user in c1.user.all():
                    
                    return HttpResponseRedirect("/home/?cex=1")
                else:
                    c1.user.add(request.user)
                    contact.user.remove(request.user)
                    if not contact.user.all(): #remove empty contacts
                        contact.delete()
                    
                    return HttpResponseRedirect("/home/?ced=1")
            else:
                name=form.cleaned_data['name']
                ph_no=form.cleaned_data['ph_no']
                email=form.cleaned_data['email']
                timestamp=datetime.datetime.now()
                users=form.cleaned_data['user']
                try:
                    c1=Contact.objects.get(ph_no=ph_no, name=name, email=email)
                except Contact.DoesNotExist:
                    contact.delete()
                    c=Contact(name=name,ph_no=ph_no,email=email,timestamp=timestamp)
                    c.save()
                    for u in users:
                        c.user.add(u)
                    contact_edited=1
                    return HttpResponseRedirect("/home/?ced=1")
                if c1==contact:
                    contact.delete()
                    c=Contact(name=name,ph_no=ph_no,email=email,timestamp=timestamp)
                    c.save()
                    for u in users:
                        c.user.add(u)
                    contact_edited=1
                    return HttpResponseRedirect("/home/?ced=1")
                
                return HttpResponseRedirect("/home/?cex=1")
                
        
    return render_to_response("add_contact.html", locals(),context_instance=RequestContext(request))

