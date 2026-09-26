PyDMSpinBox always takes limits from PV even when user defined limits are set
The PyDMSpinBox will always set the maximum and minimum values to display based on the HOPR/LOPR fields of the PV:

https://github.com/slaclab/pydm/blob/1dd59b9d8a700926c774ca27e522e843a5302164/pydm/widgets/spinbox.py#L159-L175

This happens even if the user sets their own limits in designer. And in the case HOPR/LOPR are not defined then it will set minimum and maximum both to zero so that the spinbox cannot display anything other than zero.

We should create an option that is surfaced in designer for taking limits from the PV only if the user wants this behavior. Should keep this option consistent with other widgets as per #577
