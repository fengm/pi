

all: compile

compile:
	swig -python hs_sensor.i
	g++ -c *c -I/usr/include/python2.7 -I/home/mfeng/local/lib/high_op/src/seabreeze/include
	ld -shared -lseabreeze -lusb *.o -o _hs_sensor.so -L/home/mfeng/local/lib/high_op/src/seabreeze/lib -L/usr/lib
	
clean:
	rm -f *.o *.so *.pyc *_wrap.c
	
