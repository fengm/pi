
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "util.h"

#include "api/SeaBreezeWrapper.h"

#define MAX_CONSECUTIVE_ERRORS 10
#define MILLISEC_TO_USEC 1000

// global for convenience
const int spec_index = 0;
/* int error_code = 0; */
/* int len = 0; */

void emitError(int errorCode, const char* func) {
    printf("error: \"%s\"=%s\n", func, get_error_string(errorCode));
}

void emitFatal(int errorCode, const char* func) {
    emitError(errorCode, func);
    seabreeze_close_spectrometer(spec_index, &errorCode);
    exit(1);
}

int init(int integ){
    unsigned long integMS = 100;
    if (integ > 0) 
        integMS = integ;

	/* spec_index = 0; */
	/* error_code = 0; */

	int error_code = 0;
    seabreeze_open_spectrometer(spec_index, &error_code);

    if (error_code) 
        emitFatal(error_code, "seabreeze_open_spectrometer(0)");

    int len = seabreeze_get_formatted_spectrum_length(spec_index, &error_code);
    if (error_code) 
        emitFatal(error_code, "seabreeze_get_formatted_spectrum_length");

    seabreeze_set_integration_time_microsec(spec_index, &error_code, integMS * MILLISEC_TO_USEC);
    if (error_code) 
        emitFatal(error_code, "seabreeze_set_integration_time_microsec");

	return len;
}

int read(int len, double* vals, double* refs){
    unsigned bytes = len * sizeof(double);
    double spec[len]; 
    double wavelengths[len]; 
    memset(spec, 0, bytes);
    memset(wavelengths, 0, bytes);

	int error_code = 0;

    seabreeze_get_wavelengths(spec_index, &error_code, wavelengths, len);
    if (error_code)
        emitFatal(error_code, "seabreeze_get_wavelengths");

	seabreeze_get_formatted_spectrum(spec_index, &error_code, spec, len);
	if (error_code) {
		emitError(error_code, "seabreeze_get_formatted_spectrum");
	} else {
		for (unsigned i = 0; i < len; i++) {
			vals[i] = spec[i];
			refs[i] = wavelengths[i];
		}
	}
	return len;
}

void close(){
	int error_code = 0;
    seabreeze_close_spectrometer(spec_index, &error_code);
}
