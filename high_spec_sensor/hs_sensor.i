/* eass.i */

%include "carrays.i"
%array_class(double, farray);

%module hs_sensor
%{
    extern int s_init();
    extern int s_read(double vals[], double refs[]);
    extern void s_close();
%}

extern int s_init();
extern int s_read(double vals[], double refs[]);
extern void s_close();
