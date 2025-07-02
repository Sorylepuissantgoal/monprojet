from django.shortcuts import render, redirect
from .models import Produit, Commande, CommandeItem
from django.contrib import messages
import random

def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'boutique/liste_produits.html', {'produits': produits})


def ajouter_au_panier(request, produit_id):
    produit = Produit.objects.get(id=produit_id)
    taille = request.POST.get('taille')
    couleur = request.POST.get('couleur')

    panier = request.session.get('panier', {})

    key = f"{produit_id}-{taille}-{couleur}"
    if key in panier:
        panier[key]['quantite'] += 1
    else:
        panier[key] = {
            'produit_id': produit.id,
            'taille': taille,
            'couleur': couleur,
            'quantite': 1
        }

    request.session['panier'] = panier
    return redirect('voir_panier')


def voir_panier(request):
    panier = request.session.get('panier', {})
    produits = []

    for item in panier.values():
        try:
            produit = Produit.objects.get(id=item['produit_id'])
            produit.taille = item['taille']
            produit.couleur = item['couleur']
            produit.quantite = item['quantite']
            produit.sous_total = produit.prix * produit.quantite
            produits.append(produit)
        except Produit.DoesNotExist:
            continue

    total = sum([p.sous_total for p in produits])

    return render(request, 'boutique/panier.html', {
        'produits': produits,
        'total': total
    })


def retirer_du_panier(request, produit_id, taille, couleur):
    panier = request.session.get('panier', {})

    for key in list(panier.keys()):
        item = panier[key]
        if (
            item.get('produit_id') == produit_id and
            item.get('taille') == taille and
            item.get('couleur') == couleur
        ):
            del panier[key]
            break

    request.session['panier'] = panier
    return redirect('voir_panier')


def vider_panier(request):
    request.session['panier'] = {}
    return redirect('voir_panier')


def commande(request):
    code_confirmation = None
    if request.method == "POST":
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        quartier = request.POST.get('quartier')
        secteur = request.POST.get('secteur')

        if not telephone or not quartier:
            messages.error(request, "Veuillez remplir tous les champs requis.")
            return redirect('voir_panier')

        code_confirmation = random.randint(100000, 999999)

        commande = Commande.objects.create(
            telephone=telephone,
            email=email,
            quartier=quartier,
            secteur=secteur,
            code_confirmation=code_confirmation
        )

        panier = request.session.get('panier', {})
        for key, item in panier.items():
            try:
                produit_id = item.get('produit_id')
                if not produit_id or not str(produit_id).isdigit():
                    continue
                produit = Produit.objects.get(id=int(produit_id))
                CommandeItem.objects.create(
                    commande=commande,
                    produit=produit,
                    quantite=item['quantite']
                )
                produit.stock_initial -= item['quantite']
                produit.save()
            except Produit.DoesNotExist:
                continue

        request.session['panier'] = {}
        messages.success(request, f"Commande confirmée ! Code : {code_confirmation}")

    return render(request, 'boutique/commande.html', {
        'code_confirmation': code_confirmation
    })
def liste_categories(request):
    # Exemple simple à adapter
    categories = ['Chaussures', 'T-shirts', 'Pantalons']
    return render(request, 'boutique/liste_categories.html', {'categories': categories})
