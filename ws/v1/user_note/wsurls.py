from django.urls import path
from ws.v1.user_note import views

urlpatterns = [
    path('create-note/', views.CreateNote.as_view()),
    path('<int:note_id>/', views.GetNote.as_view()),
    path('share/', views.ShareNote.as_view()),
    path('update/<int:note_id>/', views.UpdateNote.as_view()),
    path('version-history/<int:note_id>/', views.GetNoteVersionHistory.as_view()),
]