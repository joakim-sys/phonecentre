from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import (
    MultiFieldPanel,
    FieldPanel,
    InlinePanel,
    FieldRowPanel,
    MultipleChooserPanel,
)
from wagtail.fields import RichTextField, StreamField

from modelcluster.fields import ParentalKey

from services.models import Service


class HomePage(Page):
    # ********************* Hero Section ***********************
    hero_welcome_text = models.CharField(
        verbose_name="Hero Welcome Text",
        max_length=255,
        blank=True,
        null=True,
        help_text="Enter a welcome message for the hero section, displayed prominently to visitors. like 'Welcome to Mars'",
    )
    hero_heading = models.CharField(
        verbose_name="Hero Heading",
        max_length=255,
        blank=True,
        null=True,
        help_text="Provide a descriptive heading for the hero section that introduces and summarizes the business.",
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Hero Image",
        related_name="+",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Choose an image to visually represent the hero section, capturing attention and conveying the essence of the business.",
    )
    hero_subheading = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=" Hero Subheading",
        help_text="Add a subheading to complement the hero heading, providing additional context or information",
    )
    hero_cta_text = models.CharField(
        verbose_name=" Call-to-Action Text",
        max_length=255,
        null=True,
        blank=True,
        help_text="Enter the text to display on the Call-to-Action (CTA) button in the hero section.",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Call-to-Action Link",
        help_text="Choose a page to link to when the CTA button in the hero section is clicked.",
    )

    # ******************** About Section **************************
    about_title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="About Section Title",
        help_text="Enter a title for the About section, providing a concise label for the content that follows.",
    )
    about_heading = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="About Heading",
        help_text="Provide a heading for the About section that succinctly describes its purpose or content.",
    )
    about_subheading = models.TextField(
        null=True,
        blank=True,
        verbose_name="About Subheading",
        help_text="Add a subheading to offer additional context or information for the About section.",
    )
    about_intro = models.TextField(
        null=True,
        blank=True,
        verbose_name="About Introduction",
        help_text="Introduce the About section with a brief overview or introductory text.",
    )

    about_body = models.TextField(
        null=True,
        blank=True,
        verbose_name="About Body",
        help_text="Compose the main content for the About section, providing detailed information and insights.",
    )
    about_cta_text = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="About CTA Text",
        help_text="Enter the text to display on the Call-to-Action (CTA) button associated with the About section.",
    )
    about_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        related_name="+",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="About CTA Link",
        help_text="Choose a page to link to when the CTA button in the About section is clicked.",
    )

    # **************** Services Section **************************
    services_title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Services Section Title",
        help_text="Enter a title for the Services section, providing a clear label for the content that follows.",
    )
    services_heading = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Services Heading",
        help_text="Provide a heading for the Services section that succinctly describes its purpose or content.",
    )
    services_subheading = models.TextField(
        null=True,
        blank=True,
        verbose_name="Services Subheading",
        help_text="Add a subheading to offer additional context or information for the Services section.",
    )

    # ************* Call to Action Section ******************
    cta_title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="CTA Section Title",
        help_text=" Enter a title for the Call to Action (CTA) section, providing a label for the content that follows.",
    )
    cta_descr = models.TextField(
        blank=True,
        null=True,
        verbose_name="CTA Description",
        help_text="Provide a description for the Call to Action (CTA) section, offering additional context or information.",
    )
    cta_text = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="CTA Text",
        help_text="Enter the text to display for the Call to Action (CTA) button in this section.",
    )
    cta_image = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="CTA Image",
        help_text="Choose an image to visually represent the Call to Action (CTA) section, capturing attention and enhancing engagement.",
    )

    cta_link = models.ForeignKey(
        "wagtailcore.Page",
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="CTA Link",
        help_text="Choose a page to link to when the CTA button in the Call to Action (CTA) section is clicked.",
    )

    # ************** Pricing Section ***********************
    pricing_title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Pricing Section Title",
        help_text="Enter a title for the Pricing section, providing a clear label for the content that follows.",
    )
    pricing_heading = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Pricing Heading",
        help_text="Provide a heading for the Pricing section that succinctly describes its purpose or content.",
    )
    pricing_subheading = models.TextField(
        blank=True,
        null=True,
        verbose_name="Pricing Subheading",
        help_text="Add a subheading to offer additional context or information for the Pricing section.",
    )

    # *************** F.A.Q Section **************************
    faq_title = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="FAQ Section Title",
        help_text="Enter a title for the Frequently Asked Questions (FAQ) section, providing a concise label for the content that follows.",
    )
    faq_heading = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="FAQ Heading",
        help_text="Provide a heading for the FAQ section that succinctly describes its purpose or content.",
    )
    faq_subheading = models.TextField(
        blank=True,
        null=True,
        verbose_name="FAQ Subheading",
        help_text="Add a subheading to offer additional context or information for the FAQ section.",
    )

    # ************ Contact Section **********************
    contact_title = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Contact Section Title",
        help_text="Enter a title for the Contact section, providing a concise label for the content that follows.",
    )
    contact_heading = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Contact Heading",
        help_text="Provide a heading for the Contact section that succinctly describes its purpose or content.",
    )
    contact_subheading = models.TextField(
        blank=True,
        null=True,
        verbose_name="Contact Subheading",
        help_text="Add a subheading to offer additional context or information for the Contact section.",
    )

    content_panels = Page.content_panels + [
        # *********** Hero Section **************
        MultiFieldPanel(
            [
                MultiFieldPanel(
                    [
                        FieldPanel("hero_image"),
                        FieldPanel("hero_welcome_text"),
                        FieldPanel("hero_heading"),
                        FieldPanel("hero_subheading"),
                    ],
                    heading="Hero Content",
                    help_text="Customize the visual and textual components of the Hero section. Upload an image, provide a welcome message, a heading, and a subheading.",
                ),
                MultiFieldPanel(
                    [
                        FieldPanel("hero_cta_text"),
                        FieldPanel("hero_cta_link"),
                    ],
                    heading="Hero CTA",
                    help_text="Configure the call-to-action (CTA) button for the Hero section. Specify the text and link for the CTA button.",
                ),
            ],
            heading="Hero Section",
            help_text="Customize the content for the Hero section. Include an image, welcome text, heading, subheading, call-to-action (CTA) text, and CTA link.",
        ),
        # ************ About Section ***********
        MultiFieldPanel(
            [
                FieldPanel("about_title"),
                FieldPanel("about_heading"),
                FieldPanel("about_subheading"),
                FieldPanel("about_intro"),
                InlinePanel(
                    "about_listed_services",
                    max_num=4,
                    heading="About Listed Services",
                    help_text="Manage and customize the services listed in the About section. Add up to 4 services with accompanying text.",
                ),
                FieldPanel("about_body"),
                MultiFieldPanel(
                    [FieldPanel("about_cta_link"), FieldPanel("about_cta_text")],
                    help_text="Configure the call-to-action (CTA) button for the About section. Specify the link and text for the CTA button.",
                ),
            ],
            heading="About Section",
            help_text="Customize the content for the About section. Include a title, heading, subheading, introduction, listed services, main body, and a call-to-action (CTA) button.",
        ),
        # ************* Services Section **********************
        MultiFieldPanel(
            [
                FieldPanel("services_title"),
                FieldPanel("services_heading"),
                FieldPanel("services_subheading"),
                MultipleChooserPanel(
                    "home_service_relation",
                    chooser_field_name="service",
                    heading="Services",
                    label="Service",
                    min_num=4,
                    help_text="Manage and customize the individual services listed in the Services section. Add up to 4 services with accompanying details.",
                    # panels=None
                ),
            ],
            heading="Services Section",
            help_text="Manage and customize the content for the Services section. Include a title, heading, subheading, and up to 4 individual services with additional details.",
        ),
        # ************** Features Section ********************
        MultipleChooserPanel(
            "home_feature_relation",
            chooser_field_name="feature",
            heading="Features",
            label="Feature",
            min_num=4,
            help_text="Manage and customize the features listed in the Features section. Add up to 12 features with accompanying details.",
            # panels=None
            max_num=12,
        ),
        # ************ CTA Section ********************
        MultiFieldPanel(
            [
                MultiFieldPanel(
                    [
                        FieldPanel("cta_image"),
                        FieldPanel("cta_title"),
                        FieldPanel("cta_descr"),
                    ],
                    heading="CTA Content",
                    help_text="Customize the visual and textual components of the Call to Action (CTA) section. Upload an image, provide a title, and a description.",
                ),
                FieldRowPanel(
                    [FieldPanel("cta_text"), FieldPanel("cta_link")],
                    heading="CTA Text and Link",
                    help_text=" Configure the button for the Call to Action (CTA) section. Specify the text and link for the button.",
                ),
            ],
            heading="CTA Section",
            help_text="Customize the content for the Call to Action (CTA) section. Include an image, title, description, and a configurable button.",
        ),
        # ************** Pricing Section **********************
        MultiFieldPanel(
            [
                FieldPanel("pricing_title"),
                FieldPanel("pricing_heading"),
                FieldPanel("pricing_subheading"),
                InlinePanel(
                    "pricing_tiers",
                    max_num=3,
                    heading="Tiers",
                    label="Pricing Tier",
                    help_text="Manage and customize the pricing tiers listed in the Pricing section. Add up to 3 pricing tiers with accompanying details.",
                ),
            ],
            heading="Pricing Section",
            help_text="Customize the content for the Pricing section. Include a title, heading, subheading, and up to 3 pricing tiers.",
        ),
        # ************* F.A.Q Section ***********************
        MultiFieldPanel(
            [
                FieldPanel("faq_title"),
                FieldPanel("faq_heading"),
                FieldPanel("faq_subheading"),
                InlinePanel(
                    "faqs",
                    heading="Frequent Questions",
                    label="Question",
                    help_text="Manage and customize the frequently asked questions listed in the F.A.Q section. Add questions and their corresponding answers.",
                ),
            ],
            heading="F.A.Q Section",
            help_text="Customize the content for the Frequently Asked Questions (F.A.Q) section. Include a title, heading, subheading, and manage frequently asked questions.",
        ),
        # ***************** ContactUs Section *************************
        MultiFieldPanel(
            [
                FieldPanel("contact_title"),
                FieldPanel("contact_heading"),
                FieldPanel("contact_subheading"),
            ],
            heading="Contact Us Section",
            help_text="Customize the content for the Contact section. Include a title, heading, subheading. The form is hardcoded within the template for now.",
        ),
    ]
    page_description = "The homepage serves as the landing page for the website. Customize it to showcase key content, introduce visitors to your site, and provide an engaging starting point for their journey."

    def services(self):
        return [
            n.service for n in self.home_service_relation.all().select_related("service")
        ]

    def features(self):
        return [
            n.feature for n in self.home_feature_relation.all().select_related("feature")
        ]


class AboutList(models.Model):
    text = models.TextField()
    page = ParentalKey(
        HomePage, related_name="about_listed_services", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text


class Faq(models.Model):
    question = models.TextField(
        help_text=" Enter the question for the Frequently Asked Questions (FAQ) section"
    )
    answer = models.TextField(
        help_text=" Provide the answer to the corresponding FAQ question."
    )
    page = ParentalKey(HomePage, related_name="faqs", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "Frequently Asked Questions"
