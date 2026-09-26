## Opening a broken BPMN file gives no error feedback

If I try to open a BPMN file that's malformed (e.g. it got corrupted on disk, or I hand-edited the XML and accidentally broke it), Camunda Modeler doesn't tell me anything went wrong. The tab opens, the loading spinner shows up, and then... that's it. It just sits in the loading state and never finishes — no dialog, no message, nothing to suggest the file failed to parse.

From the user side, this is pretty confusing: I can't tell whether the modeler is just slow, frozen, or whether the file itself is the problem.

I'd expect that when a diagram can't be opened, the modeler surfaces a proper error dialog so I know the file is broken, instead of leaving me staring at an indefinite loading state.
