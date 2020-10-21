from django.shortcuts import render


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
