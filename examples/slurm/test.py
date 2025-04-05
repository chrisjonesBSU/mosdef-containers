import hoomd
import mbuild
import gmso
import foyer
import os

cwd = "/bsuhome/cjones/scratch/test-containers/mosdef-containers/examples/slurm"

device = hoomd.device.GPU()
print(device)

comp = mbbuild.Compound(pos=(1,1,1), name="A", mass=1.0)
fpath = os.path.join(cwd, "comp.xyz")
comp.save(fpath)
