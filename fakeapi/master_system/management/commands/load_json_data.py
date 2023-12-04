import json
import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from master_system.models import Comment, Post

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):
    help = """Load data from JSON file into DRF models.
    Argument to call command
    ------------------------
    --docname : str
        posts, comments
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "docname",
            type=str,
            help="Document name (posts, comments)",
        )
        parser.add_argument(
            "--path",
            type=str,
            required=False,
            help="Optional path to the JSON file",
            default=None,
        )

    def _category_bulk_create(self, data, docname):
        bulk_list = list()
        for object in data:
            if "posts" in docname:
                bulk_list.append(
                    Post(
                        title=object["title"],
                        body=object["body"],
                    )
                )
            elif "comments" in docname:
                bulk_list.append(
                    Comment(
                        name=object["name"],
                        email=object["email"],
                        body=object["body"],
                        postId=Post.objects.get(pk=object["postId"]),
                    )
                )
        try:
            if "posts" in docname:
                Post.objects.bulk_create(bulk_list)
            elif "comments" in docname:
                Comment.objects.bulk_create(bulk_list)
        except Exception as error:
            raise CommandError("During the creation an error occured:", error)
        return len(bulk_list)

    def handle(self, *args, **options):
        docname = options["docname"]
        file_path = options["path"]
        if not file_path:
            file_path = os.path.join(BASE_DIR, "data", docname + ".json")
        with open(file_path, encoding="utf-8") as data_file:
            json_data = json.loads(data_file.read())
        num_objects = self._category_bulk_create(json_data, docname)

        self.stdout.write(self.style.SUCCESS(f"Loaded objects: {num_objects}"))
