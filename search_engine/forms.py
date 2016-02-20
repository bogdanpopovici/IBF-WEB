from django import forms
from haystack.forms import SearchForm
import datetime

class ItemsSearchForm(SearchForm):

    CATEGORY_CHOICES = (
        ('ACCESSORY', 'Accessory'),
        ('ANIMAL', 'Animal'),
        ('BAG', 'Bag'),
        ('BOOK', 'Book'),
        ('CLOTHES', 'Clothes'),
        ('CONTAINER', 'Container'),
        ('ELECTRONICS', 'Electronics'),
        ('ID/CARDS', 'Id/cards'),
        ('JEWELLERY', 'Jewellery'),
        ('OTHER', 'Other')
    )
    date_item_lost = forms.DateField(required=False)
    location = forms.CharField(required=False)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    def search(self):
        # First, store the SearchQuerySet received from other processing.

        sqs = super(ItemsSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['location']:
                sqs = sqs.filter(location=self.cleaned_data['location'])

        # Check to see if a start_date was chosen.
        if self.cleaned_data['date_item_lost']:
            lost_date = self.cleaned_data['date_item_lost']
            start_date = lost_date - datetime.timedelta(days=7)
            end_date = lost_date + datetime.timedelta(days=7)
            sqs = sqs.filter(date_found__gte=start_date)
            sqs = sqs.filter(date_found__lte=end_date)


        return sqs

class ItemsMatchForm(SearchForm):
    category = forms.CharField(required=False)
    unique_id = forms.CharField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(ItemsMatchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()
        if self.cleaned_data['category']:
                sqs = sqs.filter(category=self.cleaned_data['category'])

        if self.cleaned_data['unique_id']:
                sqs = sqs.filter(unique_id=self.cleaned_data['unique_id'])
        return sqs