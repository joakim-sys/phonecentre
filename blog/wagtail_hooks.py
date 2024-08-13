from wagtail import hooks
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.snippets.models import register_snippet

from .models import Author, Category


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        "wagtailfontawesomesvg/brands/twitter.svg",
    ]


class AuthorViewSet(SnippetViewSet):
    model = Author
    menu_label = "Authors"
    icon = "user"
    list_display = (
        "first_name",
        "last_name",
        "job_title",
        "thumb_image",
    )
    list_filter = {"job_title": ["icontains"]}


class CategoryViewSet(SnippetViewSet):
    model = Category
    menu_label = "Blog Categories"
    icon = ""
    icon = 'tag'
    list_display = ("name",)
    list_filter = {"name": ["icontains"]}


class BlogSnippetViewSetGroup(SnippetViewSetGroup):
    menu_label = 'Blog Snippets'
    menu_icon = 'snippet'
    menu_order = 300
    items = (CategoryViewSet, AuthorViewSet)

register_snippet(BlogSnippetViewSetGroup)