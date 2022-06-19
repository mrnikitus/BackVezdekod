import datetime
import json

from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Meme, Like
from .serializers import MemeSerializer

# Запрос всех мемов
class MemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Meme.objects.all().order_by('-created_at')
    serializer_class = MemeSerializer

# Запрос мемов в порядке от самых новых к самым старым
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed(request):
    # Запрашивается первый мем в порядке от самых новых до самых старых, который не оценил текущий пользователь
    obj = Meme.objects.raw(f'SELECT backend_meme.*, backend_like.user_id FROM backend_meme LEFT JOIN backend_like ON backend_meme.id = backend_like.meme_id '
                                   f'WHERE backend_like.user_id IS NULL OR backend_like.user_id <> {request.user.id} ORDER BY backend_meme.created_at DESC LIMIT 1;')
    # Если неоценённый мем есть
    if len(obj) != 0:
        data = {
            "id": obj[0].id,
            "photo": obj[0].photo,
            "author": obj[0].author,
            "likes": obj[0].likes,
            "created_at": obj[0].created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return Response(data)
    else:
        # Запрашивается самая давняя оценка пользователя.
        like = Like.objects.filter(user=request.user).order_by('updated_at').first()
        if like:
            # Запрашивается самый давно лайкнутый мем
            meme = Meme.objects.get(id=like.meme.id)
            queryset = MemeSerializer(meme, many=False)
            queryset.data['id'] = meme.id
            return Response(queryset.data)
        else:
            # Если мемов нет
            return Response({"detail": "Мемов пока еще нет в базе("}, status=204)

# Запрос мемов с приоритетом заранее определенных картинок
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed_new(request):
    # Запрашивается первый мем в порядке от самых новых до самых старых, который не оценил текущий пользователь
    obj = Meme.objects.raw(f'SELECT backend_meme.*, backend_like.user_id FROM backend_meme LEFT JOIN backend_like ON backend_meme.id = backend_like.meme_id '
                           f'WHERE backend_like.user_id IS NULL OR backend_like.user_id <> {request.user.id} ORDER BY backend_meme.important DESC, backend_meme.likes ASC, '
                           f'backend_meme.created_at DESC LIMIT 1;')
    # Если неоценённый мем есть
    if len(obj) != 0:
        data = {
            "id": obj[0].id,
            "photo": obj[0].photo,
            "author": obj[0].author,
            "likes": obj[0].likes,
            "created_at": obj[0].created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return Response(data)
    else:
        # Если всё лайкнуто, запрашиваются мемы в порядке [1] от самых старых лайков, [2] сначала важные
        obj = Meme.objects.raw(f'SELECT backend_meme.*, backend_like.user_id FROM backend_meme LEFT JOIN backend_like ON backend_meme.id = backend_like.meme_id '
                               f'WHERE backend_like.user_id = {request.user.id} ORDER BY backend_like.updated_at ASC, backend_meme.important DESC LIMIT 1;')
        if len(obj) != 0:
            data = {
                "id": obj[0].id,
                "photo": obj[0].photo,
                "author": obj[0].author,
                "likes": obj[0].likes,
                "created_at": obj[0].created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            return Response(data)
        else:
            # Если мемов нет
            return Response({"detail": "Мемов пока еще нет в базе("}, status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    memes = Meme.objects.all().order_by('-likes')[:30]
    queryset = MemeSerializer(memes, many=True)
    return Response({'last_updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'data': queryset.data})


# Оценка мема (POST-запрос - лайк, DELETE-запрос - скип)
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def like(request, id):
    meme = get_object_or_404(Meme, id=id)
    liked = Like.objects.get_or_create(user=request.user, meme=meme)
    liked[0].liked = True if request.method == 'POST' else False
    liked[0].save()
    return Response({'detail': 'Лайк поставлен успешно' if liked[0].liked == True else 'Мем пропущен успешно'})

# Добавление нового пользователя
# @api_view(['POST'])
# def new_user(request):
#     data = json.loads(request.body)
#     user = User(
#         first_name=data['name'],
#         username=data['username'],
#         is_staff=True if data['admin'] == 1 else False,
#         is_admin=True if data['admin'] == 1 else False
#     )
#     user.save()
#     token = Token(user=user)
#     return Response({'token': token[0].token})