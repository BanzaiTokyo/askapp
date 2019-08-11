from django.core.management.base import BaseCommand, CommandError
from askapp.score_calculator import calculate_scores


class Command(BaseCommand):
    def handle(self, *args, **options):
        calculate_scores(weeks=0)
