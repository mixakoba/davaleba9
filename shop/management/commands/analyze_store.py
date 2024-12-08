from django.core.management.base import BaseCommand
from shop.models import Item,Category,Tag
from django.db.models import (
    Sum,
    Avg,
    Min,
    Max,
    Count
)

class Command(BaseCommand):
    def handle(self,*args,**kwargs):

        categories_count=Item.objects.aggregate(categories_count=Count('category'))
        print(categories_count)

        min_max_avg=Item.objects.aggregate(max_price=Max('price'),min_price=Min('price'),avg_price=Avg('price'))
        print(min_max_avg)

        categories=Category.objects.annotate(items_count=Count('items'))
        for category in categories:
            print(f"{category.name} : {category.items_count}")

        categories=Category.objects.annotate(items_price=Sum('items__price',default=0))
        for category in categories:
            print(f"{category.name} : {category.items_price}")

        items=Item.objects.select_related('category').all()

        for item in items:
            print(f"{item.name} : {item.category.name}")

        items=Item.objects.prefetch_related('tags').all()

        for item in items:
            print(item.name,[tag.name for tag in item.tags.all()])