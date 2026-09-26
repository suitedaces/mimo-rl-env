## Django test runner: way to write all test output into a single XML file

I'm using the Django test runner from `xmlrunner.extra.djangotestrunner` to produce JUnit-style XML for our CI. With `TEST_OUTPUT_DIR` pointed at a directory the runner works fine, but it drops **one XML file per test module/class** into that directory.

The problem is that pretty much every JUnit consumer I've integrated with (Jenkins, GitLab CI, etc.) wants a **single** report file at a known path, e.g. `reports/junit.xml`. Right now I either have to post-process the output directory and merge the XML files by hand, or point the CI at a glob and hope it picks everything up — neither is great, and it makes the Django integration noticeably less convenient than just running `xmlrunner` directly on a non-Django project, where you can already aim it at one file.

Could the Django runner grow an option that says "put all of the test output into this one file" instead of fanning out per class? The existing directory-based behaviour should obviously keep working for projects that already depend on it — this would just be an alternative for people who want the single-file mode.

To stay consistent with the existing `TEST_OUTPUT_DIR` / `TEST_OUTPUT_DESCRIPTIONS` settings, something like a `TEST_OUTPUT_FILE_NAME` setting would probably be the natural place to opt in.
