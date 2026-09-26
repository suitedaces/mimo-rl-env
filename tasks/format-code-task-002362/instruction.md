Add Warnings for Ignored Options on Components
### What happened?

As uncovered in https://github.com/pulumi/pulumi/issues/9704, there are additional resource options that do nothing when applied to components. This issue is to generate warnings for each of them.

Namely, these options are ignored on Components:

- [x] ignoreChanges (implemented per https://github.com/pulumi/pulumi/pull/9863)
- [x] customTimeouts
- [x] additionalSecretOutputs
- [x] replaceOnChanges
- [x] retainOnDelete

Other options that would feasibly have the same behavior, but I was unable to confirm this:
- [ ] deleteBeforeReplace

### Steps to reproduce

Here's an example program that demonstrates the problem.
```
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const tags = {
    "issue": "9704",
    "creator": "robbiemckinstry",
    "pulumi": "yes",
};

class OurBucketComponent extends pulumi.ComponentResource {
  public bucket: aws.s3.Bucket;

  constructor(name: string, args: any, opts?: pulumi.ComponentResourceOptions) {
    super("pkg:index:OurBucketComponent", name, args, opts);
    this.bucket = new aws.s3.Bucket(name, {
      tags: args.tags,
      bucket: args.bucketName,
    }, { parent: this });
    
    this.registerOutputs({
      bucketName: this.bucket.id,
    });
  }
}

const args = {
  bucketName: "mckinstry-bug-repro",
  tags: tags,
};

const opts = {
  ignoreChanges: ["root.nested"],
  additionalSecretOutputs: ["bucket"], 
  customTimeouts: {
    create: "1ns",
    update: "1ns",
    destroy: "1ns",
  },
  retainOnDelete: true,
  replaceOnChanges: ["*"],
};

const bucket = new OurBucketComponent("mckinstry-bucket", args, opts);

// Export the bucket names and tags.
export const bucketName = bucket.bucket.id;
export const bucketTags = bucket.bucket.tags;
```

The resource options applied to `OurBucketComponent` have no effect.

### Expected Behavior

Expected to see a warning in the console if an option is ignored when applied to a Component.

### Actual Behavior

No warning, and ignoring options defies average expectations, though this design is intentional.

### Versions used

_No response_

### Additional context

_No response_

### Contributing

Vote on this issue by adding a 👍 reaction. 
To contribute a fix for this issue, leave a comment (and link to your pull request, if you've opened one already).
