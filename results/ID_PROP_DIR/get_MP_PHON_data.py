#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import pickle
import numpy as np
from mp_api.client import MPRester

MP_API_KEY=os.environ.get("MP_API_KEY")
'''
For M-B-C type PHDOS stable/unstable ML Data Querying
elements = ["H", "B", "C", "N", "Si", "P", "Ge", "Al"]
'''

with MPRester(MP_API_KEY) as mpr:

    chemsys_list = ["*-*", "*-*-*",]

    mpid_pdos_dict = []

    for item in chemsys_list:

        docs = mpr.materials.summary.search(
            # formula = "**O3",
            # elements = ["H", "B", "C", "N", "Si", "P", "Ge", "Al"],
            chemsys=[item],
            # exclude_elements = ["O"],
            fields = ["material_id", "energy_above_hull", "formula_pretty", "calc_types"]
        )

        for doc in docs:
            mat_id = str(doc.material_id)
            chem_form = str(doc.formula_pretty)
            e_above_hull = float(doc.energy_above_hull)
            ph_dos = mpr.get_phonon_dos_by_material_id(doc.material_id)

            if ph_dos is not None:

                ph_freq = ph_dos.frequencies
                min_freq = min(ph_freq)

                if np.allclose(e_above_hull, 0.0, rtol=1e-05, atol=1e-08):
                    is_stable = 1.0
                else:
                    if min_freq > -1.0:
                        is_stable = 1.0
                    else:
                        is_stable = 0.0
                struct_id = chem_form + '_' + str(mat_id)
                mpid_pdos_dict.append( {"Structure ID": struct_id,
                                        # "Energy Above Hull": e_above_hull,
                                        "Phonon Stability": is_stable} )
                struct = mpr.get_structure_by_material_id(mat_id)
                # struct.to(struct_id + '.vasp', fmt='POSCAR')
                struct.to(struct_id + '.cif', fmt='CIF', significant_figures=4)
                # struct.to(struct_id + '.cif', fmt='CIF', significant_figures=4, symprec=1.0E-9, angle_tolerance=0.5, refine_struct=True)

    # field_names = ["Structure ID", "Energy Above Hull", "Phonon Stability"]
    field_names = ["Structure ID", "Phonon Stability"]

    with open('id_prop.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        # writer.writeheader()
        writer.writerows(mpid_pdos_dict)

