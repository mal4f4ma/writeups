# Rev 100 Rans0m

Un virus de tipo ransomware encripto los archivos de nuestra Empresa, por suerte obtuvimos el trafico de red que creemos capturo dicho malware con el nombre.

El reto consistía en un archivo pcap y un archivo txt con la flag.

Al analizar el archivo en Wireshark se identifico una sesión FTP donde se enviaba un archivo llamado svchost.exe.tar.gz
Se extrajeron los bytes del envio, de esta manera se recupero el archivo svchost.exe el cual simulaba el comportamiento del ransomware encriptando los archivos con compuertas XOR, por lo que al pasar el archivo con la flag nuevamente debería de regresar la bandera.

Siguiendo esa lógica, se ejecuto nuevamente el ransomware sobre el archivo y se obtuvo un código base64 que hacia referencia al formato de una imagen PNG, al traducir el código base64 a una imagen nos da la flag.

## FLAG
hackdef{R4nsom_L1f3_F0r3v3r_D13_B4ckup5!} 