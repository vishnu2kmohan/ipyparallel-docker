FROM vishnumohan/jupyter-notebook

MAINTAINER Vishnu Mohan <vishnu@mesosphere.com>

USER root

# Add the Mesosphere repo
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF \
    && DISTRO=debian \
    && CODENAME=jessie \
    && echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" \
       > /etc/apt/sources.list.d/mesosphere.list \
    && apt-get update -yq --fix-missing \
    && apt-get install -yq --no-install-recommends \
       openjdk-7-jre-headless \
       mesos \
    && apt-get clean

USER conda
# There are no py35 conda packages for spark and py4j - create a py34 conda env
RUN conda config --add channels anaconda-cluster \
    && conda create -yq -n py34 python=3.4 anaconda \
    && conda install -yq -c anaconda-cluster -n py34 \
       py4j \
       scala \
       spark \
    && conda install -yq -n py34 \
       cloudpickle \
       ipyparallel \
       seaborn \
    && conda clean -yt \
    && conda clean -yp \
    && bash -c 'source activate py34 && pip install -q -U httpie hdfs pywebhdfs' \
    && bash -c 'source activate py34 && ipython profile create --parallel'

EXPOSE 8888
WORKDIR ${CONDA_USER_HOME}/work
ENTRYPOINT ["tini", "--"]
CMD ["notebook.sh"]

# Add local files as late as possible to stay cache friendly
COPY notebook.sh /usr/local/bin/
COPY jupyter_notebook_config.py ${CONDA_USER_HOME}/.jupyter/
COPY upload_ctrl_conf_hdfs.py /usr/local/bin/
COPY download_ctrl_conf_hdfs.py /usr/local/bin/
COPY ipcontroller_config.py ${CONDA_USER_HOME}/.ipython/profile_default/
COPY ipengine_config.py ${CONDA_USER_HOME}/.ipython/profile_default/
