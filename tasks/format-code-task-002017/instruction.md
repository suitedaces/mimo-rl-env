[UX] Shape & Points selection status remains visible when another layer is selected
When you draw a shape then it become selected when you finish (as of 0.5.0, https://github.com/napari/napari/pull/6640). This is great, because then you can change the Shape color, etc.
If you then switch the layer selection to an Image or Labels layer, the Shape continues to display the "selected" visual, even though it **cannot be interacted with**:
<img width="1198" alt="image" src="https://github.com/user-attachments/assets/b471d551-6fa6-4123-820c-dce9cb578e71">

I feel like this is misleading and can result in stray painting or whatnot if the user tries to interact with the Shape without the Shapes layer selected.
Ideally, the selection visual would drop if a different layer is selected, but, importantly, return when the Shapes layer is re-selected.

Note in 0.4.19 shapes were not selected after drawing, so this potentially confusing effect didn't occur.
Edit: And in 0.4.19 if you manually select a shape and switch to a different layer it becomes de-selected. However, it is not be re-selected upon switching back to the Shapes layer.

Edit2: I reverted https://github.com/napari/napari/pull/6640 locally and Shapes are no longer selected on completion, but if you manually select a shape and change layers the selection visual still persists, so it must be related to a different PR.

Edit3: Selection of Points also persists visually when changing to a different layer type.
