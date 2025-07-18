# Generated by Django 5.2.3 on 2025-06-19 22:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0003_commande'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveIntegerField()),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='boutique.commande')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boutique.produit')),
            ],
        ),
    ]
