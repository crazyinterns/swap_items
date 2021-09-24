from django import forms
from items.models import Category


class ItemForm(forms.Form):

    def __init__(self, phonenumber, email, other_contact, *args, **kwargs):

        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['phonenumber'].initial = phonenumber
        self.fields['email'].initial = email
        self.fields['other_contact'].initial = other_contact

    title = forms.CharField(
        label='Название',
        max_length=100,
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea,
        label='Описание',
        required=False
    )
    category = forms.ModelChoiceField(
        required=True,
        label='Выберите категорию',
        queryset=Category.objects.all(),
        to_field_name='title',
        empty_label=''
    )
    phonenumber = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label='Телефон',
        required=False
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label='Почта',
        required=False
    )
    other_contact = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        label='Прочий контакт',
        required=False
    )
    images = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )



