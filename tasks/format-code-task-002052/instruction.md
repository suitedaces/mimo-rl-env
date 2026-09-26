Title not handled properly in the `plotting.plot_surf_stat_map` method
<!--Provide a brief description of the bug.-->

In `plotting.plot_surf_stat_map`, passing a title and a given axis (e.g in a subplots case) to the method results in the title being displayed for the subplot only. When passing a title to the `plotting.plot_surf_stat_map` method, the title is being displayed as the title of the overall figure. This results in different subplots with no titles, and a general figure with the title of the last subplot.

<!--Please fill in the following information, to the best of your ability.-->
Nilearn version: main

### Expected behavior

one title per subplot

![image](https://user-images.githubusercontent.com/12402673/162764534-5cf45085-638e-4111-8424-2a9e7d563b1e.png)

### Actual behavior

last title is used as title of the overall figure

![image](https://user-images.githubusercontent.com/12402673/162764621-403f3699-4eff-4e89-9c96-a9c067ef7123.png)

### Solution

The solution is to replace the [figure.suptitle](https://github.com/nilearn/nilearn/blob/0eb1340212c6db5aac07ae31b3061bde5c9f7432/nilearn/plotting/surf_plotting.py#L522) by something similar to [plot_stat_map](https://github.com/nilearn/nilearn/blob/main/nilearn/plotting/img_plotting.py#L213) which is implemented [here](https://github.com/nilearn/nilearn/blob/main/nilearn/plotting/displays/_slicers.py#L162).

I've generated the actual behavior figure by hard coding the following code in the figure.suptitle emplacement:

```python
    if title is not None:
        # Actual version, leading to general title
        # figure.suptitle(title, x=.5, y=.95, fontsize=title_font_size)
        # New version leading to title for each subplot (with hardcoded values)
        x = 0.01
        y = 0.99
        text = title
        size=15
        color="w"
        bgcolor="k"
        axes.text2D(x, y, text,
                transform=axes.transAxes,
                horizontalalignment='left',
                verticalalignment='top',
                size=size, color=color,
                bbox=dict(boxstyle="square,pad=.3",
                          ec=bgcolor, fc=bgcolor, alpha=1),
                zorder=1000)
        axes.set_zorder(1000)
```

### Steps and code to reproduce bug

```python
import matplotlib.pyplot as plt
from nilearn import datasets, plotting, surface

# Fetch mask and motor images
motor_img = datasets.fetch_neurovault_motor_task().images[0]

# Compute a texture example
fsaverage = datasets.fetch_surf_fsaverage()
texture = surface.vol_to_surf(motor_img, fsaverage.pial_right)
texture = texture.clip(0, texture.max())

fig, axes = plt.subplots(nrows=1, ncols=2, subplot_kw={"projection": "3d"})
plotting.plot_surf_stat_map(
    fsaverage.infl_right,
    texture,
    hemi='right',
    title='a subplot',
    colorbar=True,
    threshold=1.,
    axes=axes[0],
    bg_map=fsaverage.sulc_right,
)
plotting.plot_surf_stat_map(
    fsaverage.infl_right,
    texture,
    hemi='right',
    title='an other subplot',
    colorbar=True,
    threshold=1.,
    axes=axes[1],
    bg_map=fsaverage.sulc_right,
)
plotting.show()
```
