ArcGIS provider adapter missing stateCode and streetNumber
When using the ArcGIS provider, the adapter always returns null for stateCode and an empty string for the streetNumber when geocoding an address.

i.e. when geocoding `187 Bedford Ave, Brooklyn, NY 11211`, the google adapter returns:

```
{
    latitude: 40.7175439,
    longitude: -73.95771119999999,
    country: 'United States',
    city: null,
    state: 'New York',
    stateCode: 'NY',
    zipcode: '11211',
    streetName: 'Bedford Avenue',
    streetNumber: '187',
    countryCode: 'US'
}
```

and the ArcGIS adapter returns:

```
{
    latitude: -73.95785917316152,
    longitude: 40.71766805993411,
    country: 'USA',
    city: 'Brooklyn',
    state: 'New York',
    stateCode: null,
    zipcode: '11211',
    streetName: ' Bedford Ave',
    streetNumber: '',
    countryCode: 'USA'
}
```
