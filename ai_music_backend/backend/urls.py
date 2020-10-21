from django.urls import path

from . import views

urlpatterns = [
    path('/generate/', views.gen_music, name='gen_music'),
    path('/save/', views.save_music, name='save_music'),
    path('/share/', views.share_music, name='share_music'),
    path('/music/get/', views.get_all_music, name='get_all_music'),
    path('/music/get/<user_id:str>/', views.get_user_music,
         name='get_user_music'),
    path('/music/delete/<music_id:str>/', views.delete_music,
         name='delete_music'),
    path('/music/info/<music_id:str>/', views.get_music_info,
         name='get_music_info'),
]
