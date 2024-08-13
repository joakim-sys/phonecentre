from django import template
from wagtail.models import Page, Site
from base.models import FooterInfo
from home.models import HomePage
from services.models import Service


register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


def has_children(page):
    return page.get_children().live().exists()

@register.simple_tag(takes_context=False)
def is_active(page, current_page):
    return current_page.url_path.startswith(page.url_path) if current_page else False


@register.inclusion_tag("tags/top_menu.html", takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = (
            calling_page.url_path.startswith(menuitem.url_path)
            if calling_page
            else False
        )
    return {
        "calling_page": calling_page,
        "menuitems": menuitems,
        "request": context["request"],
    }


@register.inclusion_tag("tags/top_menu_children.html", takes_context=True)
def top_menu_children(context, parent, calling_page=None):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    for menuitem in menuitems_children:
        menuitem.has_dropdown = has_menu_children(menuitem)
        menuitem.active = (
            calling_page.url_path.startswith(menuitem.url_path)
            if calling_page
            else False
        )
        menuitem.children = menuitem.get_children().live().in_menu()
    return {
        "parent": parent,
        "menuitems_children": menuitems_children,
        "request": context["request"],
    }


@register.inclusion_tag("tags/deep_dropdown_children.html", takes_context=True)
def deep_dropdown_children(context, parent, calling_page=None):
    deep_dropdown_children = parent.get_children().live().in_menu()
    for item in deep_dropdown_children:
        item.active = (
            calling_page.url_path.startswith(item.url_path) if calling_page else False
        )
    return {
        "parent": parent,
        "deep_dropdown_children": deep_dropdown_children,
        "request": context["request"],
    }


@register.inclusion_tag("tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    self = context.get("self")
    if self is None or self.depth <= 2:
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gt=1)
    return {
        "ancestors": ancestors,
        "request": context["request"],
    }


@register.inclusion_tag("base/include/footer_links_title.txt", takes_context=True)
def get_footer_links_title(context):
    footer_links_title = context.get("footer_links_title", "")
    if not footer_links_title:
        instance = FooterInfo.objects.first()
        footer_links_title = instance.links_title if instance else "Useful Links"
    return {"footer_links_title": footer_links_title}


@register.inclusion_tag("base/include/footer_services_title.txt", takes_context=True)
def get_footer_services_title(context):
    footer_services_title = context.get("footer_services_title", "")
    if not footer_services_title:
        instance = FooterInfo.objects.first()
        footer_services_title = instance.services_title if instance else "Our Services"
    return {"footer_services_title": footer_services_title}


@register.inclusion_tag(
    "base/include/footer_subscribe_email_title.txt", takes_context=True
)
def get_footer_subscribe_email_title(context):
    footer_subscribe_email_title = context.get("footer_subscribe_email_title", "")
    if not footer_subscribe_email_title:
        instance = FooterInfo.objects.first()
        footer_subscribe_email_title = (
            instance.subscribe_email_title if instance else "Join Our Newsletter"
        )
    return {"footer_subscribe_email_title": footer_subscribe_email_title}


@register.inclusion_tag(
    "base/include/footer_subscribe_email_body.txt", takes_context=True
)
def get_footer_subscribe_email_body(context):
    footer_subscribe_email_body = context.get("footer_subscribe_email_body", "")
    if not footer_subscribe_email_body:
        instance = FooterInfo.objects.first()
        footer_subscribe_email_body = (
            instance.subscribe_email_body
            if instance
            else "Stay updated on the exlusive list of events that unfold"
        )
    return {"footer_subscribe_email_body": footer_subscribe_email_body}


@register.inclusion_tag("base/include/footer_links.html", takes_context=True)
def get_footer_links(context):
    homepage = HomePage.objects.first()
    children = homepage.get_children().live()
    return {"links": children}


@register.inclusion_tag("base/include/footer_services.html", takes_context=True)
def get_footer_services(context):
    services = Service.objects.all()
    return {"services": services}
