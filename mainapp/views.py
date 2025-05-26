from django.urls import reverse

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.db.models import Sum, F, FloatField
from django.db import transaction
import json
from datetime import date
from .forms import ReviewsForm, OrderForm, BouquetForm, MessageForm, UserBouquetOrderForm
from .models import Products, Basket, Reviews, Order, Category, Favorites, Flowers, Pack, Decoration, Bouquet, Message, \
    UserBouquetOrder, Answer, Article, Rubric, ArticleLike


def index(request):
    products = Products.objects.order_by('-id')[:4]
    basket_count = 0
    favorites_count = 0

    if request.user.is_authenticated:
        basket_count = Basket.objects.filter(user=request.user).aggregate(Sum('counts'))['counts__sum'] or 0
        favorites_count = Favorites.objects.filter(user=request.user).count()

    review_count = Reviews.objects.filter(is_active='published').count()

    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                request.session['success_message'] = 'Отзыв отправлен на модерацию.'
                return redirect('mainapp:index')
            else:
                return redirect('auth:login')
    else:
        form = ReviewsForm()

    message_form = MessageForm()
    if request.method == 'POST' and 'send_message' in request.POST:
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.save()
            request.session['success_message'] = 'Сообщение успешно отправлено.'
            return redirect('mainapp:index')

    selected_user_id = request.session.get('selected_user_id')

    if request.user.is_authenticated:
        messages_qs = Message.objects.filter(user=request.user).order_by('created_at')
    else:
        messages_qs = Message.objects.none()

    if request.method == 'POST':
        if 'add_to_basket' in request.POST:
            pass
        elif 'add_to_favorites' in request.POST:
            pass
        elif 'send_message' in request.POST:
            pass
        elif 'submit_review' in request.POST:
            pass

    messages_list = list(messages_qs)

    answers_qs = Answer.objects.filter(message__in=messages_list)
    answers_map = {}
    for ans in answers_qs:
        answers_map.setdefault(ans.message_id, []).append(ans)

    answers_for_messages = [
        answers_map.get(msg.id, [])
        for msg in messages_list
    ]

    messages_with_answers = list(zip(messages_list, answers_for_messages))

    context = {
        'title': 'Главная',
        'products': products,
        'form': form,
        'message_form': message_form,
        'reviews': Reviews.objects.filter(is_active='published').order_by('-created_at')[:3],
        'messages': messages_list,
        'answers_for_messages': answers_for_messages,
        'review_count': review_count,
        'basket_count': basket_count,
        'favorites_count': favorites_count,
        'success_message': request.session.pop('success_message', None),
        'selected_user_id': int(selected_user_id) if selected_user_id else None,
        'messages_with_answers': messages_with_answers,
    }

    return render(request, 'mainapp/index.html', context)


@login_required
def order(request, product_id=None):
    print("Обработчик вызван")
    print("Request method:", request.method)
    product = None
    show_modal = False

    if product_id:
        basket_items = Basket.objects.filter(user=request.user, product_id=product_id)
        product = Products.objects.get(id=product_id)
        product_price_value = product.price
    else:
        basket_items = Basket.objects.filter(user=request.user)
        product_price_value = None

    total_sum = sum(item.product.price * item.counts for item in basket_items)

    bouquets_data = []

    if basket_items.exists():
        for item in basket_items:
            bouquets_data.append({
                'name': item.product.name,
                'quantity': item.counts,
            })

    if product:
        bouquets_data.append({
            'name': product.name,
            'quantity': 1,
        })

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = Order.objects.create(
                    user=request.user,
                    sender_name=form.cleaned_data['sender_name'],
                    recipient_name=form.cleaned_data['recipient_name'],
                    phone_number=form.cleaned_data['phone_number'],
                    recipient_phone=form.cleaned_data['recipient_phone'],
                    delivery_type=form.cleaned_data['delivery_type'],
                    address=form.cleaned_data['address'],
                    date=form.cleaned_data['date'],
                    time=form.cleaned_data['time'],
                    comment=form.cleaned_data['comment'],
                    pay_type=form.cleaned_data['pay_type'],
                    card_number=form.cleaned_data['card_number'],
                    CVV=form.cleaned_data['CVV'],
                    total_price=total_sum,
                    product_price=product_price_value,
                    bouquets=bouquets_data,
                )
                print("Заказ успешно сохранен с ID:", order.id)
                basket_items.delete()

                return redirect(reverse('mainapp:orders') + '?success=1')

            except Exception as e:
                print("Ошибка при сохранении заказа:", e)
        else:
            print('Форма не прошла валидацию:', form.errors)

    form = form if request.method == 'POST' else OrderForm()

    context = {
        'basket': basket_items,
        'title': 'Оформление заказа',
        'total_sum': total_sum,
        'form': form,
        'product': product,
        'product_price': product.price if product else None,
        'show_modal': False,
    }
    return render(request, 'mainapp/order.html', context)


