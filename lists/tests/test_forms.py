from django.test import TestCase

from lists.forms import ItemForm


class ItemFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_selector(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
