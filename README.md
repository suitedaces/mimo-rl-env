# MiMo code tasks in Harbor

This repo contains Harbor tasks for all 2,698 rows of the [MiMo-V2.6-RL-oss `code/train` split](https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss/viewer/code/train). Each task under [`tasks/`](tasks/) uses its source instruction, test patch, test command, working directory, and published Linux amd64 image pinned by digest. The dataset provides prebuilt images and test patches, but no original Dockerfiles or solutions.

The earlier pilot, [`format-code-task-001457`](tasks/format-code-task-001457/), remains extended beyond the source row: it also checks the shipped `dist/index.js` bundle and action metadata without a `secrets` input. Its `solution/solve.sh` is a separately authored Oracle check. The other 2,697 tasks preserve the source verifier without this pilot addition.

The [Harbor skill](.agents/skills/harbor/SKILL.md) contains the user-provided documentation index and a local snapshot of all 74 linked official Markdown pages. The source [MiMo dataset card](https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss) declares Apache-2.0; the tasks retain source provenance in each `source.json`.

## Run tasks

Harbor 0.22.0 and Docker are needed. The published images are Linux amd64, so Docker on Apple silicon must support amd64 emulation. A no-op run checks an environment and verifier path; reward 0 is expected when the source task needs a code change. Select a task with `-i`, or omit `-i` to run the whole dataset.

With Colima on macOS, use a job output directory under `/Users` (the default `jobs/` in this repo works). A `/tmp` output directory did not return verifier reward files through Colima's bind mount during these runs.

```bash
harbor run -p tasks -i format-code-task-001457 -a nop -e docker -n 1
harbor run -p tasks -i format-code-task-001457 -a oracle -e docker -n 1
```

To evaluate a coding agent, replace `nop` with that agent and provide its model and credentials according to the [Harbor run-job docs](https://docs.harborframework.com/core-concepts/jobs/run-a-job).

For Codex with an existing ChatGPT OAuth login on the host, the installed Harbor Codex agent can pass `~/.codex/auth.json` into the container. On Apple silicon, an isolated 16 GiB Colima profile with Rosetta can run the Linux amd64 images while leaving the default Docker context alone:

```bash
colima start --profile mimo-rl --cpus 6 --memory 16 --disk 40 \
  --vm-type vz --vz-rosetta --activate=false
codex login status
DOCKER_HOST="unix://$HOME/.colima/mimo-rl/docker.sock" \
CODEX_FORCE_AUTH_JSON=1 harbor run -p tasks -i format-code-task-001457 \
  -a codex -m openai/gpt-6-sol -e docker -n 1 \
  --agent-kwarg version=0.157.1 \
  -o "$HOME/harbor-jobs"
harbor view "$HOME/harbor-jobs" -p 8088
```

Codex CLI 0.157.1 starts a code mode host that reached about 8.5 GB resident memory and was killed in the original 11 GiB Colima VM. Disabling that host made its tools fail closed. CLI 0.118.0 has regular shell tools but the service rejected `gpt-6-sol` through ChatGPT OAuth for that older client. The isolated profile gives the current CLI more memory without stopping the other local containers.

The corrected local run on 2026-09-25 scored 1.0 with zero exceptions using Codex 0.157.1, GPT-6 Sol, and ChatGPT OAuth. Harbor's verifier passed the source row's 28 Jest tests and the pilot's action metadata and `dist/index.js` checks. Its [local viewer page](http://127.0.0.1:8088/jobs/2026-09-25__21-01-06/tasks/tasks/codex/openai/gpt-6-sol/format-code-task-001457/trials/format-code-task-001457__qEf4epc) shows the trajectory and verifier output.

## Regenerate the dataset

The source split is pinned to dataset revision `639865fd3374018d6cb29b9fb82dd531406fcf5f`. Download its Parquet file and install `pyarrow` for the converter. The image repository is documented in the [dataset card](https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss). The checked-in [image audit](reports/code-image-audit.json) and [platform metadata](reports/code-image-metadata.json) cover every source ID and supply the immutable digests.

```bash
curl -L -o /tmp/mimo-code.parquet 'https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss/resolve/639865fd3374018d6cb29b9fb82dd531406fcf5f/code.parquet?download=true'
python3 scripts/convert_code_split.py \
  --parquet /tmp/mimo-code.parquet \
  --expected-sha256 e15733cf2451cfbc5492a4120f7f8cfddbad818aa9f0b324c79888dd1fece161 \
  --image-audit reports/code-image-audit.json \
  --image-metadata reports/code-image-metadata.json \
  --image-repo xiaomimimo/mimo-v2.6-rl-oss \
  --source-revision 639865fd3374018d6cb29b9fb82dd531406fcf5f \
  --output-root tasks
```

The converter checks the Parquet hash, every patch's parseability, and each Linux amd64 digest against the registry audit and Docker Hub platform metadata. It preserves existing tasks only when their source provenance and image match, so rerunning it keeps the pilot's extra verifier. Each generated `environment/Dockerfile` starts from the source image digest. Harbor builds that Dockerfile and uploads the source test patch under `tests/` for verification after the agent runs. `source.json` records the dataset revision, row offset, and hashes.

Run `scripts/validate_code_split.py` with the same source, audit, metadata, revision, and repository flags plus `--task-root tasks` to compare every generated folder with its source row. On 2026-09-25, all 2,698 folders, Dockerfiles, and patches passed that check; Harbor 0.22.0 discovered and parsed all 2,698 task definitions and found all verifier scripts. Rerunning the converter created zero tasks and verified all 2,698 existing ones.

Registry checks resolved all 2,698 image manifests and confirmed Linux amd64 platform metadata. Three representative images were pulled and started directly. Harbor no-op jobs completed with zero exceptions for [`format-code-task-001305`](tasks/format-code-task-001305/) (`/workspace/repo`), [`format-code-task-000989`](tasks/format-code-task-000989/) (the unusual plain unified patch), and [`format-code-task-001871`](tasks/format-code-task-001871/) (both `base` and `new` test commands). Each recorded reward 0 because the no-op agent made no code change. The [local viewer](http://127.0.0.1:8088) has these jobs. The registry reports 6.07 TiB of image sizes before shared layers, so the per-image registry checks are distinct from a full pull and execution of all images.

The converter writes the source-equivalent task. The checked-in pilot extends its verifier and instruction to require the shipped bundle, because this GitHub Action runs `dist/index.js`. The pinned upstream image fails a plain `npm run build` with `ERR_OSSL_EVP_UNSUPPORTED`. The pilot Dockerfile sets `NODE_OPTIONS=--openssl-legacy-provider` so the existing `@zeit/ncc` build command works; this is a Harbor environment adjustment, not a field from the dataset.
