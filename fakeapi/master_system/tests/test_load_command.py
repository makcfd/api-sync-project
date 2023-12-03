import os
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.test import TransactionTestCase

TEST_DIR = Path(__file__).resolve().parent


class CommandTestCase(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        """Fixtures for the command tests."""
        super().setUpClass()
        cls.fixtures_path = os.path.join(TEST_DIR, "fixtures")

    def test_command_posts_loading(self):
        """Successfully Posts loading data with custom command."""
        out = StringIO()
        file_path = os.path.join(
            self.fixtures_path,
            "posts_for_test" + ".json",
        )
        call_command(
            "load_json_data",
            "posts_for_test",
            "--path",
            file_path,
            stdout=out,
        )
        # print("After loading", Post.objects.all().count())
        self.assertIn("Loaded objects", out.getvalue())

    def test_command_comments_loading(self):
        """Successfully Comments loading data with custom command."""
        out = StringIO()
        posts_path = os.path.join(
            self.fixtures_path,
            "posts_for_test" + ".json",
        )
        call_command(
            "load_json_data",
            "posts_for_test",
            "--path",
            posts_path,
            stdout=out,
        )
        comments_file_path = os.path.join(
            self.fixtures_path,
            "comments_for_test" + ".json",
        )
        call_command(
            "load_json_data",
            "comments_for_test",
            "--path",
            comments_file_path,
            stdout=out,
        )
        self.assertIn("Loaded objects", out.getvalue())
