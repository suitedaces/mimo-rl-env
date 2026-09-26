ccz drawing inconsistency
A cz gate is being draw like this:
```
qr = QuantumRegister(2, 'q')
circuit = QuantumCircuit(qr)
circuit.append(ZGate().control(1), [qr[0], qr[1]])
circuit.draw()
```
```  
q_0: |0>─■─
         │ 
q_1: |0>─■─     
```

![image](https://user-images.githubusercontent.com/766693/76632131-15a5da00-6519-11ea-8794-55f1b26bdbaa.png)

![image](https://user-images.githubusercontent.com/766693/76632458-a4b2f200-6519-11ea-88a5-db932e93d465.png)

A ccz gate is being draw like this:
```
qr = QuantumRegister(3, 'q')
circuit = QuantumCircuit(qr)
circuit.append(ZGate().control(2), [qr[0], qr[1], qr[2]])
circuit.draw('text')
```
```
             
q_0: |0>──■──
          │  
q_1: |0>──■──
        ┌─┴─┐
q_2: |0>┤ Z ├
        └───┘
```
![image](https://user-images.githubusercontent.com/766693/76632604-d75cea80-6519-11ea-98ea-397ae4a6e1e6.png)

![image](https://user-images.githubusercontent.com/766693/76632631-e04dbc00-6519-11ea-9945-cc77ce114c47.png)

I thinks they all should be something like this:
```
             
q_0: |0>──■──
          │  
q_1: |0>──■──
          │  
q_2: |0>──■──
```
