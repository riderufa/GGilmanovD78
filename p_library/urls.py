from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView


# from p_library import views
# from p_library.views import AuthorEdit, AuthorList, FriendList,  author_create_many, books_authors_create_many, friend_detail, FriendEdit, BookEdit, index, login, logout
from p_library.views import *
from allauth.account.views import login, logout


app_name = 'p_library'
urlpatterns = [
    path('', index, name='index'),
    path('index/', index_books, name='index_books'),
    path('login/', login, name='login'),  
    path('logout/', logout, name='logout'),
    path('register/', RegisterView.as_view(template_name='register.html', success_url=reverse_lazy('p_library:profile-create')), name='register'),  
    path('profile-create/', CreateUserProfile.as_view(), name='profile-create'),
    path('leasing/', leasing, name='leasing_books'),
    path('publishing/', index_publishing, name='publishing_books'),
    path('index/book_increment/', book_increment),
    path('index/book_decrement/', book_decrement),
    path('leasing/leasing_book/', leasing_book),
    path('leasing/unleasing_book/', unleasing_book),
    path('author/create', AuthorEdit.as_view(), name='author_create'),  
    path('authors', AuthorList.as_view(), name='author_list'),  
    path('friends', FriendList.as_view(), name='friend_list'),  
    path('friend/create', FriendEdit.as_view(), name='friend_create'),  
    path('book/create', BookEdit.as_view(), name='book_create'),  
    path('friend/<str:f_n>', friend_detail, name='friend_detail_url'),
    path('author/create_many', author_create_many, name='author_create_many'),
    path('author_book/create_many', books_authors_create_many, name='author_book_create_many'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)