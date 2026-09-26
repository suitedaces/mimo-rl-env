Broken when no previewVariables is defined
Hello there. After update to 2.2.0 we've got error when no previewVariables is defined. `scriptAsReact `generates code like this with broken concatenation
```
j.src='//www.googletagmanager.com/gtm.js?id='+i+dl
+;
f.parentNode.insertBefore(j,f);
```
