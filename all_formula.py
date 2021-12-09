"""
A simple example that uses the NOMAD client library to access the archive.

Modified from source: https://nomad-lab.eu/prod/rae/docs/archive.html#first-example
to download all chemical formulas `chemical_composition_reduced` along with their calculation ids `calc_id` and `total_energy`.
"""
import pandas as pd
from nomad.client import ArchiveQuery
from nomad.metainfo import units

# exclude noble gases and certain radioactive elements, source: https://github.com/sparks-baird/mat_discover/blob/4e65b710b948c7ce269cc1741c12e219507aa2dd/mat_discover/utils/generate_elasticity_data.py#L74-L76
# fmt: off
excluded_elements = [
    "He", "Ne", "Ar", "Kr", "Xe", "Rn", "U", "Th", "Rn", "Tc", "Po", "Pu", "Pa",
    ]
# fmt: on

# %% query NOMAD database
query = ArchiveQuery(
    # url="http://nomad-lab.eu/prod/rae/api",
    query={"dft.code_name": "VASP",},
    required={
        "section_run": {
            "section_single_configuration_calculation": {"energy_total": "*",},
            "section_system": {"chemical_composition_reduced": "*"},
        },
        "section_metadata": {"calc_id": "*"},
    },
    per_page=10,
    max=100,
)

print(query)

# %% extract values
hartree_total_energies = [
    result.section_run[0]
    .section_single_configuration_calculation[-1]
    .energy_total.to(units.hartree)
    for result in query
]

hartree_total_energy_values = [
    hartree_total_energy.m for hartree_total_energy in hartree_total_energies
]

formulas = [
    result.section_run[0].section_system[0].chemical_composition_reduced
    for result in query
]

calc_ids = [result.section_metadata.calc_id for result in query]

# %% combine and save
df = pd.DataFrame(
    {
        "calc_id": calc_ids,
        "formula": formulas,
        "hartree_total_energy": hartree_total_energy_values,
    }
)

df.to_csv("all-formula.csv", index=False)
1 + 1  # breakpoint

# %% Code Graveyard
# required={
#     "section_run": {
#         "energy_total": "*",
#         "section_single_configuration_calculation": {
#             "single_configuration_calculation_to_system_ref": "*"
#         },
#     }
# },

# required={
#     "section_run": {
#         "section_single_configuration_calculation": "*",
#         "section_system": "*",
#     }
# },
# required={
#     "section_run": {"section_single_configuration_calculation": "*"},
#     "section_system": "*",
# },

#     "single_configuration_calculation_to_system_ref": {
#         "chemical_composition_reduced": "*"
#     },

# query={"domain": "dft", "atoms": ["Po"]},

# formulas = [
#     result.section_run[0]
#     .section_single_configuration_calculation[-1]
#     .single_configuration_calculation_to_system_ref.chemical_composition_reduced
#     for result in query
# ]

# from mendeleev.fetch import fetch_table
# all_elements = fetch_table("elements")["symbol"]
# elements = list(set(all_elements) - set(excluded_elements))

# "dft.optimade": [
#     f"NOT (elements HAS ANY {excluded_elements})".replace("'", '"')
# ],

