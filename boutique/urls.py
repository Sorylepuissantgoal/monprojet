from django.urls import path
from .views import (
    liste_produits,
    ajouter_au_panier,
    voir_panier,
    retirer_du_panier,
    vider_panier,
    liste_categories,
    produits_par_categorie,
    commande
)

urlpatterns = [
    path('', liste_produits, name='liste_produits'),
    path('ajouter-au-panier/<int:produit_id>/', ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', voir_panier, name='voir_panier'),
    path('retirer/<int:produit_id>/', retirer_du_panier, name='retirer_du_panier'),
    path('vider/', vider_panier, name='vider_panier'),
    path('categories/', liste_categories, name='liste_categories'),
    path('categorie/<int:categorie_id>/', produits_par_categorie, name='produits_par_categorie'),
    path('commande/', commande, name='commande'),

]




