import datetime
from haystack import indexes
from core.models import Item


class ItemsSearchForm(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    location = indexes.CharField(model_attr='location')
    date_found = indexes.DateTimeField(model_attr='date_field')

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

