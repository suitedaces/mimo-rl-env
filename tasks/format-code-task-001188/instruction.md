## Linux host re-enrolled from Windows still shows old Windows MDM status on the hosts page

We re-image machines occasionally — sometimes a workstation that used to run Windows gets wiped and reinstalled with Ubuntu, then re-enrolled into Fleet via fleetd. The host record itself updates fine: it shows up in the hosts list with the new Linux platform as expected.

The problem is the MDM info on that host. Before the re-image, the host was enrolled as a Windows host and had Windows MDM details associated with it on its host page. After re-imaging to Ubuntu and re-enrolling, those Windows MDM details are still being shown for that host. That doesn't really make sense — the machine isn't running Windows anymore, Linux doesn't have MDM in the same sense, and the stale info is misleading for whoever is auditing the fleet.

### What I'd expect

When a host that was previously enrolled as Windows comes back enrolled as a non-Windows OS (Linux in our case), Fleet shouldn't keep showing the previous Windows MDM information for it on the hosts page. The host has effectively changed OS as far as Fleet sees it; the old MDM state from the prior OS shouldn't carry over.

We do also have a couple of dual-boot test machines that go back and forth, so it'd be good if a host that later re-enrolls as Windows again can have its Windows MDM info show up normally — it's specifically the case where the host is no longer Windows that's currently confusing.

### To reproduce

1. Enroll a Windows host into Fleet so it appears with Windows MDM info on the hosts page.
2. Wipe that machine and install Ubuntu (or another Linux distro).
3. Install fleetd on the new Linux install and let it enroll. The same host record is reused (same hardware), and the platform updates to Linux.
4. Open that host on the hosts page — Windows MDM information from before the re-image is still displayed.
