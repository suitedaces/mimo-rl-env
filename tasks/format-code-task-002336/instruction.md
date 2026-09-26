bug: `EstimatorReport(SVC())` provides a brier score that fails
### How to reproduce

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from skore import EstimatorReport

X, y = make_classification(random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

report = EstimatorReport(
    SVC(),
    X_train=X_train,
    y_train=y_train,
    X_test=X_test,
    y_test=y_test,
)
```

```
report.metrics.help()
╭─────────────────────────── Available metrics methods ───────────────────────────╮
│ report.metrics                                                                  │
│ ├── .accuracy(...)         (↗︎)     - Compute the accuracy score.                │
│ ├── .brier_score(...)      (↘︎)     - Compute the Brier score.                   │
│ ├── .log_loss(...)         (↘︎)     - Compute the log loss.                      │
│ ├── .precision(...)        (↗︎)     - Compute the precision score.               │
│ ├── .precision_recall(...)         - Plot the precision-recall curve.           │
│ ├── .recall(...)           (↗︎)     - Compute the recall score.                  │
│ ├── .roc(...)                      - Plot the ROC curve.                        │
│ ├── .roc_auc(...)          (↗︎)     - Compute the ROC AUC score.                 │
│ ├── .custom_metric(...)            - Compute a custom metric.                   │
│ └── .report_metrics(...)           - Report a set of metrics for our estimator. │
│                                                                                 │
│                                                                                 │
│ Legend:                                                                         │
│ (↗︎) higher is better (↘︎) lower is better                                        │
╰─────────────────────────────────────────────────────────────────────────────────╯
```
```
report.metrics.brier_score()
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[2], line 1
----> 1 report.metrics.brier_score()

File skore/src/skore/sklearn/_estimator/metrics_accessor.py:872, in _MetricsAccessor.brier_score(self, data_source, X, y)
    818 @available_if(
    819     _check_supported_ml_task(supported_ml_tasks=["binary-classification"])
    820 )
   (...)
    826     y: Optional[ArrayLike] = None,
    827 ) -> float:
    828     """Compute the Brier score.
    829 
    830     Parameters
   (...)
    870     0.03...
    871     """
--> 872     return self._brier_score(
    873         data_source=data_source,
    874         data_source_hash=None,
    875         X=X,
    876         y=y,
    877     )

File skore/skore/src/skore/sklearn/_estimator/metrics_accessor.py:897, in _MetricsAccessor._brier_score(self, data_source, data_source_hash, X, y)
    887 """Private interface of `brier_score` to be able to pass `data_source_hash`.
    888 
    889 `data_source_hash` is either an `int` when we already computed the hash
    890 and are able to pass it around or `None` and thus trigger its computation
    891 in the underlying process.
    892 """
    893 # The Brier score in scikit-learn request `pos_label` to ensure that the
    894 # integral encoding of `y_true` corresponds to the probabilities of the
    895 # `pos_label`. Since we get the predictions with `get_response_method`, we
    896 # can pass any `pos_label`, they will lead to the same result.
--> 897 result = self._compute_metric_scores(
    898     metrics.brier_score_loss,
    899     X=X,
    900     y_true=y,
    901     data_source=data_source,
    902     data_source_hash=data_source_hash,
    903     response_method="predict_proba",
    904     pos_label=self._parent._estimator.classes_[-1],
    905 )
    906 assert isinstance(result, float), (
    907     "The Brier score should be a float, got "
    908     f"{type(result)} with value {result}."
    909 )
    910 return result

File skore/skore/src/skore/sklearn/_estimator/metrics_accessor.py:419, in _MetricsAccessor._compute_metric_scores(self, metric_fn, X, y_true, response_method, data_source, data_source_hash, pos_label, **metric_kwargs)
    416 if "pos_label" in metric_params:
    417     kwargs.update(pos_label=pos_label)
--> 419 y_pred = _get_cached_response_values(
    420     cache=self._parent._cache,
    421     estimator_hash=self._parent._hash,
    422     estimator=self._parent.estimator_,
    423     X=X,
    424     response_method=response_method,
    425     pos_label=pos_label,
    426     data_source=data_source,
    427     data_source_hash=data_source_hash,
    428 )
    430 score = metric_fn(y_true, y_pred, **kwargs)
    432 if isinstance(score, np.ndarray):

File skore/skore/src/skore/sklearn/_base.py:371, in _get_cached_response_values(cache, estimator_hash, estimator, X, response_method, pos_label, data_source, data_source_hash)
    322 def _get_cached_response_values(
    323     *,
    324     cache: dict[tuple[Any, ...], ArrayLike],
   (...)
    331     data_source_hash: Optional[int] = None,
    332 ) -> NDArray:
    333     """Compute or load from local cache the response values.
    334 
    335     Parameters
   (...)
    369         The response values.
    370     """
--> 371     prediction_method = _check_response_method(estimator, response_method).__name__
    372     if prediction_method in ("predict_proba", "decision_function"):
    373         # pos_label is only important in classification and with probabilities
    374         # and decision functions
    375         cache_key: tuple[Any, ...] = (
    376             estimator_hash,
    377             pos_label,
    378             prediction_method,
    379             data_source,
    380         )

File sklearn/utils/validation.py:2283, in _check_response_method(estimator, response_method)
   2281 prediction_method = reduce(lambda x, y: x or y, prediction_method)
   2282 if prediction_method is None:
-> 2283     raise AttributeError(
   2284         f"{estimator.__class__.__name__} has none of the following attributes: "
   2285         f"{', '.join(list_methods)}."
   2286     )
   2288 return prediction_method

AttributeError: SVC has none of the following attributes: predict_proba.
```
