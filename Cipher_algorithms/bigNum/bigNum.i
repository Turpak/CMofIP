%module bigNum
%{
/* Includes the header in the wrapper code */
#include "bigNum.h"
%}

/* Parse the header file to generate wrappers */
%include "bigNum.h"
