# MoSDeF Containers
Docker containers for the Molecular Simulation Design Framework (MoSDeF)

Docker containers can be pulled from [DockerHub](https://hub.docker.com/repository/docker/chrisjonesbsu/mosdef-containers/general).


## Quick Examples

### Using Docker
<img src=".images/docker.png" width="150" style="margin-right: 100px"/>  &nbsp; &nbsp; <img src=".images/podman.png" width="150"/>
If you want to use these containers on a personal computer (as opposed to a compute cluster), using Docker or an equivalent would be best.

[Docker Install](https://docs.docker.com/engine/install) **|** [Docker Get Started](https://www.docker.com/get-started/) **|** [Podman Install](https://podman.io/docs/installation) **|** [Podman Get Started](https://podman.io/get-started)

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


### Using apptainer and/or singularity
<img src=".images/apptainer.svg" width=300/>

[Apptainer](https://apptainer.org/) (formely Singularity) will allow use of these containers in high-performance computer clusters.
Using these containers for scientific research ensures you are following best practices for reproducibility.

Apptainer is often available as a module on computer clusters and can be used to pull and run Docker containers.

**Pull the container from DockerHub and use it to run a python file**
```bash
module load apptainer/1.2.5
apptainer pull mosdef_hoomd_gpu.sif docker://chrisjonesbsu/mosdef-containers:mosdef_hoomd_gpu-2025-04-03
apptainer exec --nv mosdef_hoomd_gpu.sif python hoomd_simulation.py
```

