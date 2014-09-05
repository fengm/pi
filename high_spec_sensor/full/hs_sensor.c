
#include <stdio.h>

#include <Wrapper.h>
#include <ArrayTypes.h>
#include <ContinuousStrobeImpl.h>
#include <JString.h>

WRAPPER_T	wrapperHandle;

int s_init(){
	JSTRING apiVersion;
	int		buildNumber;
	JSTRING serialNumber;
	JSTRING spectrometerName;
	JSTRING firmwareVersion;
	int		numberOfSpectrometersAttached; // actually attached and talking to us
	int		spectrometerIndex; // 0-n, identifies which spectrometer we are interacting with

	printf("\nCSpectrumTest_Linux 1.00\n");
	printf("language: C/C++\n");
	printf("OmniDriver interface type: \"C\"\n");
	printf("API demonstrated: Wrapper\n");
	
	wrapperHandle = Wrapper_Create();

	buildNumber = Wrapper_getBuildNumber(wrapperHandle);
	/* printf("build number = %d\n",buildNumber); */

	apiVersion = JString_Create();
	Wrapper_getApiVersion(wrapperHandle,apiVersion);
	/* printf("api version = %s\n",JString_getASCII(apiVersion)); */
	JString_Destroy(apiVersion);

	// The following call will populate an internal array of spectrometer objects 
	numberOfSpectrometersAttached = Wrapper_openAllSpectrometers(wrapperHandle);
	/* printf("number of spectrometers found = %d\n",numberOfSpectrometersAttached); */
	if (numberOfSpectrometersAttached == 0)
		return 0; // there are no attached spectrometers
	
	// We will arbitrarily use the first attached spectrometer
	spectrometerIndex = 0;

	// Display some information about this spectrometer
	firmwareVersion = JString_Create();
	serialNumber = JString_Create();
	spectrometerName = JString_Create();
	Wrapper_getSerialNumber(wrapperHandle,spectrometerIndex,serialNumber);
	Wrapper_getName(wrapperHandle,spectrometerIndex,spectrometerName);
	Wrapper_getFirmwareVersion(wrapperHandle,spectrometerIndex,firmwareVersion);
	/* printf("spectrometer type: %s   serial number: %s  firmware version: %s\n", */
	/* 	JString_getASCII(spectrometerName), */
	/* 	JString_getASCII(serialNumber), */
	/* 	JString_getASCII(firmwareVersion)); */
	JString_Destroy(firmwareVersion);
	JString_Destroy(serialNumber);
	JString_Destroy(spectrometerName);

	return 0;
}

int s_read(double* vals, double* refs){
	int		index;
	int		minimumAllowedIntegrationTime; // units: microseconds
	int		numberOfPixels;
	int		spectrometerIndex; // 0-n, identifies which spectrometer we are interacting with
	DOUBLEARRAY_T spectrumArrayHandle;
	double* spectrumValues;
	DOUBLEARRAY_T wavelengthArrayHandle;
	double	wavelengthIntercept;
	double	wavelengthCoefficient1;
	double	wavelengthCoefficient2;
	double	wavelengthCoefficient3;
	double* wavelengthValues;

	spectrometerIndex = 0;

	// Demonstrate how to obtain and display wavelength coefficients
	wavelengthIntercept = Wrapper_getWavelengthIntercept(wrapperHandle,spectrometerIndex);
	wavelengthCoefficient1 = Wrapper_getWavelengthFirst(wrapperHandle,spectrometerIndex);
	wavelengthCoefficient2 = Wrapper_getWavelengthSecond(wrapperHandle,spectrometerIndex);
	wavelengthCoefficient3 = Wrapper_getWavelengthThird(wrapperHandle,spectrometerIndex);
	/* printf("wavelength intercept = %1.4f  1st: %1.4f  2nd: %1.4f  3rd: %1.4f\n", */
	/* 	wavelengthIntercept, */
	/* 	wavelengthCoefficient1,wavelengthCoefficient2,wavelengthCoefficient3); */

	// Set some acquisition parameters
	minimumAllowedIntegrationTime = Wrapper_getMinimumIntegrationTime(wrapperHandle,spectrometerIndex);
	Wrapper_setIntegrationTime(wrapperHandle,spectrometerIndex,minimumAllowedIntegrationTime);
	Wrapper_setBoxcarWidth(wrapperHandle,spectrometerIndex,0);
	Wrapper_setScansToAverage(wrapperHandle,spectrometerIndex,1);
	Wrapper_setCorrectForElectricalDark(wrapperHandle,spectrometerIndex,0);

	// Aquire a spectrum
	/* printf ("\nPress <enter> to get a spectrum from this spectrometer\n"); */
	/* getchar(); */

	spectrumArrayHandle = DoubleArray_Create();
	Wrapper_getSpectrum(wrapperHandle,spectrometerIndex,spectrumArrayHandle);
	spectrumValues = DoubleArray_getDoubleValues(spectrumArrayHandle);
	numberOfPixels = DoubleArray_getLength(spectrumArrayHandle);

	wavelengthArrayHandle = (DOUBLEARRAY_T)DoubleArray_Create();
	Wrapper_getWavelengths(wrapperHandle,spectrometerIndex,wavelengthArrayHandle);
	wavelengthValues = DoubleArray_getDoubleValues(wavelengthArrayHandle);

	// Loop to print the spectral data to the screen
	for (index = 0; index<numberOfPixels; index++)
	{
		vals[index] = spectrumValues[index];
		refs[index] = wavelengthValues[index];
		/* printf("pixel %4d = %5.2f  wavelength(nm): %1.2f\n",index,spectrumValues[index],wavelengthValues[index]); */
	}

	DoubleArray_Destroy(spectrumArrayHandle);
	DoubleArray_Destroy(wavelengthArrayHandle);

	return numberOfPixels;
}

void s_close(){
	// Clean up
	Wrapper_closeAllSpectrometers(wrapperHandle);
	Wrapper_Destroy(wrapperHandle);
}
