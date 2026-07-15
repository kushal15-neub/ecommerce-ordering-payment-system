from django.core.cache import cache

from .models import Category, Product


def get_all_child_categories(category):
    """
    DFS Traversal
    Returns all descendant categories
    """

    result = []

    def dfs(node):
        children = Category.objects.filter(parent=node)

        for child in children:
            result.append(child)
            dfs(child)

    dfs(category)

    return result


def get_category_and_children_ids(category):
    """
    Returns current category ID
    + all descendant category IDs
    """

    categories = get_all_child_categories(category)

    ids = [category.id]

    for cat in categories:
        ids.append(cat.id)

    return ids


def get_category_tree(category_id):
    """
    DFS + Cache
    Returns category hierarchy as names
    """

    cache_key = f"category_tree_{category_id}"

    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    category = Category.objects.get(id=category_id)

    categories = get_all_child_categories(category)

    result = [cat.name for cat in categories]

    cache.set(
        cache_key,
        result,
        timeout=300
    )

    return result


def get_recommended_products(product, limit=5):
    """
    Recommend related products using category tree (DFS).
    """

    if not product.category:
        return Product.objects.exclude(
            id=product.id
        )[:limit]

    category_ids = get_category_and_children_ids(
        product.category
    )

    return Product.objects.filter(
        category_id__in=category_ids
    ).exclude(
        id=product.id
    )[:limit]