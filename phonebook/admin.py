from phonebook.models import Contact
from django.contrib import admin

#class ContactInline(admin.TabularInline):
#   model = Contact
#   extra = 1
   
class ContactAdmin(admin.ModelAdmin):
    filter_horizontal= ("user",)
    list_display = ('name', 'ph_no', 'email', 'timestamp',)

admin.site.register(Contact, ContactAdmin)
