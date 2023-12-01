import json
import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from master_system.models import Comment, Post

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent


class Command(BaseCommand):
    help = """Load data from JSON file into DRF models.
    Argument to call command
    ------------------------
    --docname : str
        posts, comments
    """

    def add_arguments(self, parser):
        parser.add_argument("--docname", type=str)

    def _category_bulk_create(self, data, docname):
        bulk_list = list()
        for object in data:
            if docname == "posts":
                bulk_list.append(
                    Post(
                        title=object["title"],
                        body=object["body"],
                    )
                )
            elif docname == "comments":
                bulk_list.append(
                    Comment(
                        name=object["name"],
                        email=object["email"],
                        body=object["body"],
                        post=Post.objects.get(pk=object["postId"]),
                    )
                )
        try:
            if docname == "posts":
                Post.objects.bulk_create(bulk_list)
            elif docname == "comments":
                Comment.objects.bulk_create(bulk_list)
        except Exception as error:
            raise CommandError("During the creating an error occured:", error)
        return len(bulk_list)

    def handle(self, *args, **options):
        docname = options["docname"]
        data_path = os.path.join(BASE_DIR, "data", docname + ".json")
        with open(data_path, encoding="utf-8") as data_file:
            json_data = json.loads(data_file.read())
        num_objects = self._category_bulk_create(json_data, docname)

        self.stdout.write(self.style.SUCCESS(f"Loaded objects: {num_objects}"))
