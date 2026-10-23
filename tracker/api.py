from rest_framework import viewsets

from .models import Application
from .serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        qs = Application.objects.filter(owner=self.request.user)
        status = self.request.query_params.get("status")
        if status in Application.Status.values:
            qs = qs.filter(status=status)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
