from django.contrib import admin
from .models import Pharmacien, Avis

class AvisInline(admin.TabularInline):
    model = Avis
    extra = 0
    readonly_fields = ('auteur', 'note', 'commentaire', 'date_ajout')

class PharmacienAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'date_ajout', 'moyenne_notes')
    search_fields = ('nom', 'email', 'adresse')
    inlines = [AvisInline]

admin.site.register(Pharmacien, PharmacienAdmin)
admin.site.register(Avis)

# Register your models here.
from django.contrib import admin
from .models import Notation

class NotationAdmin(admin.ModelAdmin):
    list_display = ('pharmacien', 'note', 'auteur', 'service_satisfait', 'ecoute', 'revenir', 'date')
    list_filter = ('note', 'service_satisfait', 'ecoute', 'revenir')

admin.site.register(Notation, NotationAdmin)

