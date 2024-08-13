from django.db import models
from django.utils.translation import gettext as _

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PublishingPanel,
)


from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)

from wagtail.fields import RichTextField, StreamField
from wagtail.models import (
    Page,
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    TranslatableMixin,
    PreviewableMixin,
)

from wagtail.search import index

from .blocks import BaseStreamBlock


class StandardPage(Page):
    introduction = models.TextField(
        blank=True,
        null=True,
        help_text="Provide a brief introduction or overview for this page.",
    )
    image_url = models.URLField(null=True,blank=True)
    body = StreamField(
        BaseStreamBlock(),
        verbose_name="Page body",
        blank=True,
        use_json_field=True,
        help_text="Compose the main content for this page. Utilize various content blocks to structure and format the information effectively.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel('image_url'),
        FieldPanel("body"),
    ]

    page_description = "This page type allows you to create standard content pages with an introduction and a flexible body."


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", related_name="form_fields", on_delete=models.CASCADE)


class FormPage(AbstractEmailForm):

    introduction = models.TextField(
        null=True,
        blank=True,
        help_text=" Provide a brief introduction or overview for this form page.",
    )
    image_url = models.URLField(null=True,blank=True)
    body = StreamField(
        BaseStreamBlock(),
        use_json_field=True,
        verbose_name="Page Body",
        null=True,
        blank=True,
        help_text="Compose the main content for this form page using various content blocks.",
    )

    thank_you_text = RichTextField(
        verbose_name="Thank You Text",
        blank=True,
        help_text="Customize the message displayed to users after submitting the form.",
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        InlinePanel("form_fields", heading="Form fields", label="Field"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("from_address"), FieldPanel("to_address")]),
                FieldPanel("subject"),
            ],
            heading="Email",
        ),
    ]

    page_description = "Create interactive forms with ease. Customize the page with images, introductions, and a flexible body. Manage form fields, set email notifications, and provide a personalized thank-you message."


@register_snippet
class FooterInfo(models.Model):
    links_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Enter a title for the links section in the footer.",
    )
    services_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Enter a title for the services section in the footer.",
    )
    subscribe_email_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Enter a title for the email subscription section in the footer.",
    )
    subscribe_email_body = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Enter the text or body content for the email subscription section in the footer.",
    )

    class Meta:
        verbose_name = "Footer Information"
        verbose_name_plural = "Footer Information"

    def __str__(self):
        return 'Footer Information'
    

@register_setting
class SiteSettings(BaseSiteSetting):
    logo = models.CharField(
        verbose_name="Site Logo",
        max_length=20,
        help_text="Enter the text or name for the site logo. This text will be displayed as the logo in the header and footer.",
        default="Phone Centre",
    )
    branding_title = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default="Phone Centre",
        verbose_name="Site Title",
        help_text='Enter the title to be displayed in the title tag of the website. If left blank, the default value is "Phone Centre."',
    )

    branding_welcome = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default="Welcome to Phone Centre CMS",
        verbose_name="Welcome Text",
        help_text='Enter the welcome text to be displayed on the admin home page. If left blank, the default is "Welcome to Phone Centre CMS."',
    )
    branding_login = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default="Sign in to Phone Centre",
        verbose_name="Login Text",
        help_text='Enter the text to be displayed on the login page. If left blank, the default is "Sign in to Phone Centre."',
    )


@register_setting
class GenericSettings(ClusterableModel, BaseGenericSetting):
    twitter_url = models.URLField("Twitter URL", blank=True, null=True)
    facebook_url = models.URLField("Facebook URL", blank=True, null=True)
    instagram_url = models.URLField("Instagram URL", blank=True, null=True)
    tiktok_url = models.URLField("Tiktok URL", blank=True, null=True)
    whatsapp_url = models.URLField("WhatsApp Business URL", blank=True, null=True)
    telegram_url = models.URLField("Telegram URL", blank=True, null=True)
    linkedin_url = models.URLField("LinkedIn URL", blank=True, null=True)

    email = models.CharField("Contact Email", max_length=100, blank=True, null=True)
    phone = models.CharField("Contact Phone", max_length=100, blank=True, null=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("twitter_url"),
                FieldPanel("facebook_url"),
                FieldPanel("instagram_url"),
                FieldPanel("tiktok_url"),
                FieldPanel("whatsapp_url"),
                FieldPanel("telegram_url"),
                FieldPanel("linkedin_url"),
            ],
            "Social Media URLs",
        ),
        MultiFieldPanel(
            [
                FieldPanel("email"),
                FieldPanel("phone"),
            ],
            "Email & Phone",
        ),
    ]
