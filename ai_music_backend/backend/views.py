from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from .models import Music
from . import process, generate_melody
import random
import threading
import json
import uuid
import requests

INSTR_CODE_DICT = {
    "Piano": (1 << 0),
    "Bass": (1 << 1),
    "Drums": (1 << 2),
    "Strings": (1 << 3),
    "Guitar": (1 << 4),
    "Lead": (1 << 5),
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


def get_aligned_lyric(request, music_id):
    with open(f'./backend/music/{music_id}.txt', 'r') as f:
        file_data = f.read()
    return HttpResponse(file_data)


def gen_thread(req, music_id):
    music = Music.objects.get(pk=music_id)
    midi_xuanlv, midi_banzou = f'./backend/lead_tracks/{music_id}.mid', f'./backend/music/{music_id}.mid'
    lyric_file = f'./backend/music/{music_id}.txt'
    # Turn newline into [sep]
    text = f' {generate_melody.SEP} '.join(req['text'].split('\n')) + f' {generate_melody.SEP}'
    print(text)

    # Turn lyric to melody (SongMASS)
    url = 'http://40.87.50.42:8080/gen_ci'
    r = requests.post(url, data={'ci_head' : text})
    mid = json.loads(r.text)['content']
    generate_melody.to_midi(mid, midi_xuanlv)

    # Calculate alignment for lyrics
    aligns = generate_melody.lyric_align(mid)
    aligned_lyric = []

    for x in zip(aligns, req['text'].split('\n')):
        aligned_lyric.append(x[0] + x[1])

    with open(lyric_file, 'w') as f:
        f.write('\n'.join(aligned_lyric))

    # Turn melody to music (PopMAG)
    music.status = 1
    music.save()

    process.process(midi_xuanlv, midi_banzou)

    # Select instruments
    process.select_track(midi_banzou, req['instruments'])

    # Transform midi to mp3
    music.status = 2
    music.save()

    url = 'http://fandahao.cn/mid2wav/'
    files = {'file': open(midi_banzou, 'rb')}
    r = requests.post(url, files=files)
    if r.status_code != 200:
        raise Exception(f'mid2wav returned {r.status_code}!')

    with open(f'backend/music/{music_id}.mp3', 'wb+') as f:
        f.write(r.content)

    music.status = 3
    music.save()


def gen_music(request):
    req = json.loads(request.body)

    # Get music id
    music_id = uuid.uuid4().hex
    print(music_id)

    instr = 0
    for i in req['instruments']:
        instr += INSTR_CODE_DICT[i]

    music = Music(music_id=music_id, text=req['text'], gen_date=datetime.now().strftime("%Y-%m-%d %H:%M"), emotion=req['emotion'],
                  instruments=instr)
    music.save()

    t = threading.Thread(target=gen_thread, args=(req, music_id), daemon=True)
    t.start()

    return JsonResponse({'id': music_id})


def get_status(request, music_id):
    music = Music.objects.get(pk=music_id)
    return HttpResponse(music.status)


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
