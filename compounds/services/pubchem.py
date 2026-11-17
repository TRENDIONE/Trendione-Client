"""Small, deliberately conservative PubChem PUG REST client."""
import requests
from urllib.parse import quote

BASE = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'

class PubChemError(Exception): pass

def lookup_compound(term: str) -> dict:
    term = term.strip()
    if not term:
        raise PubChemError('Enter a compound name.')
    safe = quote(term, safe='')
    url = f'{BASE}/compound/name/{safe}/property/IUPACName,MolecularFormula,MolecularWeight,CanonicalSMILES,InChIKey/JSON'
    try:
        response = requests.get(url, timeout=20, headers={'User-Agent': 'CompoundIntelligenceLocal/0.1 (research catalog)'})
    except requests.RequestException as exc:
        raise PubChemError(f'Could not contact PubChem: {exc}') from exc
    if response.status_code == 404:
        raise PubChemError('PubChem did not find a matching compound. Try another name or add it manually as unverified.')
    if not response.ok:
        raise PubChemError(f'PubChem returned HTTP {response.status_code}.')
    try:
        props = response.json()['PropertyTable']['Properties'][0]
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise PubChemError('PubChem returned an unexpected response.') from exc
    return props
