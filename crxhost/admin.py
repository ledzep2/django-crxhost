from django.contrib.admin import site, ModelAdmin
from .models import *


class CRXPackageAdmin(ModelAdmin):
    list_display = ("active", "downloaded", "crx", "version", "timestamp")
    ordering = ("-id",)

class CRXIdAdmin(ModelAdmin):
    list_display = ("active", "name", "cid")

site.register(CRXPackage, CRXPackageAdmin)
site.register(CRXId, CRXIdAdmin)