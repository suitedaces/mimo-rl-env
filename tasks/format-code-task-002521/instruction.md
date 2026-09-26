## Installation hub doesn't fit on smaller screens

When running the graphical installer on a smaller display, the main hub
(the screen showing all the configuration spokes) doesn't fit on the
screen anymore. Some of the spokes get pushed off / the layout overflows,
which makes parts of the hub hard or impossible to reach without scrolling
or resizing.

This started being noticeable after the "Connect to Red Hat" spoke was
added — the System column on the hub now has one extra entry compared to
the other columns, which seems to be what's tipping the overall layout
over the edge on smaller resolutions.

Could the placement of the Connect to Red Hat spoke on the hub be
reconsidered so the hub layout fits on smaller screens again? The other
columns have more room to spare, so moving it shouldn't be a problem
visually.

Resolves: rhbz#1845493
