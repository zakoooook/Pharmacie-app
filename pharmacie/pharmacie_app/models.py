from django.db import models
from django.contrib.auth.models import User

class Pharmacien(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='pharmaciens/', blank=True, null=True)
    description = models.TextField(blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    def moyenne_notes(self):
        avis = self.avis_set.all()
        if avis.exists():
            return round(sum([a.note for a in avis]) / avis.count(), 2)
        return None

class Avis(models.Model):
    pharmacien = models.ForeignKey(Pharmacien, on_delete=models.CASCADE)
    auteur = models.CharField(max_length=100)
    note = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField()
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auteur} - {self.pharmacien.nom} ({self.note}/5)"
from django.db import models

class Notation(models.Model):
    pharmacien = models.ForeignKey('Pharmacien', on_delete=models.CASCADE)
    auteur = models.CharField(max_length=100, blank=True)
    note = models.IntegerField()
    commentaire = models.TextField(blank=True)
    
    service_satisfait = models.CharField(max_length=3, choices=[('oui', 'Oui'), ('non', 'Non')])
    ecoute = models.CharField(max_length=3, choices=[('oui', 'Oui'), ('non', 'Non')])
    revenir = models.CharField(max_length=3, choices=[('oui', 'Oui'), ('non', 'Non')])

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pharmacien.nom} - {self.note}/5"
