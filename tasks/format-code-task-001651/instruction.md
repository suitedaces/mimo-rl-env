I've been profiling my urh-based app and noticed the memory keeps climbing every time I open and close a bunch of spectrum/signal views. The scene-manager objects appear to keep resources alive after the views are no longer needed. Could there be a clean way to fully release what a scene manager owns when I'm tearing it down? Also it'd be nice if a freshly created `SceneManager` didn't already pretend it has plot data when nothing's been loaded yet — right now `plot_data` is some dummy array instead of just being empty.

Expected outcomes:
- Freshly constructed `SceneManager` instances should represent “no loaded plot data” with `plot_data` set to `None`, rather than pre-populating placeholder samples.
- Scene manager objects should provide an explicit teardown method named `eliminate()` that leaves the manager in a released state, so resources it owns are no longer retained after teardown.
- `FFTSceneManager` and `SignalSceneManager` should participate in the same teardown contract, including resources owned by those subclasses.
- A manager that has already been torn down should remain safe for cleanup-related calls that may still occur during normal view shutdown.

Implementation notes:
- The exact cleanup sequence and internal organization are up to the implementation, as long as the public scene-manager objects no longer retain their owned resources after teardown.
- Keep the behavior compatible with normal Qt/graphics-scene lifecycle expectations; tests should verify final object state and safe method calls rather than a particular helper structure, call chain, or controller/CI-side change.
