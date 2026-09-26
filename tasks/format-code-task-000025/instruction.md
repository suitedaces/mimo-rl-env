ts def of updateOne&findOneAndUpdate returns FlattenMap instead of UpdateWriteOpResult, when lean() is used
### Prerequisites

- [X] I have written a descriptive issue title
- [X] I have searched existing issues to ensure the bug has not already been reported


### Mongoose version

7.1.0

### Node.js version

16.20

### MongoDB server version

5.x

### Typescript version (if applicable)

4.9.5

### Description

I tried upgrading to mongoose 7.x, but now I'm stuck with some typescript issues.
![image](https://user-images.githubusercontent.com/5757263/236601137-fd8e2776-2b12-427b-bc02-e81ee801791d.png)

somehow updateOne returns a FlattenMap and not the ResultType defined in updateOne:
![image](https://user-images.githubusercontent.com/5757263/236601177-2fcb360b-5dab-4cef-91ae-066cc6c3f34b.png)

I would expect a UpdateWriteOpResult here.


### Steps to Reproduce

my UserModel is defined as 

```
const userSchema = new Schema({...});

export interface IDBUser { .. };

const DBUserModel: Model<IDBUser> = model<IDBUser>('User', userSchema);


```

just run updateOne on it and check the return type.

### Expected Behavior

typescript should correctly return the UpdateWriteOpResult
