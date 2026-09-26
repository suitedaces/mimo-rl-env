> ## Documentation Index
> Fetch the complete documentation index at: https://docs.harborframework.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Create a Dataset

> Create a dataset of Harbor tasks

## Implicit datasets

The simplest way to create a dataset is to collocate a group of tasks in a directory.

```bash theme={"system"}
my-dataset/
├── task1/
├── task2/
└── task3/
```

which can be run with:

```bash theme={"system"}
harbor run -p ./my-dataset -a "<agent>" -m "<model>"
```

## Explicit datasets

You may want to define multiple datasets containing overlapping tasks. For example, you may have a directory of tasks defining an implicit dataset that you want to subset into categories.

In this case, copying and pasting the tasks is inconvenient, inefficient, and adds maintenance overhead.

Instead, you should create a `dataset.toml` manifest, which contains pointers to the task directories.

### Create a `dataset.toml` manifest

To create a `dataset.toml` manifest, run

```bash theme={"system"}
harbor dataset init "<org/name>"
```

which outputs a `dataset.toml` manifest in the current directory.

<Note>
  Usually, `<org>` is the name of your company and `<name>` is the name of the dataset.
</Note>

### Add and remove tasks

To add tasks to the dataset, run

```bash theme={"system"}
harbor dataset add "<task-dir>"
```

To remove tasks from the dataset, run

```bash theme={"system"}
harbor dataset remove "<task-dir>"
```

You can also add and remove all tasks from another dataset

```bash theme={"system"}
harbor dataset add "<other-dataset.toml>"
harbor dataset remove "<other-dataset.toml>"
```

### Run the `dataset.toml`

To run the `dataset.toml` manifest, run

```bash theme={"system"}
harbor run -p "<path-to-dataset.toml>"
```

## Publish a dataset

To share your dataset with team members or publicly using Harbor Hub, run

```bash theme={"system"}
harbor publish "<org/name>"
```

Think of Harbor Hub like PyPI or NPM rather than GitHub. Because tasks are software, development typically happens in a version-controlled repository and versions are published to Harbor Hub.

Once a dataset is published, anyone with access can run it using the `harbor run -d <org/name>` command.
