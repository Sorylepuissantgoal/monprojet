from django.urls import path
from . import views
from boutique.views import (
    liste_produits,
    ajouter_au_panier,
    voir_panier,
    retirer_du_panier,
    vider_panier,
    commande
)

app_name = 'boutique'


urlpatterns = [
    path('', liste_produits, name='liste_produits'),
    path('ajouter-au-panier/<int:produit_id>/', ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', voir_panier, name='voir_panier'),
    path('retirer/<int:produit_id>/<str:taille>/<str:couleur>/', retirer_du_panier, name='retirer_du_panier'),
    path('vider/', vider_panier, name='vider_panier'),
    path('commande/', commande, name='commande'),
    path('categories/', views.liste_categories, name='liste_categories')
]





