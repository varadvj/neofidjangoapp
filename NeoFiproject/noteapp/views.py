from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Note
from .serializers import UserSerializer, NoteSerializer, NoteVersionSerializer


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        # Get or create the token for the user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    # Setting the owner to the authenticated user
    request.data['owner'] = request.user.id

    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Note created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)
    serializer = NoteSerializer(note)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_note(request, note_id):
    # Ensure that the requesting user is the owner of the note
    note = get_object_or_404(Note, id=note_id, owner=request.user)

    # Get a list of user IDs to share the note with
    user_ids = request.data.get('users', [])

    # owner's ID to the list to ensure they always have access
    user_ids.append(request.user.id)

    # Add the users to the note's shared_users field
    note.shared_users.set(user_ids)

    return Response({'message': 'Note shared successfully'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_note(request, note_id):
    # Ensure that the requesting user has access to the note
    note = get_object_or_404(Note, id=note_id, shared_users=request.user)

    # Extracting new content from the request
    new_content = request.data.get('content', '')

    # Appending new content to the existing note content
    note.content += '\n' + new_content

    # Save the note with the updated content
    note.save()

    return Response({'message': 'Note updated successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note_version_history(request, note_id):
    # Ensure that the requesting user has access to the note
    note = get_object_or_404(Note, id=note_id, shared_users=request.user)

    # Retrieve the version history of the note
    version_history = note.version_history.all()

    # Serialize the version history and return the response
    serializer = NoteVersionSerializer(version_history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
