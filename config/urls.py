from django.urls import path
from compounds import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('compounds/', views.compound_list, name='compound_list'),
    path('compounds/new/', views.compound_create, name='compound_create'),
    path('compounds/<int:pk>/', views.compound_detail, name='compound_detail'),
    path('compounds/<int:pk>/edit/', views.compound_edit, name='compound_edit'),
    path('import/pubchem/', views.pubchem_import, name='pubchem_import'),
]
