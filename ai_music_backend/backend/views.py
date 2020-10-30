from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from .models import Music


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
    musics = Music.objects.order_by('-gen_date').values(
        'music_id', 'name', 'gen_date'
    )
    return JsonResponse(
        list(musics), safe=False,
        json_dumps_params={'ensure_ascii': False})


def get_user_music(request, user_id):
    musics = Music.objects.filter(owner__username=user_id).order_by(
        '-gen_date').values(
        'music_id', 'name', 'gen_date'
    )
    return JsonResponse(
        list(musics), safe=False,
        json_dumps_params={'ensure_ascii': False})


def delete_music(request, music_id):
    Music.objects.get(pk=music_id).delete()
    return HttpResponse()


def get_music_info(request, music_id):
    music = Music.objects.get(pk=music_id)
    res = {
        'text': music.text,
        'emotion': music.emotion,
        'instruments': music.instruments,
    }
    return JsonResponse(res, safe=False,
                        json_dumps_params={'ensure_ascii': False})
