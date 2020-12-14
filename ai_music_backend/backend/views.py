from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from .models import Music
from . import process
import random
import json
import uuid
import requests

INSTR_CODE_DICT = {
    "piano": (1 << 0),
    "bass": (1 << 1),
    "guitar": (1 << 2)
}


def is_auth(request):
    return HttpResponse(request.user.is_authenticated)


def register_user(request):
    req = json.loads(request.body)
    username = req['username']
    password = req['password']
    email = ''
    try:
        user = User.objects.create_user(username, email, password)
    except Exception:
        ret = HttpResponse()
        ret.status_code = 500
        return ret
    else:
        login(request, user)
        return HttpResponse()


def login_user(request):
    req = json.loads(request.body)
    username = req['username']
    password = req['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Return 200 if login success
        login(request, user)
        res = HttpResponse()
        # res.set_cookie(username, uuid.uuid4().hex)
        return res
    else:
        # Return 500 if login failed
        ret = HttpResponse()
        ret.status_code = 500
        return ret

def logout_view(request):
    logout(request)
    return HttpResponse()


def download_music(request, music_id):
    with open(f'./backend/music/{music_id}.mp3', 'rb') as f:
        file_data = f.read()
    return HttpResponse(file_data)


def gen_music(request):
    req = json.loads(request.body)
    url = 'http://106.14.227.202:8000/mid2wav/'
    music_id = uuid.uuid4().hex

    # FIXME: Generating random music now
    id = random.randint(0, 8)
    print(f'Lead track: Randomly chosen {id}, music id: {music_id}')
    midi_xuanlv, midi_banzou = f'./backend/lead_tracks/{id}.mid', f'./backend/music/{music_id}.mid'
    process.process(midi_xuanlv, midi_banzou)

    files = {'file': open(midi_banzou, 'rb')}
    r = requests.post(url, files=files)
    if r.status_code != 200:
        raise Exception(f'mid2wav returned {r.status_code}!')

    with open(f'backend/music/{music_id}.mp3', 'wb+') as f:
        f.write(r.content)

    instr = 0
    for i in req['instruments']:
        instr += INSTR_CODE_DICT[i]

    music = Music(music_id=music_id, text=req['text'], emotion=req['emotion'],
                  instruments=instr)
    music.save()

    return JsonResponse({'id': music_id})


def save_music(request):
    js = json.loads(request.body)
    music = Music.objects.get(pk=js['id'])
    music.owner = request.user
    music.name = js['name']
    music.save()
    return HttpResponse()


def share_music(request):
    raise NotImplementedError


def get_all_music(request):
    if request.user.is_authenticated:
        musics = Music.objects.filter(owner__username=request.user.username).order_by(
            '-gen_date').values(
            'music_id', 'name', 'gen_date'
        )
    else:
        musics = Music.objects.filter(name__isnull=False).order_by(
            '-gen_date').values('music_id', 'name', 'gen_date')

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
    instr = []
    for ins in INSTR_CODE_DICT:
        if (music.instruments & INSTR_CODE_DICT[ins]):
            instr.append(ins)

    res = {
        'text': music.text,
        'emotion': music.emotion,
        'instruments': instr,
    }
    return JsonResponse(res, safe=False,
                        json_dumps_params={'ensure_ascii': False})
