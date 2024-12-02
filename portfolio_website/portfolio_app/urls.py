from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('portfolio/<int:pk>', views.PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('tags/', views.TagListView.as_view(), name='tags'),
    path('tag/<int:pk>', views.TagDetailView.as_view(), name='tag-detail'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('service/<int:pk>', views.ServiceDetailView.as_view(), name='service-detail'),
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('clients/archived', views.ArchivedClientListView.as_view(), name='archived-clients'),
    path('clients/active', views.ActiveClientListView.as_view(), name='active-clients'),
    path('client/', views.ClientCreateView.as_view(), name='client'),
    path('client/<str:email>', views.ClientDetailView.as_view(), name='client-detail'),
]