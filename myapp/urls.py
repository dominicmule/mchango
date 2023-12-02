from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_mchango/', views.create_mchango, name='create_mchango'),
    #path('<int:mchango_id>/', views.contribute, name='contribute'),
    path('mchango/<str:unique_link>/', views.mchango_detail, name='mchango_detail'),
    path('contribute/<str:unique_link>/', views.contribute, name='contribute'),
    path('search/', views.search_mchango, name='search_mchango'),
    path('search/results/', views.search_results, name='search_results'),
    path('contribute/', views.contribute, name='contribute'),
    path('contribution/success/', views.contribution_success, name='contribution_success'),
    path('token', views.token, name='token'),
    path('stk', views.stk, name="stk"),
]