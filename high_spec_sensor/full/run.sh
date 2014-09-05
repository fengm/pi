#!/bin/sh

export OMNIDRIVER_HOME=/home/mfeng/local/lib/optics/OmniDriver

export JAVA_HOME=$OMNIDRIVER_HOME/_jvm
export OOI_HOME=$OMNIDRIVER_HOME/OOI_HOME
export JDK_INCLUDE_FILE_ROOT=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.0.x86_64
export LD_LIBRARY_PATH=$OOI_HOME:$OMNIDRIVER_HOME/_jvm/lib/amd64/server
export JVM_ROOT=$OMNIDRIVER_HOME/_jvm
source /home/mfeng/local/.bashrc_mine

python read_hs_sensor.py -o output

