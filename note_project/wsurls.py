from django.urls import path, re_path, include

urlpatterns = [
    path('v1/', include('note_project.wsurlspath.v1_wsurls')),
    # Add other path/re_path entries as needed
]
