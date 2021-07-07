from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('is_auth/', views.is_auth, name='is_auth'),
    path('logout/', views.logout_view, name='logout_view'),
    path('generate/', views.gen_music, name='gen_music'),
    path('download/<music_id>/', views.download_music, name='download_music'),
    path('save/', views.save_music, name='save_music'),
    path('share/', views.share_music, name='share_music'),
    path('music/get/', views.get_all_music, name='get_all_music'),
    path('music/get/<user_id>/', views.get_user_music,
         name='get_user_music'),
    path('music/delete/<music_id>/', views.delete_music,
         name='delete_music'),
    path('music/info/<music_id>/', views.get_music_info,
         name='get_music_info'),
    path('music/status/<music_id>/', views.get_status,
         name='get_status'),
    path('music/lyric/<music_id>/', views.get_aligned_lyric,
         name='get_aligned_lyric'),
]
