# Super validador 3000

Reto de la categoria de reversing hackDef4 quals 2020

Es momento de algo serio, encuentra la llave y obten la flag!

## File recognition

En este ultimo reto nos dan un __.exe__ de windows, vamos usar la herramineta [DIE (Detect It Easy)](http://ntinfo.biz/index.html) para hacer el roconocimiento del binario

![alt text](https://github.com/mal4f4ma/writeups/blob/master/CTFs_games/super_validator/img/img_1.JPG)

Obeservamos que es un binario de 32 bits y aunque no vemos lo que se uso para compilar el binario pasaremos a ver los *strings*.

![alt text](https://github.com/mal4f4ma/writeups/blob/master/CTFs_games/super_validator/img/img_2.JPG)

Podemos observar texto interesante, unas nos indican algun texto donde parece que logramos obtener la llave que pide el programa.

Los otros strings nos muestran que se uso [MinGW](https://en.wikipedia.org/wiki/MinGW) para compilar el binario, lo que nos indica que posiblemente este escrito en __C/C++__.

Pasamos a ejecutar el binario en la terminal para ver de que va.

```
PS C:\Users\n0tM4laf4m4\Documents\validatorr> .\SuperValidador3000.exe
Llave: some_key
Checksum SHA-5119 Invalido!!!
```

Vemos que al ejecutar nos pide una llave que psiblemente sea la bandera, al meter la llave nos da un mensaje de que el *Checksum* es invalido.

Vamos a desensamblar el binario en IDA 7.0 para empezar el *reversing*.

Empezaremos con la funcion **_main**.

![alt text](https://github.com/mal4f4ma/writeups/blob/master/CTFs_games/super_validator/img/img_3.JPG)

Vemos que aqui nos imprime el mensaje donde pide la llave y posteriormente la lee fon __fgets__

Despues de esto pasa nuestro *input* a una funcion que cuenta los *bytes* de la llave que metimos.

Seguimos con el analisis y encontramos un ciclo for que guarda el valor 0 en __EAX__ para posterioremente compararlo con un divison.

![alt text](https://github.com/mal4f4ma/writeups/blob/master/CTFs_games/super_validator/img/img_4.JPG)

Despues observamos una serie de validaciones con la operacion modulo y el largo de nuestra key, donde si no pasamos estas, nos vamos a un mensaje de error y nos saca del programa.

Con esto deducimos el largo que tiene que tener nuestro key, en este caso son 27 *bytes*.

![alt text](https://github.com/mal4f4ma/writeups/blob/master/CTFs_games/super_validator/img/img_5.JPG)

![alt text](https://github.com/mal4f4ma/writeups/blob/master/CTFs_games/super_validator/img/img_6.JPG)

Al pasar estas validaciones encontramos asignaciones de variables donde si ponemos atencion son los primeros 7 _bytes_ de la key, esta validacion se hace en un ciclo for descendente de 7 a 0, lo cual validaria, **{fedkcah** que es **hackdef{** al reves los cuel nos confirma que la llave es la _flag_.

![alt text](https://github.com/mal4f4ma/writeups/blob/master/CTFs_games/super_validator/img/img_7.JPG)

A continuacion de esto hay una validacion del ultimo caracter de la key el cual es **0x7D** que en ASCII seria **}**, si este no es el final de la key nos imprime el mensaje de error y termina la ejecucion.

![alt text](https://github.com/mal4f4ma/writeups/blob/master/CTFs_games/super_validator/img/img_8.JPG)

Al pasar esta validacion vemos que se copia el contenido de las llaves del key en un nuevo arreglo para utilizarlo posteriormente.

![alt text](https://github.com/mal4f4ma/writeups/blob/master/CTFs_games/super_validator/img/img_9.JPG)

Despues empezamos las validaciones de cada 1 de los caracteres de lo que resta del key.

![alt text](https://github.com/mal4f4ma/writeups/blob/master/CTFs_games/super_validator/img/img_10.JPG)

Vamos a sacar el pseudocodigo para enternderlo mejor.

```c++
        v15 = len_mmmm((int)v16);
        for ( l = 0; l < v15; ++l )
        {
          if ( (l == 5 || l == 11) && v16[l] != 45 )
          {
            printf("Checksum SHA-5120 Invalido!!!");
            return -1;
          }
          if ( l == 8 && v16[8] != 95 )
          {
            printf("Checksum SHA-5120 Invalido!!!");
            return -1;
          }
          if ( (l == 1 || l == 2 || l == 4 || l == 7 || l == 9 || l == 13 || l == 16) && (v16[l] <= 47 || v16[l] > 57) )
          {
            printf("Checksum SHA-5120 Invalido!!!");
            return -1;
          }
          if ( (l == 3 || l == 12 || l == 15 || l == 10) && (v16[l] <= 96 || v16[l] > 122) )
          {
            printf("Checksum SHA-5120 Invalido!!!");
            return -1;
          }
          if ( (!l || l == 6 || l == 14 || l == 17) && (v16[l] <= 64 || v16[l] > 90) )
          {
            printf("Checksum SHA-5120 Invalido!!!");
            return -1;
          }
        }
        if ( v(v16) && vv(v16) && vvv(v16) )
        {
          printf("dING DinG DINg!!!!! Deberias trabajar para la NSA!!!!");
          result = 0;
        }
        else
        {
          printf("Checksum SHA-5112 Invalido!!!");
          result = -1;
        }
```

Analizando el codigo anterior y con ayuda del ensamblador podemos deducir que **l** es l index de la key y cuando este coincide debe de estar en un rango expecifigo *Eg* **v16[l] <= 64 || v16[l] > 90** esto nos indica que ese caracter debe de estar entre 64 y 90 ASCII lo que nos da un rango de las letras mayusculas.

Posteriormente vemos que el resultado de 3 funciones (v, vv, vvv) debe ser verdadero, vamos a analizar esas funciones.

A cada funcion le pasamos el resto de la flag, es decir lo que esta entre las llaves hackdef{xxxxxxxxxxxxx}


##### Funcion v

```c++
return a1[2] * a1[3] % a1[4] == 44
    && a1[3] + a1[2] + a1[1] + *a1 - a1[4] == 243
    && *a1 * a1[1] % a1[2] + a1[3] * a1[4] == 5986;

```
##### Funcion vv
```c++
return (a1[6] + a1[7]) * (a1[10] - a1[9]) == 9306 && (a1[6] + a1[10]) * (a1[7] + a1[9]) == 20500;
```
##### Funcion vvv
```c++
return a1[15] + a1[13] + a1[12] - a1[14] - a1[16] + a1[17] == 218
    && a1[14] + a1[12] - a1[13] - a1[15] + a1[16] * a1[17] == 4199
    && a1[15] * a1[16] % a1[17] == 12
    && a1[12] * a1[13] % a1[14] == 75;
```


Las funciones hacen operaciones con ciertos caracteres algunas operaciones que dan resultados especificos.

Con estas condiciones podemos armar el **script** para resolver el reto.

Usaremos [Z3 SMT Solver](https://github.com/Z3Prover/z3), Z3 es un *Theorem Prover* desarrollado por *Microsoft* el cual nos ayudara a calcular todas esas condiciones de cada caracter de la llave lo cual nos dara la *flag*.


## Solution

Aqui tenemos el *script* que resuleve cual es la llave.

```python
#!/usr/bin/python3
#Author: n0tM4l4f4m4
#Title: solver.py

from z3 import *

serial = [BitVec('val_%i'%i,32) for i in range(0,18)]

s = Solver()

s.add(serial[5] == 45)
s.add(serial[11] == 45)
s.add(serial[8] == 95)

s.add(serial[1] > 47, serial[1] <= 57)
s.add(serial[2] > 47, serial[2] <= 57)
s.add(serial[4] > 47, serial[4] <= 57)
s.add(serial[7] > 47, serial[7] <= 57)
s.add(serial[9] > 47, serial[9] <= 57)
s.add(serial[13] > 47, serial[13] <= 57)
s.add(serial[16] > 47, serial[16] <= 57)

s.add(serial[3] > 96, serial[3] <= 122)
s.add(serial[10] > 96, serial[10] <= 122)
s.add(serial[12] > 96, serial[12] <= 122)
s.add(serial[15] > 96, serial[15] <= 122)

s.add(serial[0] > 64, serial[0] <= 90)
s.add(serial[6] > 64, serial[6] <= 90)
s.add(serial[14] > 64, serial[14] <= 90)
s.add(serial[17] > 64, serial[17] <= 90)

#function V
s.add(serial[2] * serial[3] % serial[4] == 44)
s.add(serial[3] + serial[2] + serial[1] + serial[0] - serial[4] == 243)
s.add(serial[0] * serial[1] % serial[2] + serial[3] * serial[4] == 5986)

#function VV
s.add((serial[6] + serial[7]) * (serial[10] - serial[9]) == 9306)
s.add((serial[6] + serial[10]) * (serial[7] + serial[9]) == 20500)

#function VVV
s.add(serial[15] + serial[13] + serial[12] - serial[14] - serial[16] + serial[17] == 218)
s.add(serial[14] + serial[12] - serial[13] - serial[15] + serial[16] * serial[17] == 4199)
s.add(serial[15] * serial[16] % serial[17] == 12)
s.add(serial[12] * serial[13] % serial[14] == 75)

if s.check() == sat:
    m = s.model()
    flag = ''
    for val in range(18):
        num = m[serial[val]].as_long()
        flag += chr(num)
        pass
    print("hackdef{" + flag + "}")
    pass
else:
    print('sorry =(')
    pass
```
Ejecutamos el script

```
root@n0tM4l4f4m4:~/Documents/CTFsGames/2020/hackDefCTF/rev/super_validador# ./solver.py
hackdef{U51n6-Z3_1s-f4St3R}
```

## FLAG

hackdef{U51n6-Z3_1s-f4St3R}