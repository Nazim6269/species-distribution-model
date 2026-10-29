import warnings
import requests
from pygbif import occurrences as occ
warnings.filterwarnings("ignore",category=DeprecationWarning)

names = ["Oriolus xanthornus","Gracupica contra"]

for name in names:
    m = requests.get("https://api.gbif.org/v1/species/match",params={
        "name":name
    },timeout=30).json()
    key=m['usageKey']
    
    print(name)
    print("  Matched to:", m.get("scientificName"), "| status:", m.get("status"),
          "| match type:", m.get("matchType"), "| key:", key)

    total = occ.search(
        country="BD",
        taxonKey=key,
        hasCoordinate=True,
        hasGeospatialIssue=False,
        limit=0
    )['count']
    recent = occ.search(country="BD",
                        taxonKey=key,
                        hasCoordinate=True,
                        hasGeospatialIssue=False,
                        year="2015,2026")['count']
    print("  Records with coordinates:", total)
    print("  Records 2015-2025:", recent)
    print()
