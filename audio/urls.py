from django.urls import path
from . import views


urlpatterns = [
    path('genre/', views.GenreView.as_view()),
    path('license/', views.LicenseView.as_view({'get': 'list', 'post': 'create'})),
    path('license/<int:pk>', views.LicenseView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('stream-track/<int:pk>/', views.StreamingFileView.as_view()),
    path('download_track/<int:pk>/', views.StreamingFileAuthorView.as_view()),

    path('stream-author-track/<int:pk>/', views.StreamingFileAuthorView.as_view()),

    path('track-list/<int:pk>/', views.StreamingFileAuthorView.as_view()),
    path('author-track-list/<int:pk>/', views.AuthorTrackListView.as_view()),

    path('comments/', views.CommentAuthorView.as_view({'get': 'list', 'post': 'create'})),
    path('comments/<int:pk>/', views.CommentAuthorView.as_view({'put': 'update', 'delete': 'destroy'})),
]
