from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.snippets.models import register_snippet

from services.models import Service
from features.models import Feature


class ServiceSnippetView(SnippetViewSet):
    model = Service
    menu_label = 'Services Offered'
    icon = 'briefcase'



class FeatureSnippetView(SnippetViewSet):
    model = Feature
    icon = 'gear'
    menu_label = 'Features'



class ServicesFeaturesViewSetGroup(SnippetViewSetGroup):
    menu_label = 'Services & Features'
    menu_icon = 'briefcase'
    menu_order = 400
    items = (ServiceSnippetView,FeatureSnippetView)

# Uncomment the line below to register Service and Feature as snippets
# register_snippet(ServicesFeaturesViewSetGroup)