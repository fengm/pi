
OMNIDRIVER_HOME=/home/mfeng/local/lib/optics/OmniDriver

JAVA_HOME=$(OMNIDRIVER_HOME)/_jvm
OOI_HOME=$(OMNIDRIVER_HOME)/OOI_HOME
JDK_INCLUDE_FILE_ROOT=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.0.x86_64
LD_LIBRARY_PATH=$(OOI_HOME):$(OMNIDRIVER_HOME)/_jvm/lib/amd64/server
JVM_ROOT=$(OMNIDRIVER_HOME)/_jvm

CC=gcc
CFLAGS=-Wall -Wunused -DLINUX -fpic -I$(JDK_INCLUDE_FILE_ROOT)/include -I$(JDK_INCLUDE_FILE_ROOT)/include/linux -I$(OMNIDRIVER_HOME)/include
GFLAGS=-g

all: compile link

compile:
	$(CC) $(CFLAGS) -c hs_sensor.c hs_sensor_wrap.c -I/usr/include/python2.7

link:
	$(CC) -shared *.o -o _hs_sensor.so -lcommon -lOmniDriver -L$(JVM_ROOT)/lib/amd64/server -ljvm  -L$(OMNIDRIVER_HOME)/OOI_HOME 
