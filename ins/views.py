import json
from io import BytesIO

from PIL import Image
from django.contrib import auth
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from ins import models, validators

import time


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not validators.email_validator(email) and not validators.username_validator(email):
            response = {'msg': 'fail', 'info': 'please check your email address or username.'}
        elif not validators.password_validator(password):
            response = {'msg': 'fail', 'info': 'password too short.'}
        else:
            response = {'msg': 'success', 'info': ''}
            user = auth.authenticate(request, username=email, password=password)
            if user is not None:
                auth.login(request, user)
            else:
                response = {'msg': 'fail', 'info': 'password is invalid.'}
                try:
                    models.UserProfile.objects.get(username=email)
                except models.UserProfile.DoesNotExist:
                    try:
                        models.UserProfile.objects.get(email=email)
                    except models.UserProfile.DoesNotExist:
                        response['info'] = 'username or email not exist.'
        return HttpResponse(json.dumps(response))
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not validators.email_validator(email) or not validators.username_validator(username):
            response = {'msg': 'fail', 'info': 'please check your email address or username.'}
        elif not validators.password_validator(password):
            response = {'msg': 'fail', 'info': 'password too short.'}
        else:
            try:
                user = models.UserProfile()
                user.username = username
                user.email = email
                user.set_password(password)
                user.created_at = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                user.save()
                response = {"msg": "success"}
            except IntegrityError as e:
                response = {"msg": "fail", "info": str(e)}
        return HttpResponse(json.dumps(response))
    return render(request, 'register.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


def home(request):
    user = get_user(request)
    if user.is_anonymous:
        return render(request, 'landing.html')
    else:
        return redirect('me')


@login_required
def me(request):
    username = None
    if request.method == "GET":
        username = request.GET.get('username')
    if username is None:
        user = get_user(request)
    else:
        try:
            user = models.UserProfile.objects.get(username=username)
        except models.UserProfile.DoesNotExist:
            user = get_user(request)

    self = 'true' if user == get_user(request) else 'false'
    posts = models.Post.objects.filter(user=user).order_by('-create_at')
    resources = []

    index = 0
    for p in posts:
        try:
            models.Like.objects.get(user=get_user(request), post=p)
            liked = 'dislike'
        except models.Like.DoesNotExist:
            liked = 'like'
        resources.append({
            "id": p.id,
            "index": index,
            "time": p.create_at,
            "like": liked,
            "num": p.likes,
            "description": p.message,
            "img": p.photo.url
        })
        index += 1

    return render(request, 'me.html',
                  {'user': user, 'posts': resources, 'self': self})


def handle_image(image, ft='RGB'):
    name = 'temp.jpg'
    temp = Image.open(image)

    if temp.format != 'JPEG' and temp.format != 'GIF' and temp.format != 'BMP' and temp.format != 'PNG':
        raise ValueError()

    temp = temp.convert(ft)
    temp.save(name)
    temp = Image.open(name)
    height = temp.height
    width = temp.width

    if max(height, width) > 1000:
        if height > width:
            width = 1000 * width // height
            height = 1000
        else:
            height = 1000 * height // width
            width = 1000

    temp = temp.resize((width, height), Image.ANTIALIAS)

    pic_io = BytesIO()
    temp.save(pic_io, 'JPEG')
    return InMemoryUploadedFile(
        file=pic_io,
        field_name=None,
        name=name,
        content_type='image/jpeg',
        size=temp.size,
        charset=None
    )


@login_required
def post(request):
    if request.method == "POST":
        if request.FILES:
            try:
                new_post = models.Post(
                    photo=handle_image(request.FILES.get('file'), request.POST.get('filter')),
                    user=get_user(request),
                    message=request.POST.get("description")
                )

                new_post.save()
                response = {'msg': 'success'}
            except:
                response = {'msg': 'fail', 'info': 'invalid photo.'}
        else:
            response = {'msg': 'fail', 'info': 'no photo.'}

        return HttpResponse(json.dumps(response))


@login_required
def like(request):
    if request.method == "POST":
        user = get_user(request)
        post_id = request.POST.get("id")
        this_post = models.Post.objects.get(id=post_id)
        liked = request.POST.get("like")
        try:
            this_like = models.Like.objects.get(post=this_post, user=user)
            if liked == 'dislike':
                this_like.delete()
                likes = models.Post.objects.get(id=post_id).likes
                res = {'msg': 'success', 'like': 'like', 'likes': likes}
            else:
                res = {'msg': 'fail', 'info': 'already like it.'}
        except models.Like.DoesNotExist:
            if liked == 'like':
                this_like = models.Like()
                this_like.user = user
                this_like.post = this_post
                this_like.save()
                likes = models.Post.objects.get(id=post_id).likes
                res = {'msg': 'success', 'like': 'dislike', 'likes': likes}
            else:
                res = {'msg': 'fail', 'info': 'not like it yet.'}

        return HttpResponse(json.dumps(res))


@login_required
def square(request):
    user = get_user(request)
    posts = models.Post.objects.all().order_by('-create_at')
    resources = []
    for p in posts:
        try:
            models.Like.objects.get(user=user, post=p)
            liked = 'dislike'
        except models.Like.DoesNotExist:
            liked = 'like'
        resources.append({
            "id": p.id,
            "username": p.user.username,
            "time": p.create_at,
            "like": liked,
            "num": p.likes,
            "description": p.message,
            "img": p.photo.url
        })
    return render(request, 'square.html',
                  {'posts': resources})


@login_required
def edit(request):
    user = get_user(request)
    return render(request, 'edit.html', {'user': user})


@login_required
def upload_photo(request):
    if request.method == "POST":
        user = get_user(request)
        user.photo = handle_image(request.FILES.get('file'))
        user.save()
        return HttpResponse(json.dumps({'msg': 'success'}))


@login_required
def change_profile(request):
    if request.is_ajax():
        user = get_user(request)
        user.website = request.POST.get("website")
        user.description = request.POST.get("description")
        user.phone = request.POST.get("phone")
        user.sex = request.POST.get("sex")
        user.save()
        return HttpResponse(json.dumps({'msg': "success"}))


@login_required
def change_password(request):
    if request.is_ajax():
        old_pass = request.POST.get('oldPass')
        new_pass = request.POST.get('newPass')
        user = get_user(request)
        if not validators.password_validator(new_pass):
            res = {'msg': 'fail', 'info': 'invalid input.'}
        elif not user.check_password(old_pass) or user.check_password(new_pass):
            res = {'msg': 'fail', 'info': 'invalid password.'}
        else:
            user.set_password(new_pass)
            user.save()
            res = {'msg': 'success'}
        return HttpResponse(json.dumps(res))


@login_required
def change_email(request):
    if request.is_ajax():
        email = request.POST.get('email')
        if not validators.email_validator(email):
            res = {'msg': 'fail', 'info': 'invalid input.'}
        else:
            try:
                models.UserProfile.objects.get(email=email)
                res = {'msg': 'fail', 'info': 'email already taken.'}
            except models.UserProfile.DoesNotExist:
                user = get_user(request)
                user.email = email
                user.save()
                res = {'msg': 'success'}
        return HttpResponse(json.dumps(res))


@login_required
def change_username(request):
    if request.is_ajax():
        username = request.POST.get('username')
        if not validators.username_validator(username):
            res = {'msg': 'fail', 'info': 'invalid input.'}
        else:
            try:
                models.UserProfile.objects.get(username=username)
                res = {'msg': 'fail', 'info': 'username already taken.'}
            except models.UserProfile.DoesNotExist:
                user = get_user(request)
                user.username = username
                user.save()
                res = {'msg': 'success'}
        return HttpResponse(json.dumps(res))
