from django.urls import path, include

from booksList import views

urlpatterns = [
    path('', views.MyBookListView.as_view(), name='my-books'),
    path('add/',views.AddBookView.as_view(), name='add-book'),
    path('<int:pk>/', include([
        path('edit/', views.EditBookView.as_view(), name='edit-book'),
        path('details/', views.detail_book, name='details-book'),
        path('delete/', views.DeleteBookFromListView.as_view(), name='delete-book'),
    ])),
    path('wish_list/',views.wish_list_view, name='wish-list'),

]