from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note

# Create your views here.
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated] #you can not call this list unless you are authenticated

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):  # we evaluate if the data is accurate validating against the other fields
        if serializer.is_valid():
            serializer.save(author=self.request.user) # make a new version of the note, anything we pass will be an aditional fiel we also add the autor because it is readonly in the serializer
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author = user) #is to make sure the user only deletes notes that belongs to them

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all() #list of all objects existing, to make sure we do not duplicate users
    serializer_class = UserSerializer # what kind of data we need to accept for a new user
    permission_classes = [AllowAny] # Who can call this?