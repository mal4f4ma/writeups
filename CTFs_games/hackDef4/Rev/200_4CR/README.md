# Rev 200 4CR 

Analiza el binario C2C_module.exe adjuntado, y ayudanos a desencriptar el archivo "secret"  para obtener la flag.

Despues de analizar el binario, se encontro que era una implementacion de RC4, con este analisis pudimos entrar la llave de cifrado __hackdef_command&control_key__, con esto y por cuestiones de tiempo usamos una pagina que implementaba el RC4 para decriptar y nos dio la flag.

## FLAG

hackdef{RC4_is_c0mm0nly_used_by_m4lwar3}