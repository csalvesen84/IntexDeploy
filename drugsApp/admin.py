from django.contrib import admin
from drugsApp.models import Credential, Drugs, Prescriber, State, Triple, Specialty
# Register your models here.
admin.site.register(Credential)
admin.site.register(State)
admin.site.register(Drugs)
admin.site.register(Prescriber)
admin.site.register(Triple)
admin.site.register(Specialty)