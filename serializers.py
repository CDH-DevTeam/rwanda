from rest_framework_gis.serializers import GeoFeatureModelSerializer
from diana.abstract.serializers import DynamicDepthSerializer
from diana.utils import get_fields, DEFAULT_FIELDS
from .models import *

class PlaceOfInterestSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PlaceOfInterest
        fields = get_fields(PlaceOfInterest, exclude=DEFAULT_FIELDS) + ['names', 'id']
        geo_field = 'geometry'
        depth = 2
class TIFFImageSerializer(DynamicDepthSerializer):

    class Meta:
        model = Image
        fields = get_fields(Image, exclude=DEFAULT_FIELDS) 