Add a single_spectrum keyword to extract_region
Right now if you use `extract_region` on a multi-section spectral region, it splits the spectrum into separate distinct `Spectrum1D` objects for each sub-region. This is problematic for some workflows, for example when trying to do line fitting or similar operations on discontinuous spectral features (@camipacifici may have a more concrete example).

So I propose we add a keyword to `extract_region` that allows it to return a *single* spectrum for the multi sub-region case.  This could be just `return_single_spectrum` which would default to False but when True when trigger the discussion above.  But that's kind of a long keyword name.  Any other ideas?
