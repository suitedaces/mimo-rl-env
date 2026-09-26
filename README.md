# MiMo code tasks in Harbor

This repository contains Harbor tasks for all 2,698 rows of the [MiMo-V2.6-RL-oss `code/train` split](https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss/viewer/code/train). Each directory under [`tasks/`](tasks/) preserves its source instruction, test patch, test command, and working directory. Its Dockerfile uses the published Linux amd64 image pinned by digest. The source dataset provides prebuilt images and tests, but no original Dockerfiles or solutions.

The [Harbor skill](.agents/skills/harbor/SKILL.md) includes a snapshot of 74 official documentation pages. The [source dataset card](https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss) declares Apache-2.0; each task records its source revision and hashes in `source.json`.

## Run with Docker Desktop

Install Harbor 0.22.0 and start Docker Desktop. On macOS, select its Docker context, then confirm the engine is available:

```bash
open -a Docker
docker context use desktop-linux
docker info --format '{{.Name}} {{.Architecture}}'
```

From the repository root, run one task and inspect the result:

```bash
harbor run -p tasks -i format-code-task-001305 -a nop -e docker -n 1 -o "$PWD/jobs"
harbor view "$PWD/jobs" -p 8088
```

`nop` makes no code change, so reward 0 is expected for this task. The image is Linux amd64; Docker Desktop on Apple silicon runs it through its amd64 support. Select another task with `-i`. To run an agent, use the [Harbor run-job docs](https://docs.harborframework.com/core-concepts/jobs/run-a-job) for its agent and model options.

## Regenerate and validate

The source split is pinned to revision `639865fd3374018d6cb29b9fb82dd531406fcf5f`. Install `pyarrow`, download the Parquet file, and run the batch converter. The checked-in [image audit](reports/code-image-audit.json) and [platform metadata](reports/code-image-metadata.json) provide the verified image digests.

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

The converter verifies the Parquet hash, parses every test patch, checks each Linux amd64 image digest, and writes task folders. Run `scripts/validate_code_split.py` with the same source and audit arguments plus `--task-root tasks` to compare all generated tasks with their source rows. Harbor discovers and parses all 2,698 tasks. Registry checks resolved all 2,698 image manifests; this does not imply that all images were individually pulled and run.
