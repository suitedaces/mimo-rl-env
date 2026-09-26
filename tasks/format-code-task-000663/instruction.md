Provide a way to lookup chart instance given canvas element
### Feature Proposal
Upon instantiation of the Chart, it would be great if a reference to the Chart instance could be tagged to the `HTMLCanvasElement` for later usage, rather than [having to use hacky ways to access them](https://github.com/airblade/chartjs-ror/issues/34#issuecomment-351558852).

### Feature Use Case
I'm looking for a way to reference the instance of one of my charts which is defined in a different JS module to the one I want to reference it in. Exporting the instance doesn't seem to work, and I took a look at @vijayj's [implementation](https://github.com/airblade/chartjs-ror/issues/34#issuecomment-351558852), and it would've worked fine, but I push the Chart instances to the `window.charts` AFTER importing my other JS module, so when I came to access `window.charts`, it's empty until my other JS module is loaded and executed.

ChartJS already adds a `$chartjs` property onto the `HTMLCanvasElement` once instantiated, so it would make sense to add the instance to that property.

## Possible Implementation
### index.html
```html
<canvas id="chart" width="400" height="200"></canvas>
```
### module1.js
```js
const chartEl = document.querySelector('#chart');
new Chart(chartEl, {
  type: 'pie',
  data: {
    labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    datasets: [{
      data: [15, 1, 1, 1, 45, 1],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
      ],
      borderColor: [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 1
    }]
  }
});
```

### module2.js
```js
const chartInstance = document.querySelector('#chart').$chartjs.instance;
chartInstance.getDatasetMeta(0).hidden = true;
chartInstance.update();
```
