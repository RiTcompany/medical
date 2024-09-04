import re

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from post.models import Post

class Command(BaseCommand):
    help = 'Translate Uzbek CKEditor content to English'

    def handle(self, *args, **kwargs):
        posts = Post.objects.all()

        for post in posts:
            if post.id == 54:
                try:
                    if "youtu" in post.content:
                        post.youtube_wrapper = ''
                        post.youtube_link = ''
                        soup = BeautifulSoup(post.content, 'html.parser')
                        a = soup.findAll('a')
                        for el in a:
                            if "youtu" in str(el):
                                post.youtube_wrapper = str(el)
                                post.youtube_link = str(el['href'])
                                # post.save()
                                self.stdout.write(self.style.SUCCESS(f'{post.id}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error translating post {post.id}: {e}'))


