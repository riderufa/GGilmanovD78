from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.template import loader
from django.views.generic import CreateView, ListView, FormView
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from django.contrib.auth import login, authenticate
from allauth.socialaccount.models import SocialAccount
from p_library.models import Author, Book, Publishing, Friend, UserProfile
from p_library.forms import AuthorForm, BookForm, FriendForm, ProfileCreationForm

# Create your views here.

class AuthorEdit(CreateView):  
    model = Author  
    form_class = AuthorForm  
    success_url = reverse_lazy('author_list')  
    template_name = 'author_edit.html'  
  
class FriendEdit(CreateView):  
    model = Friend  
    form_class = FriendForm  
    success_url = reverse_lazy('friend_list')  
    template_name = 'friend_edit.html'  

class BookEdit(CreateView):  
    model = Book  
    form_class = BookForm  
    success_url = reverse_lazy('index_books')  
    template_name = 'book_edit.html'  


class AuthorList(ListView):  
    model = Author  
    template_name = 'author_list.html'

class FriendList(ListView):  
    model = Friend  
    template_name = 'friend_list.html'


def author_list(request):
    authors = Author.objects.all()
    return HttpResponse(authors)


def friend_detail(request, f_n):
    friend = Friend.objects.get(full_name=f_n)
    return render(request, 'friend_detail.html', context={'friend': friend})

def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

def index_books(request):
    template = loader.get_template('index.html')
    books = Book.objects.all()
    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
    }
    return HttpResponse(template.render(biblio_data, request))

def index(request):  
    context = {}  
    if request.user.is_authenticated:  
        books = Book.objects.all()
        context['title'] = "dfgsdfgsdfg"
        context['books'] = books
        context['username'] = request.user.username  
        context['github_url'] = SocialAccount.objects.get(provider='github', user=request.user).extra_data['html_url']
    return render(request, 'index.html', context)  

# def login(request):  
#     if request.method == 'POST':  
#         form = AuthenticationForm(request=request, data=request.POST)  
#         if form.is_valid():  
#             auth.login(request, form.get_user())  
#             return HttpResponseRedirect(reverse_lazy('p_library:index'))  
#     else:  
#         context = {'form': AuthenticationForm()}  
#         return render(request, 'login.html', context)  
  
  
# def logout(request):  
#     auth.logout(request)  
#     return HttpResponseRedirect(reverse_lazy('p_library:logout'))

class RegisterView(FormView):  
  
    form_class = UserCreationForm  
  
    def form_valid(self, form):  
        form.save()  
        username = form.cleaned_data.get('username')  
        raw_password = form.cleaned_data.get('password1')  
        login(self.request, authenticate(username=username, password=raw_password))  
        return super(RegisterView, self).form_valid(form)  
  
  
class CreateUserProfile(FormView):  
  
    form_class = ProfileCreationForm  
    template_name = 'profile-create.html'  
    success_url = reverse_lazy('p_library:index')  
  
    def dispatch(self, request, *args, **kwargs):  
        if self.request.user.is_anonymous:  
            return HttpResponseRedirect(reverse_lazy('p_library:login'))  
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)  
  
    def form_valid(self, form):  
        instance = form.save(commit=False)  
        instance.user = self.request.user  
        instance.save()  
        return super(CreateUserProfile, self).form_valid(form)

def leasing(request):
    template = loader.get_template('leasing.html')
    books = Book.objects.all()
    friends = Friend.objects.all()
    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
        "friends": friends,
    }
    return HttpResponse(template.render(biblio_data, request))


def index_publishing(request):
    template = loader.get_template('publishing.html')
    books = Book.objects.all()
    publishings = Publishing.objects.all()
    biblio_data = {
        "title": "мою библиотеку", 
        "books": books,
        "publishings": publishings,
    }
    return HttpResponse(template.render(biblio_data, request))

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

