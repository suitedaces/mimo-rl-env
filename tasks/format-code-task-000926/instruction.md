Parsing issue with nested lists in details block
Hi all 👋,

First, thanks for your work, it's awesome and very useful !

I think I spotted an issue when trying to add "complex" content in a details block, here is a description:

#### Without details block

I define the following structure:

```
Without details block
- Parent 1  
    Intro 1  

    - Child 1
    - Child 2
    - Child 3
    - Child 3

    Outro 1
```

which yields the following HTML:

```
<p>Without details block</p>
<ul>
    <li>
        <p>Parent 1<br />
            Intro 1 </p>
        <ul>
            <li>Child 1</li>
            <li>Child 2</li>
            <li>Child 3</li>
            <li>Child 3</li>
        </ul>
        <p>Outro 1</p>
    </li>
</ul>
```

which gives this in the browser:

![image](https://user-images.githubusercontent.com/11026636/107019424-ee47a380-67a1-11eb-9c13-6c89a2b7e247.png)

#### With details block

Now, when I try to add a details block around in order to make it collapsible:

```
???+ "With details block"
    - Parent 1  
        Intro 1  

        - Child 1
        - Child 2
        - Child 3
        - Child 3

        Outro 1
```

yielding this HTML:

```
<details open="open">
    <summary>With details block</summary>
    <ul>
        <li>
            <p>Parent 1<br />
                Intro 1 </p>
            <ul>
                <li>Child 1<ul>
                        <li>Child 2</li>
                        <li>Child 3</li>
                        <li>Child 3</li>
                    </ul>
                </li>
            </ul>
            <p>Outro 1</p>
        </li>
    </ul>
</details>
```

(you can already spot the issue here around `Child 1`), this gives:

![image](https://user-images.githubusercontent.com/11026636/107019583-23ec8c80-67a2-11eb-85ad-3e22820fc051.png)

The HTML is badly formatted in the children 2, 3, 4 got one extra level of indentation.

---

I tried a lot of whitespace / linebreaks / indentation combination attempting to solve the issue but I could not make it.

Is there any chance that this comes from the extension itself ?

Thanks a lot guys 😊
