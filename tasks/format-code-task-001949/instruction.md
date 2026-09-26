[BUG] EpochsTFR.save not saving metadata
Just realized that EpochsTFR.save doesn't save metadata so if you save and reload the function you'll lose the metadata, event, and event_id information. I missed this when I updated EpochsTFR to include metadata. The problem arises when writing to the Hard Disk, `mne.time_frequency._prepare_write_tfr()` hardcodes what attributes to save into a dict, so that when I added new attributes, they didn't get saved. I think I can fix this by doing something like

`attributes = vars(epochsTF)`

with a few other adjustments.

If others agree, I can make a quick PR on this
