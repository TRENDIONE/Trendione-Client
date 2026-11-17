from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CompoundForm
from .models import Compound, CompoundCategory, CompoundSource, ExternalIdentifier, Source
from .services.pubchem import lookup_compound, PubChemError


def dashboard(request):
    recent = Compound.objects.order_by('-updated_at')[:8]
    return render(request, 'compounds/dashboard.html', {'compound_count': Compound.objects.count(), 'category_count': CompoundCategory.objects.count(), 'recent': recent})


def compound_list(request):
    q = request.GET.get('q', '').strip()
    compounds = Compound.objects.select_related('category').all()
    if q:
        compounds = compounds.filter(Q(name__icontains=q) | Q(aliases__name__icontains=q) | Q(pubchem_cid__icontains=q)).distinct()
    return render(request, 'compounds/list.html', {'compounds': compounds[:250], 'q': q})


def compound_detail(request, pk):
    compound = get_object_or_404(Compound.objects.select_related('category'), pk=pk)
    return render(request, 'compounds/detail.html', {'compound': compound})


def compound_create(request):
    if request.method == 'POST':
        form = CompoundForm(request.POST)
        if form.is_valid():
            compound = form.save()
            messages.success(request, 'Compound created.')
            return redirect('compound_detail', pk=compound.pk)
    else:
        form = CompoundForm()
    return render(request, 'compounds/form.html', {'form': form, 'heading': 'Add compound'})


def compound_edit(request, pk):
    compound = get_object_or_404(Compound, pk=pk)
    if request.method == 'POST':
        form = CompoundForm(request.POST, instance=compound)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compound updated.')
            return redirect('compound_detail', pk=compound.pk)
    else:
        form = CompoundForm(instance=compound)
    return render(request, 'compounds/form.html', {'form': form, 'heading': f'Edit {compound.name}'})


def pubchem_import(request):
    if request.method == 'POST':
        term = request.POST.get('term', '').strip()
        try:
            result = lookup_compound(term)
            cid = result.get('CID')
            compound = Compound.objects.filter(pubchem_cid=cid).first() if cid else None
            if compound is None:
                compound = Compound.objects.filter(name__iexact=term).first()
            if compound is None:
                compound = Compound(name=term, identity_status=Compound.IdentityStatus.PROVISIONAL)
            compound.pubchem_cid = cid
            compound.molecular_formula = result.get('MolecularFormula', '') or ''
            compound.molecular_weight = str(result.get('MolecularWeight', '') or '')
            compound.canonical_smiles = result.get('ConnectivitySMILES', '') or result.get('CanonicalSMILES', '') or ''
            compound.save()
            source, _ = Source.objects.get_or_create(url=f'https://pubchem.ncbi.nlm.nih.gov/compound/{cid}', defaults={
                'title': f'PubChem Compound Summary: CID {cid}', 'source_type': 'database', 'provider': 'PubChem',
                'licence': 'PubChem data; check individual record/source terms before redistribution',
            })
            for field, value in [('molecular_formula', compound.molecular_formula), ('molecular_weight', compound.molecular_weight), ('canonical_smiles', compound.canonical_smiles)]:
                CompoundSource.objects.update_or_create(compound=compound, source=source, field_name=field, defaults={'source_value': value})
            if cid:
                ExternalIdentifier.objects.get_or_create(compound=compound, namespace='PubChem CID', identifier=str(cid), defaults={'source_url': source.url})
            messages.success(request, f'Imported PubChem identity data for {compound.name}. Identity remains provisional until reviewed.')
            return redirect('compound_detail', pk=compound.pk)
        except PubChemError as exc:
            messages.error(request, str(exc))
    return render(request, 'compounds/pubchem_import.html')
