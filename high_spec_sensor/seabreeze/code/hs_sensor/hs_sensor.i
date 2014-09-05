/* eass.i */

%include "carrays.i"
%array_class(double, farray);

%module hs_sensor
%{
    extern int init(int val);
    extern int read(int len, double vals[], double refs[]);
    extern void close();
%}

extern int init(int val);
extern int read(int len, double vals[], double refs[]);
extern void close();
