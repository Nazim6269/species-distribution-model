import warnings
import requests
from pygbif import occurrences as occ
    


warnings.filterwarnings("ignore",category=DeprecationWarning)

#====== Asking GBIF which bird species have the most records in banglades (2015-2026)
res= occ.search(
    country="BD",
    taxonKey=212,
    hasCoordinate=True,
    hasGeospatialIssue=False,
    year="2015,2025",
    facet="speciesKey",
    facetLimit=150,
   limit=0 
)

#----- Read the counts per species
pairs=[]
for f in res['facets']:
    for c in f['counts']:
        pairs.append((int(c['name']),c['count']))


#----------- Look up the scientific name of each key        
for key,count in pairs[::3]:
    info = requests.get(f"https://api.gbif.org/v1/species/{key}", timeout=30).json()
    print(count, "|", info.get("canonicalName"), "|", info.get("vernacularName"))

