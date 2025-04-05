import os
import mbuild as mb
import gmso
import hoomd
import unyt as u

from gmso.external import to_hoomd_snapshot, to_hoomd_forcefield
from gmso.external import from_mbuild
from gmso.parameterization import apply
from gmso.core.forcefield import ForceField


def build_system():
    print("Building system...")
    # Add your script here
    print(mol_file)
    methane = mb.load(methane.mol2)
    box = mb.fill_box(
            compound=methane,
            n_compounds=50,
            density=600,
            seed=24
    )
    box_top = from_mbuild(compound=box)
    box_top.identify_connections()
    oplsaa = ForceField("oplsaa")
    typed_box = apply(top=box_top, forcefields=oplsaa)
    print("Finished building system...")
    print("------------------------------------")
    return typed_box


typed_system = build_system()

base_units = {"mass": u.g / u.mol, "length": u.nm, "energy": u.kJ / u.mol}
snapshot, units = to_hoomd_snapshot(typed_system, base_units=base_units)
hoomd_force_dict, units = to_hoomd_forcefield(
        typed_system, r_cut=1.5, base_units=base_units
)
hoomd_forces = []
for force_type in hoomd_force_dict:
    for force in hoomd_force_dict[force_type]:
        hoomd_forces.append(force)

sim = hoomd.Simulation(device=hoomd.device.GPU(), seed=job.sp.seed)
sim.create_state_from_snapshot(snapshot)
integrator = hoomd.md.Integrator(dt=0.0001)
integrator.forces = hoomd_forces

temp = job.sp.temp * u.K
kT = temp.to_equivalent("kJ/mol", "thermal").value
job.doc.kT = kT
thermostat = hoomd.md.methods.thermostats.MTTK(kT=kT, tau=1.0)
nvt = hoomd.md.methods.ConstantVolume(
    thermostat=thermostat, filter=hoomd.filter.All()
)
integrator.methods.append(nvt)
sim.operations.integrator = integrator
sim.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=kT)
thermodynamic_properties = hoomd.md.compute.ThermodynamicQuantities(
    filter=hoomd.filter.All()
)

sim.operations.computes.append(thermodynamic_properties)

print("Starting simulation...")
sim.run(int(5e6))
print("Finished simulation...")
print("------------------------------------")
