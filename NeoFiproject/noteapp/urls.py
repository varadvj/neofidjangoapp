from django.urls import path
from .views import signup, login_user, create_note, get_note, share_note, update_note, get_note_version_history

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('notes/create/', create_note, name='create-note'),
    path('notes/<int:note_id>/', get_note, name='get-note'),
    path('notes/share/<int:note_id>/', share_note, name='share-note'),
    path('notes/update/<int:note_id>/', update_note, name='update-note'),
    path('notes/version-history/<int:note_id>/', get_note_version_history, name='get-note-version-history')
]
