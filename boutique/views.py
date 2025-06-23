from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Produit, Commande, CommandeItem, Categorie
import random

# Affichage de la liste des produits
def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'boutique/liste_produits.html', {'produits': produits})

# Ajout d’un produit au panier
def ajouter_au_panier(request, produit_id):
    if request.method == "POST":
        quantite = int(request.POST.get('quantite', 1))
        taille = request.POST.get('taille', 'M')
        couleur = request.POST.get('couleur', 'noir')

        key = f"{produit_id}_{taille}_{couleur}"
        panier = request.session.get('panier', {})

        if key in panier:
            panier[key]['quantite'] += quantite
        else:
            panier[key] = {
                'produit_id': produit_id,
                'quantite': quantite,
                'taille': taille,
                'couleur': couleur
            }

        request.session['panier'] = panier
        return redirect('liste_produits')

# Affichage du panier
def voir_panier(request):
    panier = request.session.get('panier', {})
    produits = []
    total = 0

    for key, item in panier.items():
        try:
            produit_id = item.get('produit_id')
            if not produit_id or not str(produit_id).isdigit():
                continue

            produit = Produit.objects.get(id=int(produit_id))
            produit.quantite = item['quantite']
            produit.taille = item['taille']
            produit.couleur = item['couleur']
            produit.sous_total = produit.quantite * produit.prix

            produits.append(produit)
            total += produit.sous_total
        except Produit.DoesNotExist:
            continue

    return render(request, 'boutique/panier.html', {'produits': produits, 'total': total})

# Suppression d’un produit du panier
def retirer_du_panier(request, produit_id):
    panier = request.session.get('panier', {})
    if produit_id in panier:
        del panier[produit_id]
        request.session['panier'] = panier
    return redirect('voir_panier')

# Vider le panier
def vider_panier(request):
    request.session['panier'] = {}
    return redirect('voir_panier')

# Produits par catégorie
def produits_par_categorie(request, categorie_id):
    produits = Produit.objects.filter(categorie_id=categorie_id)
    return render(request, 'boutique/liste_produits.html', {'produits': produits})

# Liste des catégories
def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'boutique/liste_categories.html', {'categories': categories})

# Traitement d'une commande
def commande(request):
    code_confirmation = None

    if request.method == "POST":
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        quartier = request.POST.get('quartier')
        secteur = request.POST.get('secteur')
        code_confirmation = random.randint(100000, 999999)

        commande = Commande.objects.create(
            telephone=telephone,
            email=email,
            quartier=quartier,
            secteur=secteur,
            code_confirmation=code_confirmation
        )

        panier = request.session.get('panier', {})

        # Ajout des produits à la commande
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
            except Produit.DoesNotExist:
                continue

        # Mise à jour du stock
        for key, item in panier.items():
            try:
                produit_id = item.get('produit_id')
                if not produit_id or not str(produit_id).isdigit():
                    continue

                produit = Produit.objects.get(id=int(produit_id))
                produit.stock_initial -= item['quantite']
                produit.save()
            except Produit.DoesNotExist:
                pass

        # Envoi du mail de confirmation
        #send_mail(
        #   'Confirmation de commande',
        #    f'Votre commande a été confirmée avec succès.\nVoici votre code : {code_confirmation}',
        #    settings.EMAIL_HOST_USER,
        #    [email],
        #    fail_silently=False
        #)

        # Vider le panier
        request.session['panier'] = {}

    return render(request, 'boutique/commande.html', {
        'code_confirmation': code_confirmation
    })