@login_required
def order_bouquet(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)
    total_price = getattr(bouquet, 'total_price', 0)

    if request.method == 'POST':
        form = UserBouquetOrderForm(request.POST)
        if form.is_valid():
            flowers_data = form.cleaned_data.get('flowers', '')
            try:
                flowers_list = json.loads(flowers_data) if flowers_data else []
            except json.JSONDecodeError:
                flowers_list = []

            UserBouquetOrder.objects.create(
                user=request.user,
                bouquet=bouquet,
                name_pack=form.cleaned_data['name_pack'],
                name_decoration=form.cleaned_data['name_decoration'],
                flowers=flowers_list,
                sender_name=form.cleaned_data['sender_name'],
                phone_number=form.cleaned_data['phone_number'],
                recipient_name=form.cleaned_data['recipient_name'],
                recipient_phone=form.cleaned_data['recipient_phone'],
                delivery_type=form.cleaned_data['delivery_type'],
                address=form.cleaned_data['address'],
                date=form.cleaned_data['date'] or date.today(),
                time=form.cleaned_data['time'],
                comment=form.cleaned_data['comment'],
                pay_type=form.cleaned_data['pay_type'],
                card_number=form.cleaned_data['card_number'],
                CVV=form.cleaned_data['CVV'],
            )

            Order.objects.create(
                user=request.user,
                total_price=total_price,
                sender_name=form.cleaned_data['sender_name'],
                recipient_name=form.cleaned_data['recipient_name'],
                phone_number=form.cleaned_data['phone_number'],
                recipient_phone=form.cleaned_data['recipient_phone'],
                delivery_type=form.cleaned_data['delivery_type'],
                address=form.cleaned_data['address'],
                date=form.cleaned_data['date'] or date.today(),
                time=form.cleaned_data['time'],
                comment=form.cleaned_data['comment'],
                pay_type=form.cleaned_data['pay_type'],
                card_number=form.cleaned_data['card_number'],
                CVV=form.cleaned_data['CVV'],
            )
            return redirect(reverse('mainapp:orders') + '?success=1')
        else:
            print('Ошибки формы:', form.errors)
    else:
        initial_data = {
            'name_pack': '',
            'name_decoration': '',
            'date': date.today(),
            'time': '--:--',
        }
        form = UserBouquetOrderForm(initial=initial_data)

    context = {
        'form': form,
        'bouquet': bouquet,
        'title': 'Оформление заказа',
    }
    return render(request, 'mainapp/order_bouquet.html', context)


@login_required
def search_by_category(request):
    query = request.GET.get('q')
    products = Products.objects.none()

    if query:
        products = Products.objects.filter(
            Q(name__icontains=query) | Q(name__icontains=query)
        )

    context = {
        'title': 'Результаты поиска',
        'products': products,
        'query': query,
    }
    return render(request, 'mainapp/search_results.html', context)


