## `pipeline init` defaults the CodeCommit branch to `master`, but new CodeCommit repos use `main`

I'm trying to set up a Copilot pipeline that's triggered from an AWS CodeCommit repository. My repo is fairly new — when I created it in CodeCommit, the default branch was `main` (which I believe is the current default for new CodeCommit repos).

I ran `copilot pipeline init` from my workspace, picked my CodeCommit repo URL when prompted, and accepted the default branch (i.e. I didn't pass `--git-branch`). When I looked at the generated pipeline manifest, the source branch was set to `master`. After deploying the pipeline, the Source stage points at a branch that doesn't exist in my repo, so the pipeline can't actually pull anything or get triggered by pushes.

If I explicitly pass the branch name it works fine, so this is just about what the default should be when CodeCommit is the source.

Looking at the docs page for the pipeline manifest, it also says:

> The name of the branch in your repository that triggers the pipeline. The default for GitHub is `main`; the default for Bitbucket and CodeCommit is `master`.

So at least for the CodeCommit half of that sentence, the documented default doesn't match what new CodeCommit repos actually use. It would be great if the CodeCommit default in `pipeline init` (and the corresponding docs) were updated to match what users actually get out of CodeCommit today, so things "just work" without having to override the branch every time.
