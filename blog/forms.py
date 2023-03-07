from django import forms
from .models import Comment, Category
from mptt.forms import TreeNodeChoiceField


# grabbing the data from table
# django has the facility. we just tell it what model or field we want to use and it will automatically make a form for us.
class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('name', 'parent', 'email', 'content')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'email': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }# add some styling to our form
        # using pre-formatted: to create the forms automatically using 'djang forms' that we imported our model, so that we can capture the data from our model.

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)


# to search from the user's post
class PostSearchForm(forms.Form):
    q = forms.CharField()
    c = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['c'].label = ''
        self.fields['c'].required = False
        self.fields['c'].label = 'Category'
        self.fields['q'].label = 'Search For'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control menudd'})
        self.fields['q'].widget.attrs.update(
            {'data-toggle': 'dropdown'})
