#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import numpy as np
from mp_api.client import MPRester

MP_API_KEY=os.environ.get("MP_API_KEY")

matid_list = []

# filename = './' + "matid_list"

with open('id_prop.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    # file = csv.DictReader(csvfile)
    for row in reader:
        struct_id = row[0]
        matid = struct_id.split('_')[1]
        matid_list.append(matid)


with MPRester(MP_API_KEY) as mpr:

    docs = mpr.materials.summary.search(
        material_ids = matid_list,
        fields = ["material_id", "formula_pretty"]
    )

    for doc in docs:

        mat_id = str(doc.material_id)
        chem_form = str(doc.formula_pretty)
        struct_id = chem_form + '_' + str(mat_id)
        struct = mpr.get_structure_by_material_id(mat_id)
        struct.to(struct_id + '.vasp', fmt='POSCAR')
        # struct.to(struct_id + '.cif', fmt='CIF', significant_figures=4)
        # struct.to(struct_id + '.cif', fmt='CIF', significant_figures=4, symprec=1.0E-9, angle_tolerance=0.5, refine_struct=True)
