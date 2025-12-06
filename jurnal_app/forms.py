from django import forms
from .models import Comment, Dash , Maqola


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ismingiz'}),
            'body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'komentingiz Sleep well, my love.'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'telefon raqamingiz yoki ijtimoiy tarmoq URL'}),
            'ad_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'reklama narxi'}),
        }
class DashForm(forms.ModelForm):
    class Meta:
        model = Dash
        fields = ('title', 'body' , 'image' , 'contact' , 'ad_price')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'reklama nomi'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'reklama tavsifi'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'telefon raqamingiz yoki ijtimoiy tarmoq URL'}),
            'ad_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'reklama narxi'}),
        }

class MaqolaForm(forms.ModelForm):
    class Meta:
        model = Maqola
        fields = ('title', 'content' , 'image' , 'contact' , 'ad_price' , 'author')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'maqola nomi'}),
            'author': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'muallif'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'maqola tavsifi'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'telefon raqamingiz yoki ijtimoiy tarmoq URL'}),
            'ad_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'reklama narxi'}),
        }


from django import forms
from .models import MaqolaComment

class MaqolaCommentForm(forms.ModelForm):
    class Meta:
        model = MaqolaComment
        fields = ['name', 'body']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingiz'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Komment yozing',
                'rows': 4
            }),
        }

        labels = {
            'name': 'Ism',
            'body': 'Komment',
        }

        help_texts = {
            'body': 'Iltimos, hurmatli komment qoldiring.'
        }
