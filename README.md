# mosdef-containers
Containers for the Molecular Simulation Design Framework (MoSDeF)

Docker containers cann be pulled from [here](https://hub.docker.com/repository/docker/chrisjonesbsu/mosdef-containers/general).


## Quick Examples

### Using Docker
If you want to use these containers on a personal computer (as opposed to a compute cluster), using Docker or an equivalent would be best.

- [Docker installation instrucitons](https://docs.docker.com/engine/install) || [Getting started with Docker](https://www.docker.com/get-started/) 

<img src="https://icon.icepanel.io/Technology/svg/Podman.svg" width="30" height="30" style="vertical-align: middle;"/> [Podman Install](https://podman.io/docs/installation) | [Podman Get Started](https://podman.io/get-started) 

<span style="display: inline-flex; align-items: center; gap: 0.4em;">
  <img src="https://icon.icepanel.io/Technology/svg/Podman.svg" width="20" height="20" />
  <span>
    <a href="https://podman.io/docs/installation">Podman installation instructions</a> ||
    <a href="https://podman.io/get-started">Getting started with Podman</a>
  </span>
</span>

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
Apptainer will allow use of these containers in high-performance computer clusters.
Using these containers for scientific research ensures you are following best practices for reproducibility.

[Apptainer](https://apptainer.org/) is often available as a module 
