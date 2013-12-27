from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import Context, loader
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from phonebook.models import Contact
import datetime
from phsite.widgets import CheckboxSelectMultiple
#from django.forms.widgets import CheckboxSelectMultiple

class ContactForm(forms.ModelForm):
    """
    A form to create a new Contact.
    """
    name = forms.CharField(label=_("Name"), max_length=200,
        help_text = _("Required. 200 characters or fewer."))

    ph_no= forms.IntegerField(label=_("Phone Number"),
        min_value=-9223372036854775808, max_value=9223372036854775807, required=False)

    email= forms.EmailField(label=_("Email Address"), max_length=200,
        help_text = _("200 characters or fewer."), required=False)
        
    user= forms.ModelMultipleChoiceField(queryset=User.objects.all().exclude(is_superuser=True),
        help_text = _("Hold down \"Control\", or \"Command\" on a Mac, to select more than one."), required=False, widget=CheckboxSelectMultiple())
    
    class Meta:
        model = Contact
 
class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password Confirmation"), widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))
    first_name= forms.CharField(label=_("First Name"), max_length=100,
        help_text = _("Required. 100 characters or fewer."))
    last_name= forms.CharField(label=_("Last Name"), max_length=100,
        help_text = _("Required. 100 characters or fewer."))
    email= forms.EmailField(label=_("Email Address"), max_length=200,
        help_text = _("Required. 200 characters or fewer."))

    class Meta:
        model = User
        fields = ("username",)

