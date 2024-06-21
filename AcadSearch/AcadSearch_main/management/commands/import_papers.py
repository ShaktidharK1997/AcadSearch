import json
from django.core.management.base import BaseCommand
from AcadSearch_main.models import Paper, Author, Journal

class Command(BaseCommand):
    help = 'Import papers from a dataset'

    def handle(self, *args, **kwargs):
        # Load the dataset
        with open('./SemanticScholarDataset1', 'r') as file:
            data = json.load(file)
        
        # Parse the dataset and save to database
        for item in data:
            authors = item.get('authors', [])
            author_instances = []
            for author in authors:
                author_instance, created = Author.objects.get_or_create(
                    author_id=author['authorId'],
                    defaults={'name': author['name']}
                )
                author_instances.append(author_instance)
            
            journal_data = item.get('journal', {})
            journal_instance, created = Journal.objects.get_or_create(
                journal_id=item['publicationvenueid'],
                defaults={
                    'name': journal_data.get('name', ''),
                    'pages': journal_data.get('pages', '').strip(),
                    'volume': journal_data.get('volume', '').strip()
                }
            )

            paper_instance, created = Paper.objects.get_or_create(
                corpus_id=item['corpusid'],
                defaults={
                    'title': item['title'],
                    'year': item.get('year', None),
                    'citation_count': item.get('citationcount', 0),
                    'influential_citation_count': item.get('influentialcitationcount', 0),
                    'is_open_access': item.get('isopenaccess', False),
                    'url': item['url'],
                    'publication_date': item.get('publicationdate', None),
                    'journal': journal_instance
                }
            )
            paper_instance.authors.set(author_instances)

        self.stdout.write(self.style.SUCCESS('Successfully imported papers'))
