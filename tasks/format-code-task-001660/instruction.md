The order:
```
"instance-variables",
"constructor",
"static-methods",
"lifecycle",
"everything-else"
"render",                   
```

Is mistaking with **static members**.

For example:
```
private static const wrong_var = 1;
private b;

constructor(props: any) {
        super(props);

        this.state = {
            ....
        };
}
```
Throws: 
> error  wrong_var should be placed after constructor  react/sort-comp

Which is wrong....

Can you please add **"static-variables"** as option in the rule? 
Expect to be something like:
```
"static-variables",
"instance-variables",
"constructor",
"static-methods",
"lifecycle",
"everything-else"
"render",                   
```
