from django.db import models
from django.utils import timezone

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=100)
    image = models.ImageField(upload_to='produits/')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock_initial = models.PositiveIntegerField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.nom

    def stock_restant(self):
        ventes = self.vente_set.aggregate(total=models.Sum('quantite'))['total'] or 0
        return self.stock_initial - ventes


class Vente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.produit.nom} - {self.quantite} - {self.date}"

    def montant_total(self):
        return self.quantite * self.produit.prix

class Commande(models.Model):
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    quartier = models.CharField(max_length=100)
    secteur = models.CharField(max_length=100)
    code_confirmation = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande {self.code_confirmation} - {self.telephone}"

class CommandeItem(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="items")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    taille = models.CharField(max_length=5, default='M')  # Taille par défaut
    couleur = models.CharField(max_length=20, default='noir')  # Couleur par défaut

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite} ({self.taille}, {self.couleur})"



# Create your models here.
