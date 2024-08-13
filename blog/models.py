from django.db import models
from django.contrib import messages
from django import forms
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.models import Page, Orderable, ClusterableModel
from wagtail.fields import StreamField
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import (
    MultiFieldPanel,
    FieldPanel,
    FieldRowPanel,
    MultipleChooserPanel,
    InlinePanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search import index

from taggit.models import TaggedItemBase, Tag
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from autoslug import AutoSlugField

from base.blocks import BaseStreamBlock


class BlogCategoryRelationship(Orderable, models.Model):
    page = ParentalKey(
        "BlogPage", related_name="blog_category_relationship", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        "Category", related_name="category_blog_relationship", on_delete=models.CASCADE
    )

    panels = [FieldPanel("category")]


class BlogAuthorRelationship(Orderable, models.Model):
    page = ParentalKey(
        "BlogPage",
        related_name="blog_author_relationship",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        "Author",
        related_name="author_blog_relationship",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("author")]


# ************************ BLOG TAG *****************************************
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


# *********************** BLOG PAGE **********************************
class BlogPage(Page):
    introduction = models.TextField(
        help_text="A brief overview or introduction to the post.", blank=True
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Featured Image",
        help_text="An image that represents or is associated with the post. This image may be used as a thumbnail or featured image.",
    )
    body = StreamField(
        BaseStreamBlock(),
        verbose_name="Page Body",
        blank=True,
        use_json_field=True,
        null=True,
        help_text="The main content of the post. You can add and organize different types of content blocks here.",
    )

    subtitle = models.CharField(
        blank=True,
        max_length=255,
        null=True,
        help_text="A short additional title or description for the post.",
    )
    tags = ClusterTaggableManager(through="BlogPageTag", blank=True)
    date_published = models.DateField(
        blank=True, null=True, help_text="The date when the post was published."
    )
    # categories = ParentalManyToManyField(
    #     "Category",
    #     verbose_name="Categories",
    #     blank=True,
    #     related_name="posts",
    #     help_text="Select categories that best describe the content of the post.",
    # )

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("introduction"),
        index.SearchField("subtitle"),
        index.SearchField("tags"),
        index.SearchField("body"),
        index.FilterField("date_published"),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel("date_published"),
        MultipleChooserPanel(
            "blog_author_relationship",
            chooser_field_name="author",
            heading=" Blog Authors",
            label="Author",
            panels=None,
            max_num=3,
        ),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
        FieldPanel("subtitle"),
        FieldPanel("body"),
        # FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        MultipleChooserPanel(
            "blog_category_relationship",
            chooser_field_name="category",
            heading="Categories",
            label="Category",
            panels=None,
            max_num=2,
            help_text="Select categories that best describe the content of the post.",
        ),
        FieldPanel("tags"),
    ]

    page_description = "This page allows you to create and manage  posts. Customize \
        various elements such as the title, introduction, subtitle, featured image, main \
            content, tags, publication date, and categories."

    class Meta:
        verbose_name = "Blogpage"
        verbose_name_plural = "Blogpages"

    def authors(self):
        return [
            n.author
            for n in self.blog_author_relationship.all().select_related("author")
        ]

    @property
    def categories(self):
        cats = [
            n.category
            for n in self.blog_category_relationship.all().select_related("category")
        ]
        base_url = self.get_parent().url
        for cat in cats:
            cat.url = f"{base_url}categories/{cat.name}"
        return cats

    def get_author(self):
        try:
            author = self.authors()[0]
        except:
            author = ""
        return author

    @property
    def get_tags(self):
        tags = self.tags.all()
        base_url = self.get_parent().url
        for tag in tags:
            tag.url = f"{base_url}tags/{tag.slug}/"
        return tags

    # def get_all_categories(self):
    #     categories = Category.objects.all()
    #     base_url = self.get_parent().url
    #     for category in categories:
    #         category.url = f"{base_url}categories/{category.name}"
    #     return categories

    def get_context(self, request):
        context = super(BlogPage, self).get_context(request)
        context["author"] = self.get_author()
        context["latest_posts"] = (
            BlogPage.objects.live().exclude(id=self.id).order_by("-date_published")
        )
        return context

    parent_page_types = ["BlogListing"]
    subpage_types = []