@login_required
def catalog(request):
    products = Products.objects.all()
    basket_count = Basket.objects.filter(user=request.user).aggregate(Sum('counts'))['counts__sum'] or 0
    favorites_count = Favorites.objects.filter(user=request.user).count()

    category_ids = request.GET.getlist('category')
    if category_ids:
        products = products.filter(category_id__in=category_ids)

    try:
        min_price = int(request.GET.get('min_price', 2000))
    except ValueError:
        min_price = 2000

    try:
        max_price = int(request.GET.get('max_price', 10000))
    except ValueError:
        max_price = 10000

    products = products.filter(price__gte=min_price, price__lte=max_price)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    category = Category.objects.all()

    favorites_ids = Favorites.objects.filter(user=request.user).values_list('product_id', flat=True)
    basket_ids = Basket.objects.filter(user=request.user).values_list('product_id', flat=True)

    context = {
        'title': 'Каталог',
        'products': page_obj,
        'category': category,
        'page_obj': page_obj,
        'min_price': min_price,
        'max_price': max_price,
        'basket_count': basket_count,
        'favorites_count': favorites_count,
        'favorites_ids': list(favorites_ids),
        'basket_ids': list(basket_ids),
    }
    return render(request, 'mainapp/catalog.html', context)


@login_required
def blog(request):
    selected_rubric = request.GET.get('rubric')
    sort_order = request.GET.get('sort', 'desc')
    filter_liked = request.GET.get('liked_only')

    if selected_rubric and selected_rubric.isdigit():
        articles_qs = Article.objects.filter(rubric__id=int(selected_rubric))
    else:
        articles_qs = Article.objects.all()

    if filter_liked == '1':
        articles_qs = articles_qs.filter(likes__user=request.user, likes__liked=True).distinct()

    if sort_order == 'asc':
        articles_qs = articles_qs.order_by('created_at')
    else:
        articles_qs = articles_qs.order_by('-created_at')

    liked_article_ids = set(
        ArticleLike.objects.filter(user=request.user, liked=True).values_list('article_id', flat=True)
    )

    rubrics = Rubric.objects.all()

    paginator = Paginator(articles_qs, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Блог',
        'articles': page_obj,
        'rubrics': rubrics,
        'selected_rank': selected_rubric,
        'selected_sort': sort_order,
        'page_obj': page_obj,
        'liked_article_ids': liked_article_ids,
        'filter_liked': filter_liked,
    }
    return render(request, 'mainapp/blog.html', context)


@login_required
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    like_exists = ArticleLike.objects.filter(user=request.user, article=article).exists()
    context = {
        'title': 'Статья',
        'article': article,
        'like_exists': like_exists,
    }
    return render(request, 'mainapp/article_detail.html', context)


