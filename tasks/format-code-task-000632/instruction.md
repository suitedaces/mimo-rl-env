[custom] Add `width` property for `CustomMetricGroup`
### Discussed in https://github.com/cdklabs/cdk-monitoring-constructs/discussions/450

<div type='discussions-op-text'>

<sup>Originally posted by **ericxinzhang** November  2, 2023</sup>
My code looks as following. I can specify `height` in `CustomMonitoringProps`. I am wondering why `CustomMetricGroup` does not have a `width` property?

I understand that for high level APIs (e.g. `monitor<ResourceType>`) it's easier for the library to calculate width dynamically. However for `CustomMetricGroup` may we have a `width` property?


```Javascript
const monitoring = new MonitoringFacade(this, 'MyDashboard');

monitoring.monitorCustom({
  height: 5,
  humanReadableName: 'API',
  metricGroups: [
    {
        title: 'API Errors',
        // I wish I could specify `width` here
        graphWidgetLegend: cw.LegendPosition.RIGHT,
        metrics:[
          new cloudwatch.Metric({...}),
          new cloudwatch.Metric({...}),
       ],
    },
    {
        title: 'API Latency',
        graphWidgetLegend: cw.LegendPosition.RIGHT,
        metrics:[
          new cloudwatch.Metric({...}),
          new cloudwatch.Metric({...}),
       ],
    }
  ],
});
```</div>
