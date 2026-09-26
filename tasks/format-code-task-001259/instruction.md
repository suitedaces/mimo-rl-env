Encryption status not updating after enabling encryption and recopying objects
Hi,

I create a bucket in which I put some objects:

```
        TEST_BUCKET = 'my-dummy-bucket'
        
        self.s3 = boto3.resource('s3')
        self.client = boto3.client(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )

        self.client.create_bucket(
            Bucket=TEST_BUCKET,
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'}
        )

        for i in range(1, 10):
            self.client.upload_file(
                os.path.join(dirname, 'data', 'dummy.txt'),
                TEST_BUCKET,
                'data/part-{}.txt'.format(str(i)))
```

Now, all these objects are not encrypted, and  **object.server_side_encryption** is set to None. I enable encryption in the bucket:

```
      response = self.client.put_bucket_encryption(
            Bucket=TEST_BUCKET,
            ServerSideEncryptionConfiguration={
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    },
                ]
            }
        )
```

and recopy all the objects:
   ```
  for i in range(1, 10):
      self.s3.Object(TEST_BUCKET, 'data/part-{}.txt'.format(str(i))).copy_from(CopySource={'Bucket': TEST_BUCKET, 'Key': 'data/part-{}.txt'.format(str(i))})
  ```

After recopying, the expected behavior is to have objects encrypted and **object.server_side_encryption** should be set the encryption we applied. In this case it should be set to **AES256**. But it is still set to **None**. On AWS S3, it is working fine but here on Moto it is still **None**.  I tried recopying objects with **MetadataDirective="REPLACE"** as well but still it is **None**. Could someone please indicate if I am missing something or is it a bug?

Thank you.
