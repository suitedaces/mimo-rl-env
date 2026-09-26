# Problem Statement

我这边用 HAP-python 起了个配件，display_name 里如果前后有空格、横杠，或者像 `💡 Reading` 这种名字，Home app 经常搜不到；把名字改成很普通的英文之后又能发现，感觉像是 mDNS 广播出来的名字/hostname 有问题。

# Expected outcomes

- mDNS advertising should remain on the HomeKit service type `_hap._tcp.local.`, and display names that are unsafe for mDNS or hostnames, including the kinds of names described above, should still produce discoverable advertised service information.
- The advertised mDNS service instance name should be derived from the accessory display name in a cleaned form, while preserving the existing uniqueness suffix.
- The advertised server hostname for the accessory should be a valid `.local.` hostname derived from the display name and the existing uniqueness suffix.
- Package metadata should require `zeroconf>=0.32.0`.
- The README installation guidance should state that, as of version 3.5.1, HAP-python no longer supports Python versions older than 3.6.

# Implementation notes

The exact normalization helpers, data structures, and where validation is applied are up to the implementation. Preserve the existing public behavior of accessory registration except for making the advertised mDNS service information valid for these display-name edge cases and updating the documented dependency/support metadata above.
