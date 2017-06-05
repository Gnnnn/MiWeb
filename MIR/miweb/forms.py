# coding:utf-8
from django import forms


class NameForm(forms.Form):
    your_email = forms.CharField(widget=forms.EmailInput)
    your_password = forms.CharField(widget=forms.PasswordInput)


class SearchForm(forms.Form):
    your_search = forms.CharField(max_length=200, min_length=1)


class InfoForm(forms.Form):
    your_name = forms.CharField(max_length=100)
    your_phone = forms.CharField(max_length=100)
    your_email = forms.CharField(widget=forms.EmailInput)
    your_info = forms.CharField(widget=forms.Textarea)
    your_place = forms.CharField(max_length=100)


class SignupForm(forms.Form):
    your_email = forms.CharField(widget=forms.EmailInput)
    your_name = forms.CharField(max_length=100)
    your_password = forms.CharField(widget=forms.PasswordInput)
    your_invitecode = forms.CharField(max_length=50)


class UploadForm(forms.Form):
    pic_name = forms.CharField(max_length=50)
    pic_way = forms.FileField()
    pic_code = forms.CharField(max_length=45)
    pic_author = forms.CharField(max_length=100)
    pic_job = forms.CharField(max_length=200)
    pic_tool = forms.CharField(max_length=200)
    pic_abstract = forms.CharField(max_length=1000)
    pic_content = forms.CharField(widget=forms.Textarea, max_length=2000)


class SafeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_two_password = forms.CharField(widget=forms.PasswordInput)


class CommentForm(forms.Form):
    com_content = forms.CharField(widget=forms.Textarea, max_length=2000)


class ChangeForm(forms.Form):
    pic_name = forms.CharField(max_length=50)
    pic_job = forms.CharField(max_length=200)
    pic_abstract = forms.CharField(max_length=1000)
    pic_content = forms.CharField(widget=forms.Textarea, max_length=2000)


class ReviewForm(forms.Form):
    review_idea = forms.CharField(widget=forms.Textarea, max_length=2000)
