import numpy as np

def latexSIString(value, error, numErrDigits=1):
    """
    Return a value and its error in a format compatible with the siunitx latex package.

    Parameters
    ----------
    value : float or int

    error : float or int, must be +ve and smaller than |value| 
        The error on value

    numErrDigits : int, must be greater than 0
        The number of digits to which the error should be given. 
        This determines the number of significant digits in the answer
    """

    value = float(value)
    error = float(error)
    
    def getMantissaAndExponent(num):
        
        if num < 0:
            num = -num

            if num < 1:
                exponent = int(np.log10(num))-1
                mantissa = num/(10**exponent)
                mantissa = -mantissa
            else:
                exponent = int(np.log10(num))
                mantissa = num/(10**exponent)
                mantissa = -mantissa

        elif num > 0:
            if num < 1:
                exponent = int(np.log10(num))-1
                mantissa = num/(10**exponent)
            else:
                exponent = int(np.log10(num))
                mantissa = num/(10**exponent)
        else:
            exponent = 0
            mantissa = num/(10**exponent)

        return mantissa, exponent

    errMantissa, errExponent = getMantissaAndExponent(error)

    # have to handle some cases separately (when rounding changes exponent)
    if numErrDigits == 1:
        upperLimitingCase = 9.5
    else: 
        upperLimitingCase = float("9.".ljust(numErrDigits+1, "9") + "5")

    if errMantissa >= upperLimitingCase:
        roundedErrMantissa = 1.
        errExponent += 1
    else:
        roundedErrMantissa = round(errMantissa, numErrDigits-1)

    # getting the error digits as a string with no decimal place
    if numErrDigits == 1:
        errDigitsString = str(roundedErrMantissa)[0]
    else:
        errDigitsString = str(roundedErrMantissa).replace(".", "")

    errDigitsString = errDigitsString.ljust(numErrDigits, "0")

    # now work out mantissa and exponent for the actual value
    mantissa, exponent = getMantissaAndExponent(value)
    roundedMantissa = round(mantissa, exponent-errExponent+numErrDigits-1)
    roundedMantissaString = str(roundedMantissa).ljust(exponent-errExponent+numErrDigits+1, "0")

    if len(roundedMantissaString) == 2:# stops it returning a single digit followed by a decimal point
        roundedMantissaString = roundedMantissaString[0]
    
    if exponent == 0:# no need for an E if exponent is 0
        return roundedMantissaString + "(" + errDigitsString + ")"
    else:
        return roundedMantissaString + "(" + errDigitsString + ")" + "E" + str(exponent)




print(latexSIString(456.67, 0.0004534986049860, 1))