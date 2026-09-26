We ran into a problem retrieving Kafka CloudWatch vlaues. This happens on the `master` branch as well as with all the `v0.26.*-alpha` versions.

Using this `config.yml`:

```yaml
discovery:
  jobs:
    - type: kafka
      regions:
        - us-east-1
      metrics:
        - name: BytesOutPerSec
          statistics:
          - Average
          period: 600
          length: 600
          addCloudwatchTimestamp: true
```
We get this error:

```sh
{"level":"info","msg":"Parse config..","time":"2021-04-16T10:29:21+02:00"}
{"level":"info","msg":"Startup completed","time":"2021-04-16T10:29:21+02:00"}
panic: assignment to entry in nil map

goroutine 20 [running]:
github.com/ivx/yet-another-cloudwatch-exporter/pkg.getFilteredMetricDatas(0xc0002badb0, 0x9, 0xc000100508, 0xc0002bad98, 0x5, 0x0, 0x0, 0x0, 0x0, 0x25d2648, ...)
	/Users/<user>/projects/yet-another-cloudwatch-exporter/pkg/aws_cloudwatch.go:313 +0x2fc
github.com/ivx/yet-another-cloudwatch-exporter/pkg.getMetricDataForQueries(0xc000442c60, 0xc000338e00, 0xc0002badb0, 0x9, 0xc000100508, 0x0, 0x1f2ecb8, 0xc00028c078, 0xc0000100b8, 0x1, ...)
	/Users/<user>/projects/yet-another-cloudwatch-exporter/pkg/abstract.go:176 +0x2b1
github.com/ivx/yet-another-cloudwatch-exporter/pkg.scrapeDiscoveryJobUsingMetricData(0xc000442c60, 0xc0002badb0, 0x9, 0xc000100508, 0x0, 0x1f2c4d0, 0xc00028c0c0, 0x1f2f8c0, 0xc00028c170, 0x1f2fee0, ...)
	/Users/<user>/projects/yet-another-cloudwatch-exporter/pkg/abstract.go:201 +0x245
github.com/ivx/yet-another-cloudwatch-exporter/pkg.scrapeAwsData.func1(0xc0000dadc0, 0x2604000, 0x0, 0xc00028c0f8, 0x1, 0x1, 0x0, 0x0, 0x0, 0x0, ...)
	/Users/<user>/projects/yet-another-cloudwatch-exporter/pkg/abstract.go:47 +0x425
created by github.com/ivx/yet-another-cloudwatch-exporter/pkg.scrapeAwsData
	/Users/<user>/projects/yet-another-cloudwatch-exporter/pkg/abstract.go:26 +0x39d
```

To investigate we added some logging statements and found a mismatch in the `dimensionName` that leads to the `nil` in `dimensionsFilter[names[i]]`. See below, it is `Cluster_Name` vs. `Cluster Name`:

```sh
{"level":"info","msg":"names:  [Cluster_Name]  dimensionsFilter:  map[Cluster Name:map[]]","time":"2021-04-16T11:29:10+02:00"}
panic: assignment to entry in nil map
```

It seems to work when commenting out [this line](https://github.com/ivx/yet-another-cloudwatch-exporter/blob/81f4cb1153f4f14ad7f17b65d5269d4507091e31/pkg/aws_cloudwatch.go#L302) here: `dimensionName = strings.ReplaceAll(dimensionName, "_", " ")`.

We don't know why this line was added (not a Go expert 🙈 ), maybe someone knows? If the line can be dropped I'd be happy to make a PR for it.
