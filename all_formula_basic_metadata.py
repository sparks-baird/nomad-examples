import requests
import json
import numpy as np
from tqdm import trange
import pandas as pd

# fmt: off
excluded_elements = [
    "He", "Ne", "Ar", "Kr", "Xe", "Rn", "U", "Th", "Rn", "Tc", "Po", "Pu", "Pa",
    ]
# fmt: on


def get_query_dict(page_after_value, page_size=10):
    d = {
        "query": {
            "and": [{"domain": "dft", "not": {"atoms": {"any": excluded_elements}}}]
        },
        "required": {"include": ["formula"]},
        "pagination": {"page_size": page_size, "page_after_value": page_after_value},
    }
    return d


def post_request(
    page_start_calc_id, return_next_page=False, return_n_iter=False, page_size=10
):
    response = requests.post(
        "http://nomad-lab.eu/prod/rae/api/v1/entries/query",
        json=get_query_dict(page_start_calc_id, page_size=page_size),
    )
    result = response.json()
    next_page_calc_id = result["pagination"]["next_page_after_value"]

    n_entries = result["pagination"]["total"]
    n_iter = np.ceil((n_entries - page_size) / page_size)

    if return_next_page and return_n_iter:
        return result, next_page_calc_id, n_iter
    elif return_next_page and not return_n_iter:
        return result, next_page_calc_id
    elif not return_next_page and return_n_iter:
        return result, n_iter
    else:
        return result


def post_first_request(page_start_calc_id, page_size=10):
    result, next_page_calc_id, n_iter = post_request(
        page_start_calc_id,
        return_next_page=True,
        return_n_iter=True,
        page_size=page_size,
    )
    return result, next_page_calc_id, n_iter

def get_data(page_start_calc_id, page_size=10):
    result, next_page_calc_id, n_iter = post_first_request(page_start_calc_id, page_size=page_size)
    data = result["data"]
    
    for _ in trange(n_iter):
        result, next_page_calc_id = post_request(next_page_calc_id)
        d = result["data"]
        data.append(d)
        
    df = pd.DataFrame(data)
    
    return df
        
first_calc_id = "----9KNOtIZc9bDFEWxgjeSRsJrC"
page_size = 10
df = get_data(first_calc_id, page_size=page_size)

1 + 1

# %% Code Graveyard
# response0 = requests.post(
#     "http://nomad-lab.eu/prod/rae/api/v1/entries/query",
#     json={
#         "query": {
#             "and": [{"domain": "dft", "not": {"atoms": {"any": excluded_elements}}}]
#         },
#         "required": {"include": ["formula"]},
#         "pagination": {"page_size": 10, "page_after_value": first_page_after_value,},
#     },
# )

# print(json.dumps(response.json(), indent=2))

# result, next_page_calc_id, n_iter = post_first_request(first_calc_id)

# for i in range(n_iter):
#     result, next_page_calc_id = post_request(next_page_calc_id)
#     results.append(result)
# print(results)