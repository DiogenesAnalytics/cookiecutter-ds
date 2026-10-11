.PHONY: all build-jupyter jupyter pause address containers list-containers \
        stop-containers restart-containers clear-nb clean shell

# Usage:
# make                    # just alias to containers command
# make build-jupyter      # pull or build the project Docker image
# make jupyter            # startup Docker container running Jupyter server
# make pause              # pause PSECS (to pause between commands)
# make address            # get Docker container address/port
# make containers         # launch all Docker containers
# make list-containers    # list all running containers
# make stop-containers    # simply stops all running Docker containers
# make restart-containers # restart all containers
# make clear-nb           # simply clears Jupyter notebook output
# make clean              # combines all clearing commands into one
# make shell              # create an interactive shell

################################################################################
# GLOBALS                                                                      #
################################################################################

# make cli args
DCTNR := $(notdir $(PWD))
INTDR := notebooks
PSECS := 5

# notebook-related variables
CURRENTDIR := $(PWD)
NOTEBOOKS  := $(shell find ${INTDR} -name "*.ipynb" -not -path "*/.ipynb_*/*")

# docker-related variables
JPTCTNR := jupyter.${DCTNR}
DCKROPT ?=
DCKR_PULL ?= true
DCKR_NOCACHE ?= false
DCKRTTY := $(if $(filter true,$(NOTTY)),-i,-it)
USE_VOL ?= true
JPTRVOL := $(if $(filter true,$(USE_VOL)),-v ${CURRENTDIR}:/home/jovyan,)
DCKRRUN := docker run --rm ${JPTRVOL} ${DCKRTTY} ${DCKROPT}

# Project-specific Docker image
DCKRIMG ?= {{ cookiecutter.docker_image }}

# jupyter nbconvert vars
NBCLER = jupyter nbconvert --clear-output --inplace

# Define the Docker build command with optional --no-cache
define DOCKER_BUILD
	docker build -t $1 . \
	  $(if $(filter true,$(DCKR_NOCACHE)),--no-cache)
endef

# Pull the published image or build it locally
define DOCKER_PULL_OR_BUILD
	$(if $(filter true,$(DCKR_PULL)), \
	  docker pull $1 || (echo "Pull failed. Building Docker image for $1..." && \
	  $(call DOCKER_BUILD,$1)), $(call DOCKER_BUILD,$1))
endef

################################################################################
# COMMANDS                                                                     #
################################################################################

# launch jupyter
all: containers

# Pull or build the project Docker image
build-jupyter:
	@ echo "Preparing project Docker image..."
	@ $(call DOCKER_PULL_OR_BUILD,${DCKRIMG})

# launch jupyter notebook development Docker image
jupyter: build-jupyter
	@ echo "Launching Jupyter in Docker container -> ${JPTCTNR} ..."
	@ if ! docker ps --format={{ "{{.Names}}" }} | grep -q "${JPTCTNR}"; then \
	  docker run -d \
	             --rm \
	             --name ${JPTCTNR} \
	             -e PYTHONPATH=/home/jovyan/src \
	             -e JUPYTER_ENABLE_LAB=yes \
	             -p 8888 \
	             ${JPTRVOL} \
	             ${DCKROPT} \
	             ${DCKRIMG} && \
	  if ! grep -sq "${JPTCTNR}" "${CURRENTDIR}/.running_containers"; then \
	    echo "${JPTCTNR}" >> .running_containers; \
	  fi \
	else \
	  echo "Container already running. Try setting DCTNR manually."; \
	fi

# simply wait for a certain amount of time
pause:
	@ echo "Sleeping ${PSECS} seconds ..."
	@ sleep ${PSECS}

# get containerized server address
address:
	@ if [ -f "${CURRENTDIR}/.running_containers" ]; then \
	while read container; do \
	  if echo "$${container}" | grep -q "${JPTCTNR}" ; then \
	    echo "Server address: $$(docker logs $${container} 2>&1 | \
	          grep http://127.0.0.1 | tail -n 1 | \
	          sed s/:8888/:$$(docker port $${container} | \
	          grep '0.0.0.0:' | awk '{print $$3}' | sed 's/0.0.0.0://g')/g | \
	          tr -d '[:blank:]')"; \
	  else \
	    echo "Could not find running container: ${JPTCTNR}." \
	         "Try running: make list-containers"; \
	  fi \
	done < "${CURRENTDIR}/.running_containers"; \
	else \
	  echo ".running_containers file not found. Is a Docker container running?"; \
	fi

# launch all docker containers
containers: jupyter pause address

# list all running containers
list-containers:
	@ if [ -f "${CURRENTDIR}/.running_containers" ]; then \
	echo "Currently running containers:"; \
	while read container; do \
	  echo "-->  $${container}"; \
	done < "${CURRENTDIR}/.running_containers"; \
	else \
	  echo ".running_containers file not found. Is a Docker container running?"; \
	fi

# stop all containers
stop-containers:
	@ if [ -f "${CURRENTDIR}/.running_containers" ]; then \
	  echo "Stopping Docker containers ..."; \
	  while read container; do \
	    echo "Container $$(docker stop $$container) stopped."; \
	  done < "${CURRENTDIR}/.running_containers"; \
	  rm -f "${CURRENTDIR}/.running_containers"; \
	else \
	  echo "${CURRENTDIR}/.running_containers file not found."; \
	fi

# restart all containers
restart-containers: stop-containers containers

# remove output from executed notebooks
clear-nb: build-jupyter
	@ echo "Removing all output from Jupyter notebooks."
	@ ${DCKRRUN} ${DCKRIMG} ${NBCLER} ${NOTEBOOKS}

# cleanup everything
clean: clear-nb

# create an interactive shell in the project container
shell: build-jupyter
	@ ${DCKRRUN} ${DCKRIMG} bash
