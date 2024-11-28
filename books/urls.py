from django.urls import path, include

from books import views

urlpatterns = [
    path('my-books/', views.MyBookListView.as_view(), name='my-books'),
    path('add/books/my-list-books/',views.MyBookAddView.as_view(), name='add-book'),
    path('<int:pk>/', include([
        path('edit/', views.edit_book, name='edit_book'),
        path('delete/', views.delete_book, name='delete_book'),
    ])),
    path('monthly_book/<int:pk>/', views.AdminBookDetailsView.as_view(), name='admin-book-details'),
    path('wishlist/', views.WishListView.as_view(), name='wish-list'),
    path('wishlist/<int:pk>/delete/',views.delete_from_wishlist, name='delete-from-wishlist')
]