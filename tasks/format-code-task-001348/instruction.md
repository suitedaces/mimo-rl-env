Support for explicitly setting the latest release
GitHub recently changed the way the latest version can be managed, to allow explicitly setting the latest release. Previously, the latest release would be the most recently created non-pre-release.

https://github.blog/changelog/2022-10-21-explicitly-set-the-latest-release/

In the web UI, this shows up as two checkboxes. In the API, this is set using the `make_latest` parameter, which defaults to `true` for newly created releases.

https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28#update-a-release

It does not seem that this parameter is available in the `RepositoryRelease` struct yet.

https://github.com/google/go-github/blob/153bbc2620f5693e42fb1ae5b80d86c611bc6727/github/repos_releases.go#L21-L29

My sample workflow is to attempt to promote an existing pre-release to the latest release. For example, given a set of releases for a repository:

```
TITLE      TYPE         TAG NAME   PUBLISHED
Release-4  Pre-release  Release-4  about 16 minutes ago
Release-3  Pre-release  Release-3  about 17 minutes ago
Release-2  Latest       Release-2  about 17 minutes ago
Release-1               Release-1  about 17 minutes ago
```

Removing the pre-release flag from Release-4:

```go
githubClient.Repositories.EditRelease(context.Background(),
	owner, repo, *release.ID,
	&github.RepositoryRelease{Prerelease: github.Bool(false)})
```

This results in,

```
TITLE      TYPE         TAG NAME   PUBLISHED
Release-4               Release-4  about 19 minutes ago
Release-3  Pre-release  Release-3  about 19 minutes ago
Release-2  Latest       Release-2  about 19 minutes ago
Release-1               Release-1  about 19 minutes ago
```

It would be useful if this were possible:

```go
githubClient.Repositories.EditRelease(context.Background(),
    owner, repo, *release.ID,
    &github.RepositoryRelease{
        Prerelease: github.Bool(false),
        Makelatest: "true", // string, because parameter supports "true", "false", "legacy"
    })
```