# *********************** BLOG LISTING PAGE ******************************
class BlogListing(RoutablePageMixin, Page):
    introduction = models.TextField(
        verbose_name="Introduction Text",
        blank=True,
        help_text="This text serves as a brief introduction or overview for the blog listing page. It may provide context or a summary of the content featured on this page.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
    ]

    subpage_types = ["BlogPage"]
    page_description = "This page lists all published blog entries, providing editors with an overview of the latest content."

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(BlogListing, self).get_context(request)
        posts = BlogPage.objects.descendant_of(self).live().order_by("-date_published")
        context["posts"] = self.paginate(request, posts)
        context["latest_posts"] = self.get_posts()[:5]
        context["tags"] = self.get_child_tags()
        return context

    class Meta:
        verbose_name = "Blog Listing"
        verbose_name_plural = "Blog Listings"

    @route(r"^tags/$", name="tag_archieve")
    @route(r"^tags/([\w-]+)/$", name="tag_archieve")
    def tag_archieve(self, request, tag=None):
        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no posts tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)
        posts = self.get_posts(tag=tag)
        tags = self.get_child_tags()
        latest_posts = self.get_latest_posts()
        context = {
            "self": self,
            "tag": tag,
            "posts": posts,
            "tags": tags,
            "latest_posts": latest_posts,
        }
        return render(request, "blog/blog_listing.html", context)

    @route(r"^categories/$", name="category_view")
    @route(r"^categories/([\w-]+)/$", name="category_view")
    def category_view(self, request, category=None):
        try:
            category = Category.objects.get(name=category)
        except Category.DoesNotExist:
            if category:
                msg = 'There are no entries associated with "{}" category'.format(
                    category
                )
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)
        posts = self.get_posts_by_category(category=category)
        tags = self.get_child_tags()
        latest_posts = self.get_latest_posts()

        context = {
            "self": self,
            "posts": posts,
            "category": category,
            "tags": tags,
            "latest_posts": latest_posts,
        }
        return render(request, "blog/blog_listing.html", context)

    def get_latest_posts(self):
        latest_posts = (
            BlogPage.objects.live().exclude(id=self.id).order_by("-date_published")
        )
        return latest_posts

    def serve_preview(self, request, mode_name):
        return self.serve(request)

    def get_posts(self, tag=None):
        posts = BlogPage.objects.live().descendant_of(self).order_by("-date_published")
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    # def get_posts_by_category(self, category=None):
    #     posts = BlogPage.objects.live().descendant_of(self).order_by("-date_published")
    #     if category:
    #         posts = category.posts.all()
    #     return posts

    def get_posts_by_category(self, category=None):
        posts = BlogPage.objects.live().descendant_of(self).order_by("-date_published")
        if category:
            posts = [
                n.page.specific
                for n in BlogCategoryRelationship.objects.filter(
                    category__in=[category]
                )
            ]
        return posts

    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags

    def paginate(self, request, *args):
        page = request.GET.get("page")
        paginator = Paginator(self.get_posts(), 2)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages


# ******************** BLOG CATEGORY *********************************
class Category(models.Model):
    name = models.CharField(
        "Category Name",
        max_length=255,
        unique=True,
        help_text="Enter a unique name for the category. Categories are used to classify and organize blog posts. Choose a descriptive name that reflects the content associated with this category.",
    )
    slug = AutoSlugField(populate_from="name",null=True)
    panels = [FieldPanel("name")]

    @property
    def pages_count(self):
        pages = [n.page for n in self.category_blog_relationship.all()]
        return len(pages)

    def __str__(self):
        # return self.name.capitalize()
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# *************** AUTHOR *******************************
class Author(models.Model):
    first_name = models.CharField(
        "First name", max_length=254, help_text="Enter the first name of the author"
    )
    last_name = models.CharField(
        "Last name", max_length=254, help_text="Enter the last name of the author."
    )
    job_title = models.CharField(
        "Job Title",
        max_length=254,
        blank=True,
        null=True,
        help_text="Optionally, provide the job title of the author.",
    )

    twitter_url = models.URLField(
        "X URL",
        blank=True,
        null=True,
        help_text="Optionally, enter the Twitter URL of the author.",
    )
    facebook_url = models.URLField(
        "Facebook URL",
        blank=True,
        null=True,
        help_text="Optionally, enter the Facebook URL of the author.",
    )
    instagram_url = models.URLField(
        "Instagram URL",
        blank=True,
        null=True,
        help_text=" Optionally, enter the Instagram URL of the author.",
    )

    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Optionally, provide a brief biography or description of the author.",
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [FieldRowPanel([FieldPanel("first_name"), FieldPanel("last_name")])],
            heading="Author Name",
        ),
        MultiFieldPanel(
            [
                FieldPanel("twitter_url"),
                FieldPanel("facebook_url"),
                FieldPanel("instagram_url"),
            ],
            "Social Media URLs",
        ),
        FieldPanel("job_title"),
        FieldPanel("bio"),
        FieldPanel("image"),
    ]

    @property
    def thumb_image(self):
        try:
            return self.image.get_rendition("fill-45x45").img_tag()
        except:
            return ""

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
