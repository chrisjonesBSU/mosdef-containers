"""Define the project's workflow logic and operation functions.

Execute this script directly from the command line, to view your project's
status, execute operations and submit them to a cluster. See also:

    $ python src/project.py --help
"""
import signac
from flow import FlowProject, directives
from flow.environment import DefaultSlurmEnvironment
import os


class MyProject(FlowProject):
    pass


class Borah(DefaultSlurmEnvironment):
    """Borah is a HPC at Boise State University."""
    hostname_pattern = "borah"
    template = "borah.sh"

    @classmethod
    def add_args(cls, parser):
        parser.add_argument(
            "--partition",
            default="shortgpu",
            help="Specify the partition to submit to."
        )


class Fry(DefaultSlurmEnvironment):
    """Fry is the HPC used by the CME Lab at Boise State University."""
    hostname_pattern = "fry"
    template = "fry.sh"

    @classmethod
    def add_args(cls, parser):
        parser.add_argument(
            "--partition",
            default="batch",
            help="Specify the partition to submit to."
        )


class Falcon(DefaultSlurmEnvironment):
    hostname_pattern = "ondemand"
    template = "falcon.sh"

    @classmethod
    def add_args(cls, parser):
        parser.add_argument(
            "--partition",
            default="batch",
            help="Specify the partition to submit to."
        )


# Definition of project-related labels (classification)
@MyProject.label
def sim_done(job):
    return job.doc.sim_done


@MyProject.label
def sample_done(job):
    return job.doc.sample_done


@MyProject.label
def hoomd_simulation(job):
    return job.sp.engine.lower() == "hoomd"


@MyProject.label
def lammps_simulation(job):
    return job.sp.engine.lower() == "lammps"


def build_system(job):
    import mbuild as mb
    import gmso
    from gmso.external import from_mbuild
    from gmso.core.forcefield import ForceField
    from gmso.parameterization import apply

    with job:
        print("Building system...")
        # Add your script here
        methane = mb.load("C", smiles=True)
        box = mb.fill_box(
                compound=methane,
                n_compounds=job.sp.num_molecules,
                density=job.sp.density,
                seed=job.sp.seed
        )
        box_top = from_mbuild(compound=box)
        box_top.identify_connections()
        oplsaa = ForceField("oplsaa")
        typed_box = apply(top=box_top, forcefields=oplsaa)
        print("Finished building system...")
        print("------------------------------------")
        return typed_box


@MyProject.pre(hoomd_simulation)
@MyProject.post(sim_done)
@MyProject.operation(
        directives={
            "ngpu": 1, "executable": "apptainer exec --nv $MOSDEF_IMG python"
        },
        name="run_hoomd"
)
def run_hoomd(job):
    import hoomd
    import unyt as u

    from gmso.external import to_gsd_snapshot, to_hoomd_forcefield

    with job:
        typed_system = build_system(job)
        base_units = {"mass": u.g / u.mol, "length": u.nm, "energy": u.kJ / u.mol}
        snapshot, units = to_gsd_snapshot(typed_system, base_units=base_units)
        hoomd_force_dict, units = to_hoomd_forcefield(typed_system, r_cut=1.5, base_units=base_units)
        hoomd_forces = []
        for force_type in hoomd_force_dict:
            for force in hoomd_force_dict[force_type]:
                hoomd_forces.append(force)

        sim = hoomd.Simulation(device=hoomd.device.GPU(), seed=job.sp.seed)
        sim.create_state_from_snapshot(snapshot)
        integrator = hoomd.md.Integrator(dt=0.0001)
        integrator.forces = hoomd_forces

        temp = job.doc.temp * u.K
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
        sim.run(job.doc.n_steps)
        print("Finished simulation...")
        print("------------------------------------")

        job.doc.sim_done = True

@MyProject.pre(lammps_simulation)
@MyProject.post(sim_done)
@MyProject.operation(
        directives={
            "ngpu": 1, "executable": "apptainer exec --nv $MOSDEF_IMG python"
        },
        name="run_lammps"
)
def run_lammps(job):
    with job:
        pass
        job.doc.sim_done = True


@MyProject.pre(sim_done)
@MyProject.post(sample_done)
@MyProject.operation(
        directives={"ngpu": 0, "executable": "python -u"}, name="sample"
)
def sample(job):
    # Add package imports here
    with job:
        print("JOB ID NUMBER:")
        print(job.id)
        print("------------------------------------")
        # Add your script here


if __name__ == "__main__":
    MyProject().main()
