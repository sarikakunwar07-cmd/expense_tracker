from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tracker.models import  Category,Expense





class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = ["category", "title", "amount", "date", "description"]

