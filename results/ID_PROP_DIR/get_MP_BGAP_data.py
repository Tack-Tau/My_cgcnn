#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import pickle
import numpy as np
from mp_api.client import MPRester

MP_API_KEY=os.environ.get("MP_API_KEY")
'''
For M-B-C Peroskite (ABX3) band gap ML Data Querying

'''

with MPRester(MP_API_KEY) as mpr:

    formula_list = ["**O3"]
    '''
    formula_list = ["**O3", "**F3", "**Cl3", "**Br3",
                    "**I3", "**S3", "**Se3", "**Te3", "**N3", "**P3"]
    '''

    mpid_bgap_dict = []

    for formula in formula_list:

        docs = mpr.materials.summary.search(
            # formula = "**O3",
            # elements = ["H", "B", "C", "N", "Si", "P", "Ge", "Al"],
            # exclude_elements = ["O"],
            formula = formula,
            # spacegroup_number = [2, 11, 12, 15, 59, 62, 63, 68, 71, 74, 99, 127, 139, 140, 221],
            fields = ["material_id", "is_metal", "is_gap_direct", "band_gap", "formula_pretty",
                      "calc_types"]
        )

        for doc in docs:
            mat_id = str(doc.material_id)
            chem_form = str(doc.formula_pretty)
            metality = int(bool(doc.is_metal))
            direct_or_not = int(bool(doc.is_gap_direct))
            e_gap_val = float(doc.band_gap)

            if e_gap_val is not None:

                struct_id = chem_form + '_' + str(mat_id)
                mpid_bgap_dict.append( {"Structure ID": struct_id,
                                        # "Metality": metality,
                                        # "Direct or not": direct_or_not,
                                        "Gap value (eV)": e_gap_val } )
                struct = mpr.get_structure_by_material_id(mat_id)
                # struct.to(struct_id + '.vasp', fmt='POSCAR')
                struct.to(struct_id + '.cif', fmt='CIF', significant_figures=4)
                # struct.to(struct_id + '.cif', fmt='CIF', significant_figures=4, symprec=1.0E-9, angle_tolerance=0.5, refine_struct=True)

    # field_names = ["Structure ID", "Metality", "Direct or not", "Gap value (eV)"]
    field_names = ["Structure ID", "Gap value (eV)"]

    with open('id_prop.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        # writer.writeheader()
        writer.writerows(mpid_bgap_dict)

