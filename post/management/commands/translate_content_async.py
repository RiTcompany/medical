import asyncio

from django.core.management.base import BaseCommand
from aiogoogletrans import Translator
from bs4 import BeautifulSoup
from post.models import Post
from asgiref.sync import sync_to_async


class Command(BaseCommand):
    help = 'Translate Uzbek CKEditor content to English asynchronously'

    async def translate_text(self, text, translator):
        if text and text.strip():
            translation = await translator.translate(text, src='ru', dest='en')
            return translation.text
        return ' '

    async def process_post(self, post, translator):
        try:
            soup = BeautifulSoup(post.content_ru, 'html.parser')
            tasks = []
            for element in soup.find_all(text=True):
                original_text = element.string
                tasks.append(self.translate_text(original_text, translator))

            translations = await asyncio.gather(*tasks)

            for element, translation in zip(soup.find_all(text=True), translations):
                original_text = element.string
                if original_text:
                    element.replace_with(translation)

            post.content_ru = str(soup)
            await sync_to_async(post.save)()
            self.stdout.write(self.style.SUCCESS(f'Successfully translated post {post.id}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error translating post {post.id}: {e}'))

    async def handle_async(self):
        translator = Translator()
        posts = await sync_to_async(list)(Post.objects.filter(content_ru__isnull=True))

        tasks = [self.process_post(post, translator) for post in posts]
        # tasks = self.process_post(posts[0], translator)
        await asyncio.gather(*tasks)

    def handle(self, *args, **kwargs):
        asyncio.run(self.handle_async())
