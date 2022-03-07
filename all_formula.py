"""
A simple example that uses the NOMAD client library to access the archive.

Modified from source: https://nomad-lab.eu/prod/rae/docs/archive.html#first-example
to download all chemical formulas `chemical_composition_reduced` along with their calculation ids `calc_id` and `total_energy`.
"""
import pandas as pd
from tqdm import tqdm
from nomad.client import ArchiveQuery

# exclude noble gases and certain radioactive elements, source: https://github.com/sparks-baird/mat_discover/blob/4e65b710b948c7ce269cc1741c12e219507aa2dd/mat_discover/utils/generate_elasticity_data.py#L74-L76
# fmt: off
excluded_elements = [
    "He", "Ne", "Ar", "Kr", "Xe", "Rn", "U", "Th", "Rn", "Tc", "Po", "Pu", "Pa",
    ]
# fmt: on

# %% query NOMAD database
query = ArchiveQuery(
    # url="http://nomad-lab.eu/prod/rae/api",
    query={"$and": {"domain": "dft", "$not": {"atoms": excluded_elements}}},
    required={
        # "section_run": {
        #    "section_single_configuration_calculation[-1]": {"energy_total": "*",},
        #    "section_system": {"chemical_composition_reduced": "*"},
        # },
        "section_metadata": {"calc_id": "*", "formula": "*"},
    },
    per_page=3000,
    max=None,
)

print(query)

# %% extract values
# initialize
calc_ids = []
formulas = []
for i, result in enumerate(tqdm(query)):
    if result.section_metadata is not None:
        # Checking if nested attribute exists https://stackoverflow.com/a/29855744/13697228
        calc_ids.append(result.section_metadata.calc_id)
        formulas.append(result.section_metadata.formula)
    else:
        calc_ids.append(None)
        formulas.append(None)

# %% combine and save
df = pd.DataFrame(
    {
        "calc_id": calc_ids,
        "formula": formulas,
        # "hartree_total_energy": hartree_total_energies,
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

# calc_ids = [
#     result.section_metadata.calc_id if result.section_metadata is not None else None
#     for result in query
# ]

# formulas = [
#     result.section_metadata.formula if result.section_metadata is not None else None
#     for result in query
# ]

# formulas = [
#    result.section_run[0].section_system[0].chemical_composition_reduced
#    for result in query
# ]

# total_energies = [
#    result.section_run[0].section_single_configuration_calculation[-1].energy_total
#    if len(result.section_run) > 1
#    and len(result.section_run.section_single_configuration_calculation) > 1
#    else None
#    for result in query
# ]

# hartree_total_energies = [
#     total_energy.to(units.hartree).m if total_energy is not None else None
#     for total_energy in total_energies
# ]

# from nomad.metainfo import units
