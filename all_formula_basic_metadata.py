import requests
import json

# fmt: off
excluded_elements = [
    "He", "Ne", "Ar", "Kr", "Xe", "Rn", "U", "Th", "Rn", "Tc", "Po", "Pu", "Pa",
    ]
# fmt: on

response = requests.post(
    "http://nomad-lab.eu/prod/rae/api/v1/entries/query",
    json={
        "query": {
            "and": [{"domain": "dft", "not": {"atoms": {"any": excluded_elements}}}]
        },
        "required": {"include": ["formula", "encyclopedia.material.formula_reduced"]},
        "pagination": {
            "page_size": 10,
            "page_after_value": "----9KNOtIZc9bDFEWxgjeSRsJrC",
        },
    },
)

print(json.dumps(response.json(), indent=2))

1 + 1