def leasing_book(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        friend_id = request.POST['select']
        if not book_id:
            return redirect('/leasing/')
        else:
            book = Book.objects.filter(id=book_id).first()
            friend = Friend.objects.get(id=friend_id)
            if not book:
                return redirect('/leasing/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
                book.leasing_count += 1
                book.friends.add(friend)
            book.save()
        return redirect('/leasing/')
    else:
        return redirect('/leasing/')

def unleasing_book(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        friend_id = request.POST['select_unleasing']
        if not book_id:
            return redirect('/leasing/')
        else:
            book = Book.objects.filter(id=book_id).first()
            friend = Friend.objects.get(id=friend_id)
            if not book:
                return redirect('/leasing/')
            if book.leasing_count < 1:
                book.leasing_count = 0
            else:
                book.copy_count += 1
                book.leasing_count -= 1
                book.friends.remove(friend)
            book.save()
        return redirect('/leasing/')
    else:
        return redirect('/leasing/')


def author_create(request):  
    AuthorFormSet = formset_factory(AuthorForm, extra=2)  #  Первым делом, получим класс, который будет создавать наши формы. Обратите внимание на параметр `extra`, в данном случае он равен двум, это значит, что на странице с несколькими формами изначально будет появляться 2 формы создания авторов.
    if request.method == 'POST':  #  Наш обработчик будет обрабатывать и GET и POST запросы. POST запрос будет содержать в себе уже заполненные данные формы
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')  #  Здесь мы заполняем формы формсета теми данными, которые пришли в запросе. Обратите внимание на параметр `prefix`. Мы можем иметь на странице не только несколько форм, но и разных формсетов, этот параметр позволяет их отличать в запросе.
        if author_formset.is_valid():  #  Проверяем, валидны ли данные формы
            for author_form in author_formset:  
                author_form.save()  #  Сохраним каждую форму в формсете
            return HttpResponseRedirect(reverse_lazy('author_list'))  #  После чего, переадресуем браузер на список всех авторов.
    else:  #  Если обработчик получил GET запрос, значит в ответ нужно просто "нарисовать" формы.
        author_formset = AuthorFormSet(prefix='authors')  #  Инициализируем формсет и ниже передаём его в контекст шаблона.
    return render(request, 'manage_authors.html', {'author_formset': author_formset})


def author_create_many(request):  
    AuthorFormSet = formset_factory(AuthorForm, extra=2)  #  Первым делом, получим класс, который будет создавать наши формы. Обратите внимание на параметр `extra`, в данном случае он равен двум, это значит, что на странице с несколькими формами изначально будет появляться 2 формы создания авторов.
    if request.method == 'POST':  #  Наш обработчик будет обрабатывать и GET и POST запросы. POST запрос будет содержать в себе уже заполненные данные формы
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')  #  Здесь мы заполняем формы формсета теми данными, которые пришли в запросе. Обратите внимание на параметр `prefix`. Мы можем иметь на странице не только несколько форм, но и разных формсетов, этот параметр позволяет их отличать в запросе.
        if author_formset.is_valid():  #  Проверяем, валидны ли данные формы
            for author_form in author_formset:  
                author_form.save()  #  Сохраним каждую форму в формсете
            return HttpResponseRedirect(reverse_lazy('author_list'))  #  После чего, переадресуем браузер на список всех авторов.
    else:  #  Если обработчик получил GET запрос, значит в ответ нужно просто "нарисовать" формы.
        author_formset = AuthorFormSet(prefix='authors')  #  Инициализируем формсет и ниже передаём его в контекст шаблона.
    return render(request, 'manage_authors.html', {'author_formset': author_formset})

def books_authors_create_many(request):  
    AuthorFormSet = formset_factory(AuthorForm, extra=2)  
    BookFormSet = formset_factory(BookForm, extra=2)  
    if request.method == 'POST':  
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')  
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')  
        if author_formset.is_valid() and book_formset.is_valid():  
            for author_form in author_formset:  
                author_form.save()  
            for book_form in book_formset:  
                book_form.save()  
            return HttpResponseRedirect(reverse_lazy('author_list'))  
    else:  
        author_formset = AuthorFormSet(prefix='authors')  
        book_formset = BookFormSet(prefix='books')  
    return render(
	    request,  
		'manage_books_authors.html',  
		{  
	        'author_formset': author_formset,  
			'book_formset': book_formset,  
		}  
	)