@login_required
def toggle_article_like(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    try:
        like_obj = ArticleLike.objects.get(user=request.user, article=article)
        like_obj.delete()
    except ArticleLike.DoesNotExist:
        ArticleLike.objects.create(user=request.user, article=article, liked=True)
    return redirect('mainapp:article_detail', article_id=article.id)


@login_required
def toggle_like(request, article_id):
    if request.method == 'POST':
        user = request.user
        article = get_object_or_404(Article, id=article_id)

        like_obj, created = ArticleLike.objects.get_or_create(user=user, article=article)
        if not created:
            like_obj.delete()

        return redirect('mainapp:blog')
    else:
        return redirect('mainapp:blog')


def articles_list(request):
    articles = Article.objects.all()

    liked_articles_ids = []
    if request.user.is_authenticated:
        liked_articles_ids = list(
            ArticleLike.objects.filter(user=request.user, article__in=articles).values_list('article_id', flat=True)
        )

    context = {
        'articles': articles,
        'liked_articles_ids': liked_articles_ids,
    }
    return render(request, 'ваш_шаблон.html', context)


@login_required
def designer(request):
    if request.method == 'POST':
        form = BouquetForm(request.POST)
        if form.is_valid():
            bouquet = form.save(commit=False)
            bouquet.save()
            form.save_m2m()
            selected_flowers = form.cleaned_data['flowers']
            selected_pack = form.cleaned_data['pack']
            selected_decorations = form.cleaned_data['decorations']
            total_price = sum(f.price for f in selected_flowers) + selected_pack.price + sum(
                d.price for d in selected_decorations)
    else:
        form = BouquetForm()

    context = {
        'title': 'Конструктор букетов',
        'form': form,
        'all_flowers': Flowers.objects.all(),
        'all_packs': Pack.objects.all(),
        'all_decorations': Decoration.objects.all(),
    }
    return render(request, 'mainapp/designer.html', context)


@login_required
def save_bouquet(request):
    if request.method == 'POST':
        clarify = 'clarify' in request.POST

        flower_ids = request.POST.getlist('flowers')
        flowers_data = []
        total_flowers_price = 0
        for fid in flower_ids:
            count_str = request.POST.get(f'flower_count_{fid}', '0')
            try:
                count = int(count_str)
            except:
                count = 0
            if count > 0:
                try:
                    flower_obj = Flowers.objects.get(id=fid)
                    total_flowers_price += flower_obj.price * count
                    flowers_data.append({
                        'id': flower_obj.id,
                        'name': flower_obj.name_flower,
                        'count': count
                    })
                except Flowers.DoesNotExist:
                    continue

        pack_id = request.POST.get('pack')
        name_pack = ''
        pack_obj = None
        if pack_id:
            try:
                pack_obj = Pack.objects.get(id=pack_id)
                name_pack = pack_obj.name_pack
            except Pack.DoesNotExist:
                pack_obj = None

        decoration_ids = request.POST.getlist('decorations')
        decorations_qs = Decoration.objects.filter(id__in=decoration_ids)
        total_decorations_price = sum(d.price for d in decorations_qs)
        name_decoration_str = ', '.join([d.name_decoration for d in decorations_qs])

        total_price = total_flowers_price
        if pack_obj:
            total_price += pack_obj.price
        total_price += total_decorations_price

        bouquet = Bouquet.objects.create(
            user=request.user,
            total_price=total_price,
            flowers=flowers_data,
            name_pack=name_pack,
            name_decoration=name_decoration_str
        )

        return redirect(reverse('mainapp:order_bouquet', kwargs={'bouquet_id': bouquet.id}))
    return redirect('mainapp:designer')


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user)
    user_bouquet_orders = UserBouquetOrder.objects.filter(user=request.user)

    combined_orders = []

    for order in user_orders:
        combined_orders.append({
            'order': order,
            'type': 'order'
        })

    for bouquet_order in user_bouquet_orders:
        combined_orders.append({
            'order': bouquet_order,
            'type': 'bouquet'
        })

    context = {
        'title': 'Мои заказы',
        'orders': combined_orders,
    }
    return render(request, 'mainapp/orders.html', context)


