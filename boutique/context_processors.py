def panier(request):
    panier = request.session.get('panier', {})
    total_articles = sum(item['quantite'] for item in panier.values())

    return {
        'panier': {
            'total_articles': total_articles
        },
        'panier_count': total_articles
    }

