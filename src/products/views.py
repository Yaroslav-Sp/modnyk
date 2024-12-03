from decimal import Decimal

from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from cart.forms import CartItemForm
from cart.models import Cart, CartItem
from common.views import FavoriteMixin
from products.models import Category, Product, Size
from reviews.forms import ReviewForm
from shop.models import Favorite


class ProductInfo(DetailView):
    model = Product
    template_name = "product_profile.html"
    context_object_name = "product"

    def get_queryset(self):
        return super().get_queryset().select_related("category__parent__parent")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        reviews = product.reviews.select_related("customer").order_by("-create_date")

        paginator = Paginator(reviews, 18)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["reviews"] = page_obj
        review_stats = product.reviews.aggregate(average_rating=Avg("rating"), review_count=Count("id"))
        context["average_rating"] = review_stats["average_rating"]
        context["review_count"] = review_stats["review_count"]
        context["review_form"] = ReviewForm()
        context["cart_form"] = CartItemForm()

        user = self.request.user

        if not user.is_authenticated:
            context["is_product_in_cart"] = False
            context["favorite_boolean"] = False
        else:
            context["favorite_boolean"] = Favorite.objects.filter(customer=user, product=product).exists()
            context["is_product_in_cart"] = CartItem.objects.filter(cart__customer=user, product=product).exists()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        post_request = request.POST
        form_type = post_request.get("form_type")
        general_params = {"customer": request.user, "product": self.object}

        if form_type == "review_form":
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.customer = general_params["customer"]
                review.product = general_params["product"]
                review.save()
                return redirect("products:product_info", pk=self.object.pk)
            else:
                context["review_form"] = form
                return self.render_to_response(context)

        elif form_type == "cart_form":
            form = CartItemForm(request.POST)
            if form.is_valid():
                cart_item = form.save(commit=False)
                cart, created = Cart.objects.get_or_create(customer=general_params["customer"])
                cart_item.cart = cart
                cart_item.product = general_params["product"]
                cart_item.save()
                return redirect("products:product_info", pk=self.object.pk)
            else:
                context["cart_form"] = form
                return self.render_to_response(context)

        elif form_type == "favorite_form":
            favorite_item = Favorite.objects.filter(**general_params)
            if favorite_item.exists():
                favorite_item.delete()
            else:
                Favorite.objects.create(**general_params)

        return redirect("products:product_info", pk=self.object.pk)


class ProductList(FavoriteMixin, ListView):
    model = Product
    template_name = "product_list.html"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("category__parent__parent")
            .prefetch_related("products_images")
            .annotate(average_rating=Avg("reviews__rating"), review_count=Count("reviews"))
        )
        categories = Category.objects.select_related("parent__parent")

        gender_names = self.request.GET.getlist("gender")
        main_category_names = self.request.GET.getlist("main_category")
        sub_category_names_row = self.request.GET.getlist("sub_category")

        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        size = self.request.GET.getlist("size")

        sort_by = self.request.GET.get("sort_by")

        sub_category_names = []
        self.control_field = []

        for sub_category in sub_category_names_row:
            split_data = sub_category.split("|")
            main_category_names.append(split_data[1])
            sub_category_names.append(split_data[0])
            self.control_field.append(split_data[1])
        self.selected_filters = []
        params_for_filter = {}

        if gender_names or main_category_names or sub_category_names:
            categories = categories.filter(level=2)

            all_categories = Category.get_history_for_categories(
                categories, gender_names, main_category_names, sub_category_names
            )
            params_for_filter["category__pk__in"] = all_categories

            self.selected_filters += list(set(gender_names + main_category_names + sub_category_names))

        if size:
            params_for_filter["size__name__in"] = size
            self.selected_filters += size

        if min_price:
            min_price = Decimal(min_price)
            params_for_filter["price__gte"] = min_price
            self.selected_filters.append(f"min price: {min_price}")
            self.selected_min_price = min_price
        else:
            self.selected_min_price = None

        if max_price:
            max_price = Decimal(max_price)
            params_for_filter["price__lte"] = max_price
            self.selected_filters.append(f"max price: {max_price}")
            self.selected_max_price = max_price
        else:
            self.selected_max_price = None

        queryset = queryset.filter(**params_for_filter)

        if sort_by:
            if sort_by == "rating":
                queryset = queryset.order_by("-average_rating")
                self.sort_by = "rating"
            elif sort_by == "price_desc":
                queryset = queryset.order_by("-price")
                self.sort_by = "price_desc"
            elif sort_by == "price_asc":
                queryset = queryset.order_by("price")
                self.sort_by = "price_asc"
        else:
            queryset = queryset.order_by("-average_rating")
            self.sort_by = "rating"
        self.products_count = queryset.count()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_filters"] = self.selected_filters
        context["control_field"] = self.control_field
        context["selected_min_price"] = self.selected_min_price
        context["selected_max_price"] = self.selected_max_price
        context["sort_by"] = self.sort_by
        context["sizes"] = Size.objects.all()
        context["products_count"] = self.products_count
        if isinstance(self.request.user, AnonymousUser):
            context["favorite_boolean"] = []
        else:
            context["favorite_boolean"] = Favorite.objects.filter(customer=self.request.user).values_list(
                "product", flat=True
            )

        paginator = Paginator(self.get_queryset(), 48)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["products"] = page_obj
        categories = Category.objects.select_related("parent__parent")
        main_categories = categories.filter(level=1).values("name").distinct()

        res = []

        for main_category in main_categories:
            sub_categories = categories.filter(level=2, parent__name=main_category["name"]).values("name").distinct()

            sub_category_names = [category["name"] for category in sub_categories]
            res.append((main_category["name"], sub_category_names))
        context["categories_level_1"] = res
        return context
