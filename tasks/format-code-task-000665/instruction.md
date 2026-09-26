## `chocolatey_package` still shells out to `choco list` even with `use_choco_list false`

After rolling Chef 18 out across our Windows fleet, chef-client runs got noticeably slower on nodes that use a lot of `chocolatey_package` resources. Querying installed package versions through `choco list` is the expensive part, and the resource has a `use_choco_list` property exactly so we can opt out of that and let the provider read versions from the local chocolatey lib directory instead.

I set `use_choco_list false` on our packages (and we don't set `Chef::Config[:always_use_choco_list]`), expecting the provider to use the on-disk fast path. Run times didn't improve at all — when I watch what chef is doing on a node, it's still invoking `choco list` to determine currently-installed versions for every chocolatey_package resource. Toggling `use_choco_list` true vs. false makes no observable difference.

Reproducer (any Windows node with chocolatey installed):

```ruby
chocolatey_package 'git' do
  action :install
  use_choco_list false
end
```

Expected: with `use_choco_list false` and no global override, the provider determines installed versions by inspecting the local chocolatey package directory, not by shelling out to `choco list`.

Actual: `choco list` is invoked anyway, and the run is just as slow as it was before the property existed. Setting the property to `true` produces the same behavior, which is what tipped me off that the selection logic between the two code paths isn't doing what its name says.

This looks like a regression — the on-disk path was the whole point of `use_choco_list false` for us, and right now there's no way to actually reach it.
