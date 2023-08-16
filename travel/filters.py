from django_filters import FilterSet, RangeFilter,NumberFilter
from .models import Tour


class TourPriceFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr='gt')
    max_price = NumberFilter(field_name="price", lookup_expr='lt')

    class Meta:
        model = Tour
        fields = ['min_price','max_price']