from django.urls import path

from .views import main_page, about_page, by_rubrics, detail


urlpatterns = [
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubrics, name='by_rubric'),
    path('<str:page>/', about_page, name='about_us'),
    path('', main_page, name='main'),
]
