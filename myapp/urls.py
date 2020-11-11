from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path('about', views.about, name='about'),
    path('<int:topic_id>', views.detail, name='detail'),
    path('findcourses', views.findcourses, name="findcourses")
    ]
