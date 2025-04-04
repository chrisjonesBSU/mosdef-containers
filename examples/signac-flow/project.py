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
    from gmso.external import (
            from_mbuild,
            to_gsd_snapshot,
            to_hoomd_forcefield
    )
    with job:
        print("JOB ID NUMBER:")
        print(job.id)
        print("------------------------------------")
        # Add your script here
        methane = mb.load("C", smiles=True)
        box = mb.fill_box(
                compound=methane,
                n_compounds=job.sp.num_molecules,
                density=job.sp.density
        )
        box_top = from_mbuild(compound=box)
        box_top.identify_connections()
        return box_top


@MyProject.pre(hoomd_simulation)
@MyProject.post(sim_done)
@MyProject.operation(
        directives={"ngpu": 1, "executable": "python -u"}, name="run_hoomd"
)
def run_hoomd(job):
    with job:
        pass

        job.doc.sim_done = True

@MyProject.pre(lammps_simulation)
@MyProject.post(sim_done)
@MyProject.operation(
        directives={"ngpu": 1, "executable": "python -u"}, name="run_lammps"
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
