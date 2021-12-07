from django.urls import path
from .views import indexPageView, searchPPageView, addPageView, editPageView, detailPageView, displayPageView, analyticsPageView, updatePageView, deletePageView, detailDrugPageView, searchPageView, searchDPageView, searchDrugsPageView

urlpatterns = [
    path('search/', searchPageView, name='search'),
    path('searchP/', searchPPageView, name='searchP'),
    path('searchDrugs/', searchDrugsPageView, name='searchDrugs'),
    path('searchD/', searchDPageView, name='searchD'),    
    path('add/', addPageView, name='add'),
    path('edit/<int:editNPI>/', editPageView, name='edit'),
    path("update/", updatePageView, name="update"),
    path("delete/<int:deleteNPI>/", deletePageView, name="delete"),
    path('detail/<int:detailNPI>/', detailPageView, name='detail'),   
    path('detailDrug/<str:detaildrugname>/', detailDrugPageView, name='detailDrug'), 
    path('display/', displayPageView, name='display'),
    path('analytics/', analyticsPageView, name='analytics'),
    path('', indexPageView, name='index'),
]
