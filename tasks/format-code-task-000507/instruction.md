CloudFront Sign creates invalid signature if URL contains &
Confirm by changing [ ] to [x] below to ensure that it's a bug:
- [x] I've gone though the [API reference](https://docs.aws.amazon.com/sdk-for-go/v2/api/)
- [x] I've checked [AWS Forums](https://forums.aws.amazon.com) and [StackOverflow](https://stackoverflow.com/questions/tagged/aws-sdk-go) for answers
- [x] I've searched for [previous similar issues](https://github.com/aws/aws-sdk-go-v2/issues) and didn't find any solution
  
**Describe the bug**
After switching from the V1 SDK to the V2 SDK, signing a URL with more than 2 query parameters results in an invalid signature and cloudfront will return a 403. For a url with 1 or less query parameters, the V1 SDK and V2 SDK signatures are identical. But if you have a URL with more than 2 query parameters, the V2 SDK will return a different signature than the V1 SDK. This looks like a regression from the v1 SDK - an issue was raised and fixed in V1 but it looks like the fix is not included in the v2 SDK https://github.com/aws/aws-sdk-go/issues/2163

**Version of AWS SDK for Go?**
1.40.18

**Version of Go (`go version`)?**
go1.16.4 darwin/amd64

**To Reproduce (observed behavior)**
Code example copied from this issue: https://github.com/aws/aws-sdk-go/issues/2163
```
signer := sign.NewURLSigner(keyID, privKey)
signedURL, _ := signer.Sign("https://myuploaddomain.com/", time.Now().Add(1*time.Hour))
// signedURL VALID
signedURL, _ := signer.Sign("https://myuploaddomain.com?key=one", time.Now().Add(1*time.Hour))
// signedURL VALID
signedURL, _ := signer.Sign("https://myuploaddomain.com?key=one&value=two", time.Now().Add(1*time.Hour))
// signedURL INVALID returns AccessDenied when uploading

```

**Expected behavior**
Signing a URL containing two query string parameters should result in the same signature as the V1 SDK.
