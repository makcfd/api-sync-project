from requests import request

from django.conf import settings
from django.core.management.base import BaseCommand
from rest_framework import status

from master_system.models import Post, Comment


class Command(BaseCommand):
    help = """Syncronization with jsonplaceholder API.
    Argument to call command
    ------------------------
    entity : str
        posts, comments
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "entity",
            type=str,
            help="Entity name (posts, comments) to syncronize",
        )

    def _check_resourse(self, url):
        response = request(method="GET", url=url)
        return True if response.status_code == status.HTTP_200_OK else False

    def _perform_sync(self, objects):
        counter = 0
        for obj in objects:
            url = settings.BASE_JSON_PH_URL + "/" + str(obj.id)
            # TODO add try catch
            if self._check_resourse(url):
                response = request(method="PUT", url=url, data=obj.json())
            else:
                response = request(
                    method="POST",
                    url=settings.BASE_JSON_PH_URL,
                    data=obj.json(),
                )
            if response.status_code in [200, 201]:
                obj.is_synced = True
                obj.save()
                counter += 1
        return counter

    def handle(self, *args, **options):
        entity = options["entity"]
        if entity == "posts":
            entity_to_synch = Post.objects.filter(is_synced=False)
        elif entity == "comments":
            entity_to_synch = Comment.objects.filter(is_synced=False)
        num_obj = self._perform_sync(entity_to_synch)

        self.stdout.write(self.style.SUCCESS(f"{entity} synced: {num_obj}"))
