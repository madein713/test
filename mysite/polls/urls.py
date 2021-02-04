from django.urls import path

from . import views
urlpatterns = [
    path('iin/', views.SnippetList.as_view()),
    path('iin/<str:iin>/', views.SnippetList.as_view()),
]
