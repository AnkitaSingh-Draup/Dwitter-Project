from django.shortcuts import render
from .models import Dweets,Followers,Comments
from .serializer import DweetsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from  rest_framework import status
from django.contrib.auth.models import User

# Create your views here.
@api_view(['GET', 'POST'])
def dweets(request):
    if request.method == 'POST':
        data = request.data
        serializer = DweetsSerializer(data={"user":request.user.pk, "dweet":data["dweet"]})
        if serializer.is_valid():
            serializer.save()
    #dweet = Dweets.objects.create(user=request.user, dweet=data["dweet"])
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #dweet = Dweets.objects.all().values("dweet","user")
    elif request.method == 'GET':
        dweet = Dweets.objects.all()
        serializer = DweetsSerializer(dweet,many=True)
        return Response(serializer.data)

@api_view(['PUT', 'DELETE','GET'])
def dweets_edit( request, pk):
    if request.method == 'DELETE':
        try:
            dweet = Dweets.objects.get(pk=pk)
            if request.user != dweet.user:
                return Response("Can't delete someone else's dweet", status=status.HTTP_401_UNAUTHORIZED)
            dweet.delete()
        except Exception:
            return Response("could not delete")
        return Response("dweet deleted")

    elif request.method == 'GET':
        dweet = Dweets.objects.get(pk=pk)
        follow = Followers.objects.filter(following=dweet.user)
        if request.user == dweet.user:
            serializer = DweetsSerializer(dweet)
            return Response(serializer.data)
        else:
            check = False
            for i in follow:
                if request.user == i.followed_by:
                    check = True
            if (not check ):
                return Response("Follow user to see dweet",status=status.HTTP_401_UNAUTHORIZED)
            serializer = DweetsSerializer(dweet)
            return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        dweet = Dweets.objects.get(pk=pk)
        if request.user != dweet.user:
            return Response("You don't have permission to edit", status=status.HTTP_401_UNAUTHORIZED)
        serializer = DweetsSerializer(dweet, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_follow(request):
    data=request.data["user"]
    user=User.objects.filter(username__icontains=data).first()
    if user:
        Followers.objects.create(following=user,followed_by=request.user)
        return Response("You have followed %s"%user.username)
    else:
        return Response("User does not exists")


@api_view(['PUT'])
def like(request,pk):
    dweet = Dweets.objects.get(pk=pk)
    follow=Followers.objects.filter(following=dweet.user)
    check = False
    for i in follow:
        if request.user == i.followed_by:
            check = True
    if(check==True):
        dweet.like.add(request.user)
        dweet.save()
        return Response("Liked the dweet")
    else:
        return Response("Follow the user to like dweet")


@api_view(["POST"])
def comment(request,pk):
    comment=request.data["comment"]
    dweet=Dweets.objects.get(pk=pk)
    follow=Followers.objects.filter(following=dweet.user)
    flag=False
    for i in follow:
        if i.followed_by == request.user:
            flag=True
    if(flag):
        Comments.objects.create(comment=comment, commented_by=request.user, dweet=dweet)
        return Response("Comment Successful")
    else:
        return Response("Follow user to comment")


@api_view(['GET'])
def search_dweet(request):
    dweet = request.data["dweet"]
    dweet1 = Dweets.objects.filter(dweet__icontains=dweet)
    serializer=DweetsSerializer(dweet1,many=True)
    if(dweet1):
        return  Response(serializer.data,status=status.HTTP_302_FOUND)
    else:
        return Response("Dweet not found",status=status.HTTP_404_NOT_FOUND)