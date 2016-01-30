from django import forms
from haystack.forms import SearchForm
import datetime

class ItemsSearchForm(SearchForm):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    location = forms.CharField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.

        sqs = super(ItemsSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['location']:
                sqs = sqs.filter(location=self.cleaned_data['location'])

        # Check to see if a start_date was chosen.
        if self.cleaned_data['start_date']:
            sqs = sqs.filter(date_found__gte=self.cleaned_data['start_date'])

        # Check to see if an end_date was chosen.
        if self.cleaned_data['end_date']:
            sqs = sqs.filter(date_found__lte=self.cleaned_data['end_date'])

        return sqs

class ItemsMatchForm(SearchForm):
    start_date = forms.DateField(required=False)
    category = forms.CharField(required=False)
    unique_id = forms.CharField(required=False)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(ItemsMatchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()
        if self.cleaned_data['category']:
                sqs = sqs.filter(category=self.cleaned_data['category'])

        # Check to see if a start_date was chosen.
        #if self.cleaned_data['start_date']:
        #    sqs = sqs.filter(date_found__lte=self.cleaned_data['start_date'])

        if self.cleaned_data['unique_id']:
                sqs = sqs.filter(unique_id=self.cleaned_data['unique_id'])
        return sqs