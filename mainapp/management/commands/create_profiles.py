from django.core.management.base import BaseCommand
from authapp.models import ArtShopUser, ArtShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in ArtShopUser.objects.filter(artshopuserprofile__isnull=True):
            artshopuserprofile = ArtShopUserProfile(user=user)
            artshopuserprofile.save()

            