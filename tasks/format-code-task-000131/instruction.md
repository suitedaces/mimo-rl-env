## SLES hosts aren't being recognized as a known OS

We have a mixed Linux fleet managed through Katello — RHEL, CentOS, Fedora, and a chunk of SUSE Linux Enterprise Server boxes. The Red Hat / CentOS / Fedora ones get their OS picked up correctly, but for the SLES hosts the OS comes back as nothing — Katello doesn't seem to map the distribution name reported by the subscription consumer to anything at all, so they end up without a proper OS assignment.

Expected: SLES (and SUSE Linux Enterprise in general, since the distribution name reported can vary a bit) should be a recognized OS just like RHEL / CentOS / Fedora are. Could support for it be added?
