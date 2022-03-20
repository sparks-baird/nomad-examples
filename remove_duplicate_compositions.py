"""Calculated reduced formulas and remove duplicate compositions.

Might take about an hour to run.
"""
import numpy as np
import pandas as pd
from tqdm import tqdm
from pymatgen.core import Composition

df = pd.read_csv("all-formula.csv")

PARSE = "unparsable"
AVAIL = "unavailable"

# https://stackoverflow.com/questions/46342492/use-dictionary-to-replace-a-string-within-a-string-in-pandas-columns
blank = ""
mapper = {
    "-": blank,
    "(alpha)": blank,
    "beta": blank,
    ",": blank,
    "(amorphous)": blank,
    "/": blank,
    "(anatase)": blank,
    "alpha": blank,
    "(hex)": blank,
    "beta": blank,
}
bad = ["X", "(6H)"]
# df["formula"] = df["formula"].replace(mapper, regex=True) # slow

reduced_formulas = []
bad_formulas = []
factors = []
for i, formula in enumerate(tqdm(df["formula"])):
    if (
        isinstance(formula, str)
        and formula != "unavailable"
        and not np.any([s in formula for s in bad])
    ):
        for key in mapper.keys():
            formula = formula.replace(key, mapper[key])
        try:
            reduced_formula, factor = Composition(
                formula
            ).get_reduced_formula_and_factor()
            reduced_formulas.append(reduced_formula)
            factors.append(factor)
        except Exception:
            print(formula)
            reduced_formulas.append("bad_formula")
            bad_formulas.append(formula)
            factors.append(0)
            pass
    else:
        reduced_formulas.append("unavailable")
        factors.append(0)

df["reduced_formula"] = reduced_formulas
df["factor"] = factors

# keep track of repeated formula calc_id-s and track counts
uniq_df = (
    df.reset_index()
    .groupby(by="reduced_formula")
    .agg({"calc_id": lambda x: tuple(x)})
    .reset_index()
)
uniq_df["count"] = uniq_df["calc_id"].apply(len)

# remove "unavailable" formula and make `calc_id`-s the index
uniq_df = uniq_df[uniq_df["reduced_formula"] != AVAIL]
uniq_df = uniq_df[uniq_df["reduced_formula"] != PARSE]
uniq_df = uniq_df.set_index("calc_id")

uniq_df.to_csv("unique-reduced-formula.csv")

bad_df = pd.DataFrame(dict(bad_formula=bad_formulas))
bad_df.to_csv("bad-formula.csv")
