from django.urls import path, include

from journal import views

urlpatterns = [

    path('', views.ReadingJournalListView.as_view(), name='reading-journal-list'),
    path('create/', views.ReadingJournalCreateView.as_view(), name='journal-create'),
    path('<int:pk>/', include([
        path('', views.ReadingJournalDetailView.as_view(), name='journal-book-details'),
        # path('edit/', views.ProfileEditView.as_view(), name='profile-edit'),
        # path('delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),
    ]))
]