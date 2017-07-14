from django.core.management.base import BaseCommand, CommandError
from prodfloor.models import Info,Stops

class Command(BaseCommand):
    help = 'Ends the shift of the Users'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['user_id']:
            try:
                poll = Info.objects.get(pk=poll_id)
            except Info.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))