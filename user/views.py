from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 db안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required



# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':  # 여긴그냥 회원가입페이지로 들어오면 처음 보이는 부분인가?
        user = request.user.is_authenticated
        if user:
            return redirect('/') #'/'는 view의 home함수 실행->home함수는 로그인되어있을때 '/tweet'으로 이동하게 되어있음
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')


        if password != password2:
            #알람 알려주기
            return render(request, 'user/signup.html',{'error':'패스워드를 확인해 주세요'})

        else:
            #만약 빈칸으로 작성할 경우
            if username == '' or password =='':
                return render(request, 'user/signup.html', {'error': 'ID/PWD는 필수입력사항입니다'})

            exist_user = get_user_model().objects.filter(username=username)


            if exist_user:
                # return render(request, 'user/signup.html')
                return render(request, 'user/signup.html',{'error':'이미 사용중인 ID입니다'})

            else:
                # new_user = UserModel()
                # new_user.username = username
                # new_user.password = password
                # new_user.bio = bio
                # new_user.save()
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')


        # 입력받은 값이 데이터베이스에 있는지 확인(왼쪽에 있는 username이 모델에 있는 정보
        me = auth.authenticate(request, username=username, password=password) #입력한 비번과 암호화된 비번 맞는지 확인
        # me = UserModel.objects.get(username=username)
        # if me.password == password:
        if me is not None: #db에 있는지만 확인해 주기
            # request.session['user'] = me.username
            auth.login(request, me)
            return redirect('/') #로그인성공하면 기본url로 넘어감->tweet.urls.py로 가서 home함수 실행
        else:
            return render(request, 'user/signin.html', {'error':'ID 또는 PWD를 확인해 주세요'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

@login_required #사용자가 로그인이 꼭 되어있어야만 접근할 수 있는 함수
def logout(request):
    auth.logout(request)
    return redirect('/')


# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user #현재 로그인한 사람
    click_user = UserModel.objects.get(id=id) #현재로그인한 사람이 팔로우한 사람
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')