from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Application
        fields = ["id", "owner", "company", "role", "status", "applied_on", "job_url", "notes", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]
