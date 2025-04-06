# MoSDeF Containers
Docker containers for the [Molecular Simulation Design Framework (MoSDeF)](https://mosdef.org/)

Docker containers can be pulled from [DockerHub](https://hub.docker.com/repository/docker/chrisjonesbsu/mosdef-containers/general).

## Notes
The `mosdef_stable` image provides the complete MoSDeF software stack and its depdencies, but ddoes not include the simulation engines that MoSDeF interfaces with.
We provide images that build on top of `mosdef_stable` and also package a single simulation engine. 

A summary of of the Docker images are as follows:
| Image | Main Software | Notes |
|----------|----------|----------|
| mosdef_stable | mBuild, GMSO, Foyer | Includes the latest conda-forge releases for each package. |
| mosdef_hoomd_gpu | mosdef_stable + Hoomd v5.1 | Compiled for GPU and single-precision. HPMC, DPCD, and MPI are disabled. |
| mosdef_lammps_gpu | mosdef_stable + Lammps | Compiled for GPU and single-precision. Only basic Lammps plugins and features are included. |
| mosdef_gromacs_gpu    | Coming Soon | More |
| mosdef_gomc_gpu    | Coming Soon | More |
| mosdef_cassandra    | Coming Soon | More |

## Quick Examples

### Using Docker
<a href="https://www.docker.com">
  <img src=".images/docker.png" width="100" />
</a>  
&nbsp; &nbsp; 
<a href="https://podman.io/">
  <img src=".images/podman.png" width="80" />
</a>


[Docker Install](https://docs.docker.com/engine/install) **|** [Docker Get Started](https://www.docker.com/get-started/) **|** [Podman Install](https://podman.io/docs/installation) **|** [Podman Get Started](https://podman.io/get-started)

If you want to use these containers on a personal computer (as opposed to a compute cluster), using Docker or an equivalent, such as Podman, would be best.  

**Pull the container from DockerHub**
```bash
docker pull chrisjonesbsu/mosdef-containers:mosdef_stable-2025-04-02
```

**See docker images available locally**
```bash
docker images
```

**Start an interactive shell with the container**
```bash
docker run -it chrisjonesbsu/mosdef-containers:mosdef_stable-2025-04-02
```


### Using apptainer
<img src=".images/apptainer.svg" width=300/>

[Apptainer](https://apptainer.org/) (formely Singularity) will allow use of these containers in high-performance computer clusters.
Using containers for computational scientific research ensures you are following best practices for reproducibility.
Apptainer is often available as a module on computer clusters and can be used to pull and run Docker containers. If you only have Singularity available, the commands should be the same, except replace `apptainer` with `singularity`.

**Pull the container from DockerHub and use it to run a python file**
```bash
module load apptainer/1.2.5
apptainer pull mosdef_hoomd_gpu.sif docker://chrisjonesbsu/mosdef-containers:mosdef_hoomd_gpu-2025-04-03
apptainer exec --nv mosdef_hoomd_gpu.sif python hoomd_simulation.py
```

## More HPC and Research-based Examples 
The above are simple examples to illustrate how to pull and run a command with an image.
More practical and indepth examples are provied in [examples](examples).
These show how to use `apptainer` within a slurm submission script or within a [signac](https://docs.signac.io/en/latest/) project.
The the `README.md` files within the examples for each for more information.
