from django.contrib import admin

from . import models

admin.site.register(models.Mouse)
admin.site.register(models.MouseTrait)
admin.site.register(models.Trait)
admin.site.register(models.Mating)
admin.site.register(models.Offspring)
admin.site.register(models.BinCage)
admin.site.register(models.MouseBinCage)
