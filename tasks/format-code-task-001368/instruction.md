Translate API usage
#### Environment details

OS: Mac OS 10.12.6
Node.js version: 6.11.0
npm version: 3.10.10
google-cloud-node version: 1.0.0

#### Steps to reproduce

```
const gcloud_translator = require('@google-cloud/translate')({ key: GCLOUD_API_KEY, promise: Promise });

module.exports.translate = (msg, from, to) => {
	// https://googlecloudplatform.github.io/google-cloud-node/#/docs/translate/1.0.0/translate?method=translate
	return gcloud_translator
		.translate(msg, { from, to })
		.then(data => {
			const translation = data[0];
			// const api_response = data[1];

			return Array.isArray(msg) ? arrify(translation) : translation;
		});
};
```

https://github.com/GoogleCloudPlatform/google-cloud-node/blob/translate-1.0.0/packages/translate/src/index.js#L371 and https://github.com/GoogleCloudPlatform/google-cloud-node/blob/translate-1.0.0/packages/translate/src/index.js#L410

This is causing inconsistency in returning messages via the API. For example, 

```
gcloud_translator.translate('Hello world', { from: 'en', to: 'vn' }).then(data => {
  const translation = data[0];

  // translation is a string
})
```

```
gcloud_translator.translate(['Hello world'], { from: 'en', to: 'vn' }).then(data => {
  const translation = data[0];

  // translation is also a string, which is unexpected
})
```

In other case like

```
gcloud_translator.translate(['Hello world', 'How are you doing?'], { from: 'en', to: 'vn' }).then(data => {
  const translation = data[0];

  // translation is an array, which is expected
})
```

I think this line https://github.com/GoogleCloudPlatform/google-cloud-node/blob/translate-1.0.0/packages/translate/src/index.js#L410 should rely on the default input instead of arrify version to return correctly data to the caller
