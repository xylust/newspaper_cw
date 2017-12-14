from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Newspaper.serializers import ArticleSerializer, ArticleHeadlineSerializer, RegisterSerializer, CommentSerializer, LikesSerializer
from Newspaper.data import *
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from Newspaper.models import User, Like, Comment
from django.http import JsonResponse
# UNUSED:
# from django.http import HttpResponse
# from rest_framework import status
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt, csrf_protect
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication


def index(request):
    return render(request, 'Newspaper/index.html')

# Web API

@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_articles(request):
    """
    Gets all articles
    """
    if request.method == 'GET':
        query = ExtractCategory(request.query_params)
        articles = None
        if query != None:
            # We got query Parameters
            articles = GetLatestArticlesByCategory(query)
        else:
            # Return the latest Articles
            articles = GetAllArticles()
            serializer = ArticleSerializer(articles, many=True)

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_latest_articles(request):
    """
    Get the latest articles, limited to 10
    """
    if request.method == 'GET':
        query = ExtractCategory(request.query_params)
        articles = None
        if query != None:
            # We got query Parameters
            articles = GetLatestArticlesByCategory(query)
        else:
            # Return the latest Articles
            articles = GetLatestArticles()
            serializer = ArticleHeadlineSerializer(articles, many=True)

        serializer = ArticleHeadlineSerializer(articles, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_article(request, pk):
    """
    Get one article by referencing the primary key
    """
    try:
        if request.method == 'GET':
            article = GetArticleById(pk)
            serializer = ArticleSerializer(article, many=False)
            return Response(serializer.data)
    except:
        return Response(status=400)


# @api_view(['POST'])
# def authentication(request):
#     if request.method == 'POST':
#         email = request.data['email']
#         password = request.data['password']
#         # Authenticate the user
#         user = authenticate(email=email, password=password)

#         # If user is not None
#         if user:
#             # And user is currently active
#             if user.is_active:
#                 print("Authenticated user: ", user)
#                 login(request, user)
#                 return Response(user.email)
#             # User is not active
#             else:
#                 return Response("Account is disabled!")
#         # Wrong details
#         else:
#             print("Invalid login for user: ", user)
#             return Response(status=403)
#     # Login was attempted but not with POST
#     else:
#         print("Attempted authentication with the wrong request method (not POST).")
#         return redirect("/")


@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    data = request.data
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status=500)
    return Response(status=200)


@api_view(['POST'])
def comment(request):
    data = request.data
    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(status=500)
    return Response(status=200)

@api_view(['GET'])
def get_user_info(request):
    if request.method == "GET":
        return JsonResponse({'email': request.user.email, 'name': request.user.name, 'phone': request.user.phone})

@api_view(['POST'])
def modify_user(request):
    if request.method == "POST":
        data = request.data
        serializer = RegisterSerializer(request.user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Modified!")
        else:
            return Response("Error!")
    else:
        print("Attempted authentication with the wrong request method (not POST).")
        return redirect("/")

@api_view(['GET'])
def get_likes(request, id):
    if request.method == "GET":
        try:
            likes = Like.objects.filter(article__id=id, liked=True)
            return Response(likes.count())
        except Like.DoesNotExist:
            return Response(0)
    else:
        print("Attempted authentication with the wrong request method (not GET).")
        return redirect("/")

@api_view(['POST'])
def like(request, id):
    if request.method == "POST":
        try:
            like = Like.objects.get(article__id=id, profile=request.user)
            if like.liked:
                like.delete()
                return Response("Unliked!")
        except Like.DoesNotExist:
            Like.objects.create(profile=request.user, article=get_object_or_404(
                Article, id=id), liked=True)
            return Response("Liked!")
    else:
        print("Attempted authentication with the wrong request method (not POST).")
        return redirect("/")
