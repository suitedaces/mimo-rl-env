## Plugin in `vendor/` directory gets removed during update

We hit this while trying to run plugin updates on a cloud instance.

In our setup we have a few plugins that we pull in directly via `composer require` — they live in `vendor/` and not under `custom/plugins` or `custom/static-plugins`. They're managed entirely through composer in the project's root `composer.json`, which is by design for our deployment.

During a plugin update run, one of these (in our case the Rufus plugin) ends up getting removed via composer as part of the update process. After the update finishes, the package is gone from `vendor/` and the system is broken.

From a user perspective, a plugin that was installed straight through composer and lives only in `vendor/` shouldn't be touched / removed by Shopware's plugin update flow at all — it isn't something the shop owner installed via the plugin manager into `custom/`, it's a project-level composer dependency. Only plugins that are actually located under the `custom/` plugin directories should be subject to that kind of composer remove behavior during updates.

Could the plugin lifecycle take the plugin's location into account here so that vendor-only, composer-managed plugins are left alone during updates?
