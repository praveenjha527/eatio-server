from rest_framework import serializers
from models import AppPreferences


class AppPreferencesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppPreferences

        depth = 2

