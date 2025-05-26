from django.contrib import admin

from mainapp.models import Category, Products, Reviews, Flowers, Pack, Decoration, Message, Answer, Order, Rubric, \
    Article, UserBouquetOrder, Bouquet

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Rubric)
admin.site.register(Article)
admin.site.register(Order)
admin.site.register(Flowers)
admin.site.register(Pack)
admin.site.register(Decoration)
admin.site.register(Message)
admin.site.register(Answer)
admin.site.register(Reviews)
admin.site.register(UserBouquetOrder)
admin.site.register(Bouquet)

