from core.models import PriceHistoricModel
from historic.serializers import (
    PriceHistoricSerializer, PriceHistoricDetailSerializer
)
from rest_framework import viewsets


class PriceHistoricViewSet(viewsets.ModelViewSet):
    """View set to manage the price historic objects"""
    queryset = PriceHistoricModel.objects.all()
    serializer_class = PriceHistoricSerializer

    def get_queryset(self):
        """Returns the price objects"""
        return self.queryset.order_by('price')

    def get_serializer_class(self):
        """Returns the appropriated serializer class"""
        if self.action == 'retrieve':
            return PriceHistoricDetailSerializer
        return self.serializer_class
