__author__ = 'CTK'


def save_mol2(traj, step=-1, filename='mbuild.mol2'):
    """Output a Trajectory as a TRIPOS mol2 file.

    Args:
        traj (md.Trajectory): The Trajectory to be output.
        filename (str, optional): Path of the output file.

    """
    bond_list = list()
    if len(traj.top._bonds) > 0:
        for bond_n, bond in enumerate(traj.top.bonds):
            bond_list.append("{0} {1} {2} 1\n".format(
                    bond_n + 1, bond[0].index + 1, bond[1].index + 1))

        n_bonds = bond_n + 1
    else:
        n_bonds = 0

    with open(filename, 'w') as mol2_file:
        mol2_file.write("@<TRIPOS>MOLECULE\n")
        mol2_file.write("Generated by mBuild\n")
        mol2_file.write("{0} {1} 0 0 0\n".format(traj.n_atoms, n_bonds))
        mol2_file.write("SMALL\n")
        mol2_file.write("NO_CHARGES\n")
        mol2_file.write("\n")

        mol2_file.write("@<TRIPOS>ATOM\n")
        for atom in traj.top.atoms:
            x, y, z = traj.xyz[step][atom.index]
            mol2_file.write("{0:d} {1:s} {2:8.4f} {3:8.4f} {4:8.4f} {5} {6:d} {7:s} {8:8.4f}\n".format(
                    atom.index + 1, atom.name, float(x), float(y), float(z), atom.name,
                    atom.residue.index + 1, atom.residue, 0.0))
        if bond_list:
            mol2_file.write("@<TRIPOS>BOND\n")
            for entry in bond_list:
                mol2_file.write(entry)
        mol2_file.write("<@TRIPOS>\n")

if __name__ == "__main__":
    from mbuild.examples.ethane.ethane import Ethane
    ethane = Ethane()
    ethane = ethane.to_trajectory()
    save_mol2(ethane, filename='ethane.mol2')

