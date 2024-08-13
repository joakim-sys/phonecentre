from django.db import models
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.panels import MultiFieldPanel, FieldRowPanel, FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.models import Orderable

class PricingTier(Orderable, models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Tier Name",
        help_text="Enter a name for this pricing tier.",
    )
    price = models.PositiveSmallIntegerField(
        "Price", help_text="Enter the price for this tier"
    )
    is_special = models.BooleanField(
        default=False,
        verbose_name=" Special Tier",
        help_text="Check this box if this tier is special or recommended.",
    )
    special_name = models.CharField(
        max_length=100,
        default="Recommended",
        verbose_name="Special Tier Name",
        help_text='Enter a name for the special tier, e.g., "Recommended"',
    )

    cta_text = models.CharField(
        max_length=100,
        default="Buy Now",
        verbose_name=" CTA Text",
        help_text="Enter the text for the Call-to-Action (CTA) button.",
    )
    cta_link = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
        verbose_name="CTA Link",
        help_text="Choose a page to link to when the CTA button is clicked.",
    )
    pricing_features = ParentalManyToManyField(
        "PricingFeature",
        related_name="+",
        blank=True,
        verbose_name="Pricing Features",
        help_text="Select features associated with this pricing tier.",
    )

    page = ParentalKey(
        "wagtailcore.Page",
        related_name="pricing_tiers",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("price"),
        FieldRowPanel([FieldPanel("is_special"), FieldPanel("special_name")]),
        MultiFieldPanel(
            [FieldPanel("pricing_features", widget=forms.CheckboxSelectMultiple)],
            heading="Features",
        ),
        FieldRowPanel([FieldPanel("cta_text"), FieldPanel("cta_link")]),
    ]

    def __str__(self):
        return self.name

    def get_excluded_features(self):
        all_features = PricingFeature.objects.all()
        excluded_features = all_features.exclude(
            id__in=self.pricing_features.values_list("id", flat=True)
        )
        return excluded_features


class PricingFeature(models.Model):
    name = models.CharField(
        "Feature Name",
        max_length=100,
        help_text="Enter a name for this pricing feature.",
    )
    description = models.TextField(
        "Feature Description",
        help_text="Provide a description for this pricing feature.",
        null=True,
        blank=True,
    )
    # tier = models.ForeignKey(PricingTier, related_name='pricing_features',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
