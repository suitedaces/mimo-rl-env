Don't close MLflow run context when training model
**Is your feature request related to a problem? Please describe.**
Currently I am using MLflow projects to run a python script that trains a model using ludwig. I would like to set the experiment name and model name to the one I pass via CLI parameters. At the same time the model name should also be the run's name in mlflow and the experiment names should match as well. The MlflowCallback seems to currently end mlflow runs if not called through hyperopt. Therefore it is not possible to let ludwig log to a run started before calling the train method. 

This is the current version of `train.py`:
```python
import mlflow
from ludwig.api import LudwigModel
from ludwig.contribs.mlflow import MlflowCallback
import pandas as pd
import pathlib
import click


@click.command()
@click.option("--data_path", help="Path to data", type=click.Path(exists=True))
@click.option(
    "--model_config_path",
    help="Path to model config",
    type=click.Path(exists=True),
)
@click.option(
    "--output_path", help="Path to save trained model", type=click.Path()
)
@click.option(
    "--model_name",
    help="Name of the model",
    type=click.STRING,
)
@click.option(
    "--experiment_name",
    help="Name of the experiment",
    type=click.STRING,
)
def train(
    data_path, model_config_path, output_path, model_name, experiment_name
):
    """Train model"""

    data_path = pathlib.Path(data_path)
    output_path = pathlib.Path(output_path)

    # load data
    df = pd.read_csv(data_path)

    # create model with mlflow callback
    # will log metrics, artifacts, and model
    model = LudwigModel(
        config=model_config_path,
        logging_level=30,
        callbacks=[MlflowCallback()],
    )
    # train model
    _, _, output_dir = model.train(
        dataset=df,
        experiment_name=experiment_name,
        model_name=model_name,
        output_directory=output_path,
    )

if __name__ == "__main__":
    train()
```

And the call I want to make is:
`mlflow run -e train -P data_path=data/train.csv -P model_config_path=config/model_config.yaml -P model_name=test -P experiment_name=titanic .`

The result should be a run with name "test" under experiment with name "titanic" containing the logs by the MlflowCallback.

**Describe the use case**
A user wants to define custom experiment and run names when using the MlflowCallback.

**Describe the solution you'd like**
A way to make it possible for the user to start a run and let the MlflowCallback log to that run. Might be enough to remove the `mlflow.end_run()` call when no experiment_id is set yet.

**Describe alternatives you've considered**
I could define experiment name and model/run name as CLI parameters to the entrypoint as well as to mlflow. That's a little ugly because it would mean writing both two times. 
E.g. `mlflow run -e train -P model_name=titanic -P experiment_name=test --run-name titanic --experiment-name test`.
I also tried a partial workaround where I set the mlflow.runName tag after using LudwigModel.train() of the last active run (`mlflow.last_active_run()`). This does not work for the experiment_name, though.
