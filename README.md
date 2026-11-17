# Compound Intelligence — local MVP

A local-first research catalogue for compounds and performance-enhancing substances. This first increment provides compound identity records, aliases, relationships, source provenance, a basic internal web UI, and a PubChem identity-data import. It intentionally has **no login workflow** and is intended for localhost use only.

## Requirements

- Python 3.11 or newer
- Internet connection for the PubChem import feature

## Windows quick start

Open PowerShell in this folder:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations compounds
python manage.py migrate
python manage.py seed_categories
python manage.py runserver
```

Open http://127.0.0.1:8000

If PowerShell blocks activation, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

## macOS / Linux quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations compounds
python manage.py migrate
python manage.py seed_categories
python manage.py runserver
```

## Current features

- Local dashboard and searchable compound catalogue.
- Manual compound creation and editing.
- Compound categories, provisional/verified/disputed identity status.
- PubChem lookup by name, with CID, formula, molecular weight and SMILES where returned.
- Alias, relationship, external identifier and source-provenance data models.
- No authentication or account setup.

## Important design notes

- The application binds to Django's default local development address (`127.0.0.1`). Do not expose this unauthenticated version to a network or the public internet.
- PubChem results are imported as **provisional**. Name matching is not proof that the returned record is the intended substance. Review identity, stereochemistry, salts, esters and synonyms before changing a record to verified.
- PubChem import is a starting connector, not a complete ingestion pipeline. It does not currently import all synonyms, stereochemical variants, metabolites or literature.
- A peptide/biologic flag is provided because not every substance is appropriately represented by a small-molecule SMILES string.
- This is a research catalogue, not a clinical decision-support system. It does not make dosing, cycle, safety or individual medical recommendations.
- SQLite is used to make local setup straightforward. The models are designed to migrate to PostgreSQL as the dataset and concurrent workload grow.

## Next development increments

1. Alias management and duplicate/identity resolution.
2. PubChem synonym and identifier ingestion with review queues.
3. Europe PMC / PubMed literature connectors and paper deduplication.
4. Study and evidence-claim models with exact source passages.
5. Research dossier generation with human approval.

## Project layout

```text
config/                 Django settings and URL routing
compounds/models.py     Core compound and provenance schema
compounds/views.py      Local UI views
compounds/services/     External data connectors
compounds/templates/    UI templates
```
