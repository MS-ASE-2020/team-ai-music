from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Return 200 if login success
        login(request, user)
        return HttpResponse()
    else:
        # Return 403 if login failed
        return HttpResponse(status_code=403)


def logout_view(request):
    logout(request)
    return HttpResponse()


def gen_music(request):
    raise NotImplementedError


def save_music(request):
    raise NotImplementedError


def share_music(request):
    raise NotImplementedError


def get_all_music(request):
    raise NotImplementedError


def get_user_music(request, user_id):
    raise NotImplementedError


def delete_music(request, music_id):
    raise NotImplementedError


def get_music_info(request, music_id):
    raise NotImplementedError
