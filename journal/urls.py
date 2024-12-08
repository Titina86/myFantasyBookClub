from django.urls import path, include

from journal import views

urlpatterns = [
    path('create/', views.CreateReadingJournalView.as_view(), name='journal-add'),
    path('',views.BooksWithJournalListView.as_view(), name='reading-journal'),
    path('<int:pk>/', include([
        path('', views.BookJournalDetailView.as_view(), name='journal-book-details'),
        path('edit/', views.EditBookJournalView.as_view(), name='journal-book-edit'),
        path('delete/', views.DeleteBookJournalView.as_view(), name='journal-book-delete'),
    ]))
]