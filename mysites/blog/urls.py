from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path('', views.post_list, name= 'home'),
    path('<int:id>', views.post_detail, name= 'post_detail'),
    path('<int:post_id>/share/', views.post_share, name ='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name = 'post_comment'),
    
    

    
]
