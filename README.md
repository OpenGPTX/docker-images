# Docker Images

[![Run pre-commit hooks](https://github.com/OpenGPTX/docker-images/actions/workflows/pre-commit.yaml/badge.svg?branch=main)](https://github.com/OpenGPTX/docker-images/actions/workflows/pre-commit.yaml)
[![Build Jupyter IDE images](https://github.com/OpenGPTX/docker-images/actions/workflows/notebook_ide.yml/badge.svg?branch=main)](https://github.com/OpenGPTX/docker-images/actions/workflows/notebook_ide.yml)
[![Build Spark Images](https://github.com/OpenGPTX/docker-images/actions/workflows/spark.yaml/badge.svg?branch=main)](https://github.com/OpenGPTX/docker-images/actions/workflows/spark.yaml)

The repository contains Notebook IDE images and Spark Kubernetes images.

All the images are public and can be refereced via:

```console
ghcr.io/opengptx/<PATH_TO_FOLDER>:latest
```

or can be found [here](https://github.com/orgs/OpenGPTX/packages?repo_name=docker-images).

The notebook images and docs are heavily inspired by the
[example notebook servers](https://github.com/kubeflow/kubeflow/tree/master/components/example-notebook-servers)
provided by Kubeflow.

## Notebook Servers

### Images // Relationship Chart

The chart shows how the images are related to each other.
![DockerImages](https://user-images.githubusercontent.com/97906975/169824391-494553f0-e3ec-4caa-8332-70f41a6732fd.png)

### Images // Important Information

- images use the [s6-overlay](https://github.com/just-containers/s6-overlay)
  init system to manager process.
- [Multiprocess Containers with Overlays](https://www.tonysm.com/multiprocess-containers-with-s6-overlay/)
- Docker driven datascience environment and workflow
- They all run as the non-root `jovyan` user

### How do I extend these images?

#### Custom Images // Python Packages

> ⚠️ a common cause of errors is users running pip install --user ..., causing
> the home-directory (which is backed by a PVC) to contain a different or
> incompatible version of a package contained in /opt/conda/...

Extend one of the images and install any pip or conda packages your Kubeflow
Notebook users are likely to need.

As a guide, look at [jupyter-spark-scipy](./notebook-servers/jupyter-spark-scipy/Dockerfile#L6)
for a pip install example.

#### Custom Images // Linux Packages

> ⚠️ ensure you swap to root in the Dockerfile before running apt-get, and
> swap back to jovyan after.

Extend one of the images and install any `apt-get` packages your Kubeflow
Notebook users are likely to need.

As a guide, look at [jupyter-spark](./notebook-servers/jupyter-spark/Dockerfile)
for a example.

#### Custom Images // S6

Some use-cases might require custom scripts to run during the startup of the
Notebook Server container, or advanced users might want to add additional
services that run inside the container (for example, an Apache or NGINX
web server). To make this easy, we use the [s6-overlay](https://github.com/just-containers/s6-overlay).

The [s6-overlay](https://github.com/just-containers/s6-overlay) differs from
other init systems like [tini](https://github.com/krallin/tini). While tini
was created to handle a single process running in a container as PID 1,
the s6-overlay is built to manage multiple processes and allows the creator
of the image to determine which process failures should silently restart, and
which should cause the container to exit.

#### Custom Images // S6 // Scripts

Scripts that need to run during the startup of the container can be placed in
`/etc/cont-init.d/`, and are executed in ascending alphanumeric order.

An example of a startup script can be found in [jupyter-scipy](./notebook-servers/jupyter/s6/cont-init.d/02-export-nb_name-namespace).
This script uses the [with-contenv](https://github.com/just-containers/s6-overlay#container-environment)
helper so that environment variables (passed to container) are available in the script.

#### Custom Images // S6 // Run As Root

> ⚠️ our example images run `s6-overlay` as `$NB_USER` (not `root`), meaning
> any files or scripts related to `s6-overlay` must be owned by the `$NB_USER`
> user to successfully run

There may be cases when you need to run a service as root, to do this, you can
change the Dockerfile to have `USER root` at the end, and then use
`s6-setuidgid` to run the user-facing services as `$NB_USER`.

### Troubleshooting

#### Troubleshooting // Jupyter

**Kernel stuck in `connecting` state:**
This is a problem that occurs from time to time and is not a Kubeflow problem,
but rather a browser.
It can be identified by looking in the browser error console, which will show
errors regarding the websocket not connecting. To solve the problem,
please restart your browser or try using a different browser.
