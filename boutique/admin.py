from django.contrib import admin
from .models import Commande 
from django.utils.html import format_html
from .models import Produit, Vente, Categorie, Commande, CommandeItem

class CommandeItemInline(admin.TabularInline):
    model = CommandeItem
    extra = 0
    readonly_fields = ['image_produit']

    def image_produit(self, obj):
        if obj.produit.image:
            return format_html('<img src="{}" width="60" height="60" />', obj.produit.image.url)
        return "Pas d'image"
    image_produit.short_description = "Image"

class CommandeAdmin(admin.ModelAdmin):
    inlines = [CommandeItemInline]

admin.site.register(Produit)
admin.site.register(Vente)
admin.site.register(Categorie)
admin.site.register(Commande, CommandeAdmin)



# Register your models here.
