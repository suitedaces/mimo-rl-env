getkeys() returns value when it should error out
### Version

0.27.1

### On which OS did this happen?

Linux

### On which Python version did this happen?

Python 3.10

### Reproduction Steps

Not sure if this is expected behavior, but it's a bit intuitive that the getkeys() returns a list when you put in the wrong key sequence (like I did).

Command
```python
import siliconcompiler
c = siliconcompiler.Chip("test")
print(c.getkeys('datasheet', 'package', 'pin'))
```

Returns:
['type', 'drawing', 'pincount', 'anchor', 'length', 'width', 'thickness', 'pitch', 'pin']

Correct behavior?
-should flag incorrect key sequence

chip.getkeys('datasheet', 'package', name, 'pin')

-----
Summary of all datasheet package keys below;

job      ,datasheet      ,enum                ,"Datasheet: package type"                    ,"datasheet,package,default,type"                           
job      ,datasheet      ,[file]              ,"Datasheet: package drawing"                 ,"datasheet,package,default,drawing"                        
job      ,datasheet      ,int                 ,"Datasheet: package total pincount"          ,"datasheet,package,default,pincount"                       
job      ,datasheet      ,(float,float)       ,"Datasheeet: package anchor"                 ,"datasheet,package,default,anchor"                         
job      ,datasheet      ,(float,float,float) ,"Datasheet: package length"                  ,"datasheet,package,default,length"                         
job      ,datasheet      ,(float,float,float) ,"Datasheet: package width"                   ,"datasheet,package,default,width"                          
job      ,datasheet      ,(float,float,float) ,"Datasheet: package thickness"               ,"datasheet,package,default,thickness"                      
job      ,datasheet      ,(float,float,float) ,"Datasheet: package pitch"                   ,"datasheet,package,default,pitch"                          
job      ,datasheet      ,enum                ,"Datasheet: package pin shape"               ,"datasheet,package,default,pin,default,shape"              
job      ,datasheet      ,(float,float,float) ,"Datasheet: package pin width"               ,"datasheet,package,default,pin,default,width"              
job      ,datasheet      ,(float,float,float) ,"Datasheet: package pin length"              ,"datasheet,package,default,pin,default,length"             
job      ,datasheet      ,(float,float)       ,"Datasheet: package pin location"            ,"datasheet,package,default,pin,default,loc"                
job      ,datasheet      ,str                 ,"Datasheet: package pin name"                ,"datasheet,package,default,pin,default,name" 




### Expected Behavior

see above

### Actual Behavior

see  above
