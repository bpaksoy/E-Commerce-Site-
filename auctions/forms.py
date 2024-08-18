from django import forms
from django.forms import ModelForm
from .models import Listing, Category, Comment, Bid


class NewListingForm(ModelForm):
    image = forms.ImageField(label='image')

    title = forms.CharField(label="title", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'style': 'width:200px'}))

    category = forms.ModelChoiceField(
        label="category", queryset=Category.objects.all())

    content = forms.CharField(label="content", widget=forms.Textarea(
        attrs={'class': 'form-control text-justify', 'style': ' width: 600px; vertical-align: top'}))

    starting_price = forms.FloatField(
        label='starting price', min_value=0.0)

    class Meta:
        model = Listing
        fields = ['image', 'title', 'category', 'content', 'starting_price']


class NewCommentForm(ModelForm):
    body = forms.CharField(label="body", widget=forms.Textarea(
        attrs={'class': 'form-control text-justify', 'style': ' width: 400px; vertical-align: top'}))

    class Meta:
        model = Comment
        exclude = ('listing', 'user')


class NewBidForm(ModelForm):
    bid = forms.FloatField(label='bid')

    class Meta:
        model = Bid
        exclude = ('listing', 'user', 'win')
