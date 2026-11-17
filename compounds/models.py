from django.db import models
from django.utils.text import slugify

class CompoundCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Compound(models.Model):
    class IdentityStatus(models.TextChoices):
        UNVERIFIED = 'unverified', 'Unverified'
        PROVISIONAL = 'provisional', 'Provisional'
        VERIFIED = 'verified', 'Verified'
        DISPUTED = 'disputed', 'Disputed'
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    category = models.ForeignKey(CompoundCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name='compounds')
    description = models.TextField(blank=True)
    identity_status = models.CharField(max_length=20, choices=IdentityStatus.choices, default=IdentityStatus.UNVERIFIED)
    pubchem_cid = models.PositiveBigIntegerField(null=True, blank=True, unique=True)
    molecular_formula = models.CharField(max_length=120, blank=True)
    molecular_weight = models.CharField(max_length=80, blank=True)
    canonical_smiles = models.TextField(blank=True)
    is_peptide_or_biologic = models.BooleanField(default=False, help_text='Use when a conventional small-molecule structure is not an appropriate representation.')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or 'compound'
            candidate, n = base, 2
            while Compound.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate, n = f'{base}-{n}', n + 1
            self.slug = candidate
        super().save(*args, **kwargs)
    def __str__(self): return self.name

class CompoundAlias(models.Model):
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE, related_name='aliases')
    name = models.CharField(max_length=250, unique=True)
    alias_type = models.CharField(max_length=80, blank=True, help_text='For example: synonym, brand, abbreviation, development code')
    source_name = models.CharField(max_length=120, blank=True)
    def __str__(self): return self.name

class CompoundRelationship(models.Model):
    RELATION_TYPES = [
        ('ester_of', 'Ester of'), ('salt_of', 'Salt of'), ('metabolite_of', 'Metabolite of'),
        ('derivative_of', 'Derivative of'), ('analogue_of', 'Analogue of'),
        ('precursor_of', 'Precursor of'), ('mixture_component', 'Component of mixture'),
        ('related_to', 'Related to'),
    ]
    source_compound = models.ForeignKey(Compound, on_delete=models.CASCADE, related_name='outgoing_relationships')
    target_compound = models.ForeignKey(Compound, on_delete=models.CASCADE, related_name='incoming_relationships')
    relationship = models.CharField(max_length=40, choices=RELATION_TYPES)
    evidence_note = models.TextField(blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['source_compound', 'target_compound', 'relationship'], name='unique_compound_relationship')]
    def __str__(self): return f'{self.source_compound} {self.get_relationship_display()} {self.target_compound}'

class ExternalIdentifier(models.Model):
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE, related_name='external_identifiers')
    namespace = models.CharField(max_length=80)
    identifier = models.CharField(max_length=250)
    source_url = models.URLField(blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['namespace', 'identifier'], name='unique_external_identifier')]
    def __str__(self): return f'{self.namespace}: {self.identifier}'

class Source(models.Model):
    SOURCE_TYPES = [('database', 'Database'), ('paper', 'Scientific paper'), ('guideline', 'Guideline'), ('regulatory', 'Regulatory source'), ('other', 'Other')]
    title = models.CharField(max_length=500)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES, default='database')
    provider = models.CharField(max_length=120, blank=True)
    url = models.URLField(max_length=1000, blank=True)
    doi = models.CharField(max_length=250, blank=True)
    pmid = models.CharField(max_length=40, blank=True)
    published_date = models.DateField(null=True, blank=True)
    retrieved_at = models.DateTimeField(auto_now_add=True)
    licence = models.CharField(max_length=250, blank=True)
    notes = models.TextField(blank=True)
    def __str__(self): return self.title

class CompoundSource(models.Model):
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE, related_name='source_links')
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='compound_links')
    field_name = models.CharField(max_length=100, blank=True, help_text='Which imported field this source supports')
    source_value = models.TextField(blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['compound', 'source', 'field_name'], name='unique_compound_source_field')]
