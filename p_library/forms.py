from django import forms  
from p_library.models import Author, Book, Friend, UserProfile
  
class AuthorForm(forms.ModelForm):  

    full_name = forms.CharField(widget=forms.TextInput)

    class Meta:  
        model = Author  
        fields = '__all__'

class FriendForm(forms.ModelForm):  

    full_name = forms.CharField(widget=forms.TextInput)

    class Meta:  
        model = Friend  
        fields = '__all__'


class BookForm(forms.ModelForm):  
    
    class Meta:  
        model = Book  
        fields = ['ISBN', 'title', 'description', 'year_release', 'author', 'publishing', 'copy_count', 'price', 'avatar']

        # widgets = {
        #     # 'label': forms.CharField(attrs={'class': 'form-control'}),
        #     'title': forms.TextInput(attrs={'class': 'form-control'}),
        # }

    # def handler_view(request):
    #     form = BookForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()

# class LeasingForm(forms.ModelForm):  
#     class Meta:  
#         model = Book  
#         fields = 'friends'

class ProfileCreationForm(forms.ModelForm):  
  
    class Meta:  
        model = UserProfile  
        fields = ['age']