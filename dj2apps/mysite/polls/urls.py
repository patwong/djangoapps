from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    # ex: /polls/5/
    # ex: /polls/5/results/
    # ex: /polls/5/vote/
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
