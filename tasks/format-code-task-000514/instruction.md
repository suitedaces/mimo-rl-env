I’ve really been enjoying using Goformation!  I found a bug recently though that I’m not sure how to fix (I'm still learning Golang), but I tracked down the reason, and figured you might immediately know how to fix.

**Summary**:
The Fn::Join is not joining values together. I've traced this down to find that it is not reading the array inside the array.  I believe the "goformation/intrinsics/fnjoin.go" file needs to be updated to loop the inner array.  Let me know if you’d like me to put this in Github Issues
 
**# TROUBLESHOOTING WALKTHROUGH**
 
Example CF snippet from the example template in the repo:
 
```
Role:
  Fn::ImportValue:
   !Join ['-', [!Ref 'ProjectId', !Ref 'AWS::Region', 'LambdaTrustRole']]
```
 
If you try to unmarshall, and output the function.Role, it gives you nothing:
 
```
   > 2018/05/12 08:40:09 Found a AWS::Serverless::Function named GetHelloWorld (Role: )
```

Let's remove the ImportValue function:
 
```
   Role: !Join ['-', [!Ref 'ProjectId', !Ref 'AWS::Region', 'LambdaTrustRole']]
```
 
If you try to unmarshall this again, and output the function.Role as before, it gives you just "-":
 
```
   > 2018/05/12 08:40:34 Found a AWS::Serverless::Function named GetHelloWorld (Role: -)
```
So then for fun, I removed the inner array, and this worked:
 
```
   Role: !Join ['-', !Ref 'AWS::Region']
```
 
The output is:
 
```
   > 2018/05/12 08:42:03 Found a AWS::Serverless::Function named GetHelloWorld (Role: -us-east-1)
``` 
However, this syntax is in invalid.

I'm pretty sure the "goformation/intrinsics/fnjoin.go" file needs to loop the inner array.

Thanks!
