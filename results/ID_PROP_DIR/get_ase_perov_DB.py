#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import csv
import ase.db
from ase.atoms import Atoms
from ase.data import atomic_numbers
from ase.build.tools import sort
# from ase.phasediagram import PhaseDiagram

atomic_symbols = {value: key for key, value in atomic_numbers.items()}

con = ase.db.connect('cubic_perovskites.db')
references = [(row.id, row.formula, row.numbers, row.positions, row.cell, row.energy) for row in con.select('standard_energy') ]

struct_id_E_dict = []

for i in range(len(references)):
    id = references[i][0]
    chem_form = references[i][1]
    struct_id = chem_form + '_' + str(id)
    atomic_nums = references[i][2]
    positions = references[i][3]
    cell = references[i][4]
    en_tot = references[i][5]
    en_per_atom = en_tot/len(positions)
    symbols = [atomic_symbols[number] for number in atomic_nums]
    atoms = Atoms(positions=positions, symbols=symbols)
    atoms.set_cell(cell)
    atoms.set_pbc(True)
    sorted_atoms=sort(atoms, tags=atoms.get_chemical_symbols())
    ase.io.write(struct_id+'.vasp', sorted_atoms, direct = True, long_format = True, vasp5 = True)
    struct_id_E_dict.append( {"Structure ID": struct_id, "Total Energy (eV/atom)": en_per_atom} )

field_names = ["Structure ID", "Total Energy (eV/atom)"]

with open('id_prop.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    # writer.writeheader()
    writer.writerows(struct_id_E_dict)
