Inicializar el backend, sniffer, y Nginx. El nobre dado a la base de datos de postgreSQL es "postgres", con usuario "postgres", contraseña "password", y nombre de tabla "Location-Data". Está sirviendo en el puerto por defecto (5432), y tiene esta estructura:

Latitud, Longitud, Fecha, Hora, ID (Todas columnas de tipo texto, y la de ID constraint de tipo identity para que la id suba cada vez que se entren datos).

El servidor de Ngninx está corriendo en puerto 80 (http), el servidor de Waitress (el backend) está corriendo en puerto 5000, el sniffer está recibiendo UDP en el puerto 5005.

El sniffer recibe tramas de la siguiente manera [Lat],[Lon],[Fecha],[Hora]. Los valores se separan con comas para las diferentes columnas, y una vez insertados en la DB, la página actualizará el valor desplegado.

Los valores de puertos pueden ser modificados. La arquitectura va a necesitar una base de datos con las características previamente mencionadas, pero pueden ser modificadas dado que se hagan los cambios respectivos en las credenciales de los scripts de python.
