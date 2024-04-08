# Use the latest Python 3 docker image
FROM freesurfer/freesurfer:7.4.1 as base
 
# Setup environment for Docker image
ENV HOME=/root/
ENV FLYWHEEL="/flywheel/v0"
WORKDIR $FLYWHEEL
RUN mkdir -p $FLYWHEEL/input

# Copy the contents of the directory the Dockerfile is into the working directory of the to be container
COPY ./ $FLYWHEEL/
COPY license.txt /usr/local/freesurfer/.license

# Install Dev dependencies (conda, jq, poetry, flywheel installed in base)
#RUN software-properties-common=0.96.20.2-2 && yum install --no-install-recommends -y

RUN yum update -y  && \
    yum clean all && \
    yum update -y && yum install jq -y && \
    yum install -y python3 && yum install -y python3-pip && \
    yum install -y unzip gzip wget && \
    pip3 install flywheel-gear-toolkit && \
    pip3 install flywheel-sdk && \
    pip3 install jsonschema && \
    pip3 install pandas  && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# setup fs env
ENV PATH /usr/local/freesurfer/bin:/usr/local/freesurfer/fsfast/bin:/usr/local/freesurfer/tktools:/usr/local/freesurfer/mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV FREESURFER_HOME /usr/local/freesurfer
ENV FREESURFER /usr/local/freesurfer

# Configure entrypoint
RUN bash -c 'chmod +rx $FLYWHEEL/run.py' && \
    bash -c 'chmod +rx $FLYWHEEL/app/'
ENTRYPOINT ["python","/flywheel/v0/main.sh"] 
# Flywheel reads the config command over this entrypoint