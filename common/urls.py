from django.urls import path, include

from common import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('monthly_book/<int:pk>/', views.AdminBookDetailsView.as_view(), name='admin-book-details'),
    path('comment/<int:book_id>/', views.comment_functionality, name='comment'),
    path('approve-comment/<int:comment_id>/', views.approve_comment, name='approve-comment'),
]