@login_required
def cancel_order(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            if order.order_status == 'decorated':
                order.delete()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Нельзя отменить этот заказ'}, status=400)
        except Order.DoesNotExist:
            return HttpResponseNotFound()
    return JsonResponse({'status': 'error', 'message': 'Неверный метод'}, status=405)


@login_required
def cancel_bouquet(request, bouquet_id):
    # Получаем букет по id
    bouquet = get_object_or_404(UserBouquetOrder, id=bouquet_id, user=request.user)

    # Проверяем, что букет в статусе 'decorated'
    if hasattr(bouquet, 'order_status') and bouquet.order_status == 'decorated':
        bouquet.delete()

    # Перенаправляем обратно на страницу заказов
    return redirect('mainapp:orders')


@login_required
def basket(request):
    basket_filter = Basket.objects.filter(user=request.user)

    basket_count = basket_filter.aggregate(Sum('counts'))['counts__sum'] or 0

    total_price = basket_filter.aggregate(
        total=Sum(F('product__price') * F('counts'), output_field=FloatField())
    )['total'] or 0

    favorites_count = Favorites.objects.filter(user=request.user).count()

    for item in basket_filter:
        item.total_price = item.product.price * item.counts

    context = {
        'title': 'корзина',
        'basket': basket_filter,
        'basket_count': basket_count,
        'total_price': total_price,
        'favorites_count': favorites_count,
    }
    return render(request, 'mainapp/basket.html', context)


@login_required
def basket_add(request, pk):
    with transaction.atomic():
        product = get_object_or_404(Products, id=pk)
        errors = []

        if product.counts == 0:
            errors.append('Товара нет в наличии')
            return JsonResponse({'error': 'Товара нет в наличии', 'errors': errors}, status=400)

        basket_item, created = Basket.objects.select_for_update().get_or_create(
            user=request.user,
            product=product,
            defaults={'counts': 0}
        )

        if product.counts < 1:
            errors.append('Недостаточно товара на складе')
            return JsonResponse({'error': 'Недостаточно товара на складе', 'errors': errors}, status=400)

        basket_item.counts += 1
        product.counts -= 1

        basket_item.save()
        product.save()

        total_basket_count = Basket.objects.filter(user=request.user).aggregate(Sum('counts'))['counts__sum'] or 0

        return JsonResponse({
            'basket_count': total_basket_count,
            'item_counts': basket_item.counts,
            'errors': errors
        })


@login_required
def basket_add(request, pk):
    product = get_object_or_404(Products, id=pk)
    errors = []

    if product.counts == 0:
        errors.append('Товара нет в наличии')
        return JsonResponse({'error': 'Товара нет в наличии', 'errors': errors}, status=400)

    basket_item, created = Basket.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'counts': 0}
    )

    if product.counts < 1:
        errors.append('Недостаточно товара на складе')
        return JsonResponse({'error': 'Недостаточно товара на складе', 'errors': errors}, status=400)

    basket_item.counts += 1
    product.counts -= 1

    basket_item.save()
    product.save()

    total_basket_count = Basket.objects.filter(user=request.user).aggregate(Sum('counts'))['counts__sum'] or 0

    return JsonResponse({
        'basket_count': total_basket_count,
        'item_counts': basket_item.counts,
        'errors': errors
    })


@login_required
def basket_remove(request, pk):
    basket_item = get_object_or_404(Basket, id=pk, user=request.user)

    if basket_item.counts > 1:
        basket_item.counts -= 1
        basket_item.save()
    else:
        basket_item.delete()
    return HttpResponseRedirect(reverse('mainapp:basket'))


@login_required
def basket_delete_entire_item(request, pk):
    basket_item = get_object_or_404(Basket, id=pk, user=request.user)
    basket_item.delete()
    return HttpResponseRedirect(reverse('mainapp:basket'))


@login_required
def favorites(request):
    favorites = Favorites.objects.filter(user=request.user)
    favorites_count = Favorites.objects.filter(user=request.user).count()
    basket_count = Basket.objects.filter(user=request.user).aggregate(Sum('counts'))['counts__sum'] or 0
    context = {
        'title': 'избранное',
        'favorites': favorites,
        'favorites_count': favorites_count,
        'basket_count': basket_count,
    }
    return render(request, 'mainapp/favorites.html', context)


@login_required
def favorites_add(request, pk):
    product = get_object_or_404(Products, id=pk)

    if not Favorites.objects.filter(product=product, user=request.user).exists():
        Favorites.objects.create(product=product, user=request.user)

    favorites_count = Favorites.objects.filter(user=request.user).count()
    return JsonResponse({'favorites_count': favorites_count})


@login_required
def favorites_remove(request, pk):
    favorites_item = get_object_or_404(Favorites, product__id=pk, user=request.user)

    favorites_item.delete()

    return HttpResponseRedirect(reverse('mainapp:favorites'))


@login_required
def get_counts(request):
    user = request.user
    basket_count = Basket.objects.filter(user=user).aggregate(Sum('counts'))['counts__sum'] or 0
    favorites_count = Favorites.objects.filter(user=user).count()
    return JsonResponse({
        'basket_count': basket_count,
        'favorites_count': favorites_count,
    })


def counts_context_processor(request):
    favorites_count = 0
    basket_count = 0

    if request.user.is_authenticated:
        favorites_count = Favorites.objects.filter(user=request.user).count()
        basket_count = Basket.objects.filter(user=request.user).aggregate(Sum('counts'))['counts__sum'] or 0

    return {
        'favorites_count': favorites_count,
        'basket_count': basket_count,
    }
