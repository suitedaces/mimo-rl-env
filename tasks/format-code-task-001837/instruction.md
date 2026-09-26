Found by @thomashampson 

### Expected behavior
The new memory widget appears in the top right of the main Workbench window
### Actual behavior
If there was a previously installed version of Workbench, then a layout for the main window has been saved. When the new Memory Usage Widget is added, it takes a full column on the right, whereas we expect it to appear above the Messages box.
### Steps to reproduce the behavior
Install an older version on Mantid (release 6.0 is fine) and a recent nightly which includes the memory widget.

- Open the older version, maybe even move the different toolboxes around on the main window (e.g. drag the algorithms box to the right of the script editor)
- Successfully close the old verison (no segfault) and the layout will be saved (maybe in mantidworkbench.ini)
- Open the recent nightly. Notice how the layout you chose is preserved and that the memory widget is awkwardly added to the end. 
![image (2)](https://user-images.githubusercontent.com/55980573/115520836-778b5400-a282-11eb-8ec6-6dd2512eaf93.png)

- If you select View > Restore Default Layout then it gets put in the correct place.

### Platforms affected
Seen on Windows and IDAaaS, recent nightly.

(Note: as part of the fix, I'd expect a new module-level constant like `SAVE_STATE_VERSION` to be introduced in `workbench.config` and threaded through the relevant `saveState` / `restoreState` calls.)
