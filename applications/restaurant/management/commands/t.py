"""
Management utility to create superusers.
"""
from __future__ import unicode_literals
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        from applications.restaurant import foursquare
        print foursquare.FourSquare().search_venues(-40.7, -74)

