from django.core.management.base import BaseCommand
from compounds.models import CompoundCategory

CATEGORIES = [
    ('Anabolic-androgenic steroid', 'Steroidal androgens and related anabolic agents.'),
    ('SARM', 'Selective androgen receptor modulators.'),
    ('Peptide', 'Peptides and peptide-based research substances.'),
    ('Growth hormone related', 'Growth hormone, secretagogues and related compounds.'),
    ('Hormone', 'Endogenous hormones and hormone analogues.'),
    ('Stimulant', 'Stimulants and wakefulness-promoting substances.'),
    ('Metabolic agent', 'Compounds investigated for metabolic effects.'),
    ('Other performance enhancer', 'Other substances used or investigated for performance enhancement.'),
    ('Experimental / research chemical', 'Emerging or poorly characterised research substances.'),
    ('Other', 'Substances that do not fit the current categories.'),
]

class Command(BaseCommand):
    help = 'Create the starter compound categories.'
    def handle(self, *args, **options):
        for name, description in CATEGORIES:
            CompoundCategory.objects.get_or_create(name=name, defaults={'description': description})
        self.stdout.write(self.style.SUCCESS(f'Categories ready: {len(CATEGORIES)} checked.'))
