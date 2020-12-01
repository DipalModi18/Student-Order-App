from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('about', views.about, name='about'),
    path('<int:topic_id>', views.detail, name='detail'),
    path('findcourses', views.findcourses, name="findcourses"),
    path('place_order', views.place_order, name="place_order"),
    path('review', views.review_view, name="review_view"),
    path('myaccount', views.myaccount, name='myaccount')
    ]
