from django.urls import path

import mainapp.views as mainapp
from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),

    path('catalog/', mainapp.catalog, name='catalog'),
    path('blog/', mainapp.blog, name='blog'),
    path('article/<int:article_id>/', mainapp.article_detail, name='article_detail'),
    path('like/<int:article_id>/', views.toggle_like, name='toggle_like'),
    path('article/<int:article_id>/like/', views.toggle_article_like, name='toggle_article_like'),
    path('order/', mainapp.order, name='order'),
    path('order/<int:product_id>', mainapp.order, name='order'),
    path('order_bouquet/<int:bouquet_id>/', mainapp.order_bouquet, name='order_bouquet'),
    path('designer/', mainapp.designer, name='designer'),
    path('orders/', mainapp.orders, name='orders'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('cancel_bouquet/<int:bouquet_id>/', views.cancel_bouquet, name='cancel_bouquet'),
    path('save_bouquet/', views.save_bouquet, name='save_bouquet'),

    path('basket', mainapp.basket, name='basket'),
    path('basket/add/<int:pk>/', mainapp.basket_add, name='basket_add'),
    path('basket/remove/<int:pk>/', mainapp.basket_remove, name='basket_remove'),
    path('basket/delete_item/<int:pk>/', mainapp.basket_delete_entire_item, name='basket_delete_entire_item'),

    path('favorites', mainapp.favorites, name='favorites'),
    path('favorites/add/<int:pk>/', mainapp.favorites_add, name='favorites_add'),
    path('favorites/remove/<int:pk>/', mainapp.favorites_remove, name='favorites_remove'),

    path('get_counts/', views.get_counts, name='get_counts'),

    path('search/', mainapp.search_by_category, name='search_results'),
]
