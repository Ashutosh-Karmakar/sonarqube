from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"), #adding the path and to look in which function in views.py
    path('<str:name>/get',views.api_get,name="get"), #<str:name> is the variable input we get from the url itself
    path('<str:name>/put',views.api_put,name="put"),
    path('post',views.api_post,name="post"),
    path('<str:name>/delete',views.api_delete,name="delete"),    
]