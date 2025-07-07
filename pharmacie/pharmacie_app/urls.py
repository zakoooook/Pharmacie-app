from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.liste_pharmaciens, name='liste_pharmaciens'),
    path('pharmacien/<int:pk>/', views.detail_pharmacien, name='detail_pharmacien'),
    path('pharmacien/<int:pk>/noter/', views.noter_pharmacien, name='noter_pharmacien'),
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('gestion/pharmaciens/', views.admin_pharmaciens, name='admin_pharmaciens'),
    path('gestion/pharmaciens/ajouter/', views.admin_ajouter_pharmacien, name='admin_ajouter_pharmacien'),
    path('gestion/pharmaciens/<int:pk>/modifier/', views.admin_modifier_pharmacien, name='admin_modifier_pharmacien'),
    path('gestion/pharmaciens/<int:pk>/supprimer/', views.admin_supprimer_pharmacien, name='admin_supprimer_pharmacien'),
    path('gestion/avis/', views.admin_avis, name='admin_avis'),
]
path('pharmaciens/<int:pk>/noter-avance/', views.noter_pharmacien_avance, name='noter_pharmacien_avance'),
