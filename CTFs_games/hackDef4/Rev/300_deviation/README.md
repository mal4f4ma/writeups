# rev 300 deviation

Nos dijeron que si corremos este programa con el username correcto nos imprime la bandera, puedes checarlo?

Un ejecutable hecho con .NET, utilizamos dnspy para poder verl el codgio fuente.

El funcionamiento general es que con el usuario del sistema el programa hace una serie de operaciones para decodficar la flag.

Para encontrar el usuario usamos el siguiente script

```python
import string

dic = string.ascii_letters + string.digits + ' _.-'

buff = [-47,-86,-107,-101,-83,-41,-80,-82,13,9,-22,-82,-68,-81,-91,-49,-80,-80,-71,-87,-30,0,-36,-97,-12,-61,-101,-67,-94,-75,-26,-15]

menssage = list("Index was outside the bounds of the array.")
y = 0
user = []
flag = list('hackdef{')

for i in range(0, len(buff)):
    for letra in dic:
        flag_char = ord(menssage[i]) ^ (ord(letra)+ buff[i])
        if flag_char == ord(flag[i]):
            user.append(letra)
            print(''.join(user))
            break
            pass
        pass
    pass
```

Dando como resultado el usuario __Personal__ y con esto la flag.

## FLAG

hackdef{.N3T_no_e5_t4N_d1FiC1L!}