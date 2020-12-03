from django import forms


class ItemForm(forms.Form):
    # item_text = forms.CharField(widget=forms.fields.TextInput(attrs={
    #     'placeholder': 'Enter a to-do item',
    # }))
    item_text = forms.CharField()
    item_text.widget.attrs.update({'placeholder': 'Enter a to-do item'})