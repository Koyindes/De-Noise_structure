import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sets = ["P", "H", "S", "G", "E"]
nsets = len(sets)

df = {}
counts = {}
for set in sets:
    df[set] = pd.read_csv("../data/5set/"+set+".csv")
    counts[set] = len(df[set])
    
from venn import venn

materials = {}
for set in sets:
    materials[set] = {mp_id for mp_id in df[set]["mp_id"].values}

venn(materials).plot()

venn(materials).get_figure().savefig("venn.pdf")
