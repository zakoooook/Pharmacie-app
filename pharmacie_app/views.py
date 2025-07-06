from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import Pharmacien, Avis
from .forms import UsernameAuthenticationForm
from django.contrib import messages


# Visiteurs : liste des pharmaciens

def liste_pharmaciens(request):
    pharmaciens = Pharmacien.objects.all()
    return render(request, 'pharmacie_app/liste_pharmaciens.html', {'pharmaciens': pharmaciens})

# Visiteurs : détail pharmacien + avis

def detail_pharmacien(request, pk):
    pharmacien = get_object_or_404(Pharmacien, pk=pk)
    avis = pharmacien.avis_set.order_by('-date_ajout')
    return render(request, 'pharmacie_app/detail_pharmacien.html', {'pharmacien': pharmacien, 'avis': avis})

# Visiteurs : noter/commenter un pharmacien

def noter_pharmacien(request, pk):
    pharmacien = get_object_or_404(Pharmacien, pk=pk)
    if request.method == 'POST':
        auteur = request.POST.get('auteur', 'Anonyme')
        note = int(request.POST.get('note', 0))
        commentaire = request.POST.get('commentaire', '')
        if 1 <= note <= 5 and commentaire:
            Avis.objects.create(pharmacien=pharmacien, auteur=auteur, note=note, commentaire=commentaire)
            messages.success(request, "Merci pour votre avis !")
        else:
            messages.error(request, "Veuillez fournir une note et un commentaire.")
        return redirect('liste_pharmaciens')
    return render(request, 'pharmacie_app/noter_pharmacien.html', {'pharmacien': pharmacien})

# Vérification admin

def is_admin(user):
    return user.is_staff

# Connexion personnalisée (email/mot de passe)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_admin')
    form = UsernameAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard_admin')
    return render(request, 'pharmacie_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Admin : liste et gestion pharmaciens

@login_required
@user_passes_test(is_admin)
def admin_pharmaciens(request):
    pharmaciens = Pharmacien.objects.all()
    return render(request, 'pharmacie_app/admin_pharmaciens.html', {'pharmaciens': pharmaciens})

@login_required
@user_passes_test(is_admin)
def admin_ajouter_pharmacien(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        Pharmacien.objects.create(nom=nom, adresse=adresse, telephone=telephone, email=email, description=description, image=image)
        messages.success(request, "Pharmacien ajouté !")
        return redirect('admin_pharmaciens')
    return render(request, 'pharmacie_app/admin_ajouter_pharmacien.html')

@login_required
@user_passes_test(is_admin)
def admin_modifier_pharmacien(request, pk):
    pharmacien = get_object_or_404(Pharmacien, pk=pk)
    if request.method == 'POST':
        pharmacien.nom = request.POST.get('nom')
        pharmacien.adresse = request.POST.get('adresse')
        pharmacien.telephone = request.POST.get('telephone')
        pharmacien.email = request.POST.get('email')
        pharmacien.description = request.POST.get('description')
        if request.FILES.get('image'):
            pharmacien.image = request.FILES.get('image')
        pharmacien.save()
        messages.success(request, "Pharmacien modifié !")
        return redirect('admin_pharmaciens')
    return render(request, 'pharmacie_app/admin_modifier_pharmacien.html', {'pharmacien': pharmacien})

@login_required
@user_passes_test(is_admin)
def admin_supprimer_pharmacien(request, pk):
    pharmacien = get_object_or_404(Pharmacien, pk=pk)
    if request.method == 'POST':
        pharmacien.delete()
        messages.success(request, "Pharmacien supprimé !")
        return redirect('admin_pharmaciens')
    return render(request, 'pharmacie_app/admin_supprimer_pharmacien.html', {'pharmacien': pharmacien})

# Admin : liste des avis
@login_required
@user_passes_test(is_admin)
def admin_avis(request):
    avis = Avis.objects.all().order_by('-date_ajout')
    return render(request, 'pharmacie_app/admin_avis.html', {'avis': avis})

# Dashboard admin avec statistiques (pour Chart.js)
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta

@login_required
@user_passes_test(is_admin)
def dashboard_admin(request):
    pharmaciens = Pharmacien.objects.all()
    avis = Avis.objects.all()
    total_avis = avis.count()
    note_moyenne_globale = avis.aggregate(moy=Avg('note'))['moy']

    # Graphique barres : nombre de notes par pharmacien
    noms = [p.nom for p in pharmaciens]
    nb_avis = [p.avis_set.count() for p in pharmaciens]

    # Graphique courbe : évolution des notes dans le temps (par jour/semaine)
    # On prend les 30 derniers jours
    dates = []
    moyennes_par_date = []
    for i in range(29, -1, -1):
        jour = timezone.now().date() - timedelta(days=i)
        avis_jour = avis.filter(date_ajout__date=jour)
        if avis_jour.exists():
            moyenne = round(avis_jour.aggregate(moy=Avg('note'))['moy'], 2)
        else:
            moyenne = None
        dates.append(jour.strftime('%d/%m'))
        moyennes_par_date.append(moyenne or 0)

    data = {
        'noms': noms,
        'nb_avis': nb_avis,
        'dates': dates,
        'moyennes_par_date': moyennes_par_date,
    }
    return render(request, 'pharmacie_app/dashboard_admin.html', {
        'data': data,
        'pharmaciens': pharmaciens,
        'total_avis': total_avis,
        'note_moyenne_globale': round(note_moyenne_globale, 2) if note_moyenne_globale else '-',
    })
