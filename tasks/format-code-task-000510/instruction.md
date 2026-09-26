Option to apply user classnames
It would be a very nice feature to allow us to set our own class names on the resulting iframe. Right now it is hardcoded to a static value:
https://github.com/awslabs/amazon-quicksight-embedding-sdk/blob/79bdce13d916ed906d22c198720ca13a42fdb0bd/src/EmbeddableDashboard.js#L139

Maybe something like this?
```js
    QuickSightEmbedding.embedDashboard({
      url,
      container,
      scrolling: 'no',
      height: 'AutoFit',
      loadingHeight: '400px',
      className: 'my-apps-classname', // <-----
    }).on('error', this.handleError);
```

For example, this could be used to apply bootstrap class names to the iframe itself to change the border or shadow, without having to duplicate framework features in custom css.
