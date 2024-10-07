from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_up, name= 'sign_up'),
    path('sign-in', views.sign_in , name='sign_in'),
    path('home-page', views.home_page, name= 'home_page'),
    path('create-account', views.create_account, name ='create_account'),
    path('enter-account', views.enter_account, name='enter_account'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('create-show-page', views.create_show_page, name='create_show_page'),
    path('create-show', views.create_show, name='create_show'),
    path('delete-show/<int:show_id>', views.delete_show, name='delete_show'),
    path('update-show/<int:show_id>', views.update_show, name ='update_show'),
    path('show-details/<int:show_id>', views.show_details, name='show_details' ),
    


    
    
]
