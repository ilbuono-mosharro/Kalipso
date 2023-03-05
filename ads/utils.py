import uuid

from django.forms import TypedChoiceField

from categories.models import Category


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename_rename = f'{uuid.uuid4()}.{ext}'
    return '{0}/user_{1}/{2}'.format(
        instance.profile.user.id, "announcement_images", filename_rename
    )


class CategoryChoiceField(TypedChoiceField):
    def __init__(self, **kwargs):
        categories_query = Category.category_manager.active_categories_searchbar()
        categories_list = []
        categories_list.insert(0, ('', "All categories"))
        for category in categories_query:
            categories_list.append((category.slug, category.name))
            for subcategory in category.category_in_sub.filter(is_active=True).values('slug', 'name'):
                categories_list.append((subcategory['slug'], f"- {subcategory['name']}"))
        kwargs['coerce'] = str
        kwargs['choices'] = categories_list
        kwargs['empty_value'] = None
        super().__init__(**kwargs)


SORTING_LIST = [
    ('-created_at', 'Newest'),
    ('-price', 'Price: Hight - Low'),
    ('price', 'Price: Low - High'),
]

PRICE_LIST = [(f"{price}", f"{price:6,}") for price in range(500, 515000, 5000)]
PRICE_LIST.insert(0, ("", '0'))
