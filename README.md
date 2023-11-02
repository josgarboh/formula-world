# formula-world
Repositorio para el desarrollo del Trabajo de Fin de Grado Formula World, aplicación web en Django para fanáticos de la Fórmula 1.

# DESPLIEGUE:
josgarboh2001.pythonanywhere.com.

# IMPORTANTE

- La base de datos viene poblada, si se desea repoblar se avisa de que es un proceso de unos 15 minutos, accesible desde la url /cargaBD.
- Para poder votar los pilotos, circuitos y equipos se requiere registrarse en la aplicación.
- Para acceder al Sistema de Recomendación se requiere registrarse en la aplicación.

# Instalación:
Requisitos previos:
1. Tener instalado Python 10.1 en el sistema. Para comprobar si lo está, se puede
utilizar en una consola (símbolo del sistema o cmd) el comando “python –
version”.
2. Tener instalado git 10.8, contar con Github Desktop o alguna opcion equivalente.


A continuacion, se describen los pasos de instalacion de la aplicacion Formula
World.
1. En la carpeta o direccion que queramos, abrimos un terminal (o nos servimos
de la interfaz de GitHub Desktop) escribiendo “cmd” en la barra de busqueda.
2. Una vez en la consola, debemos clonar el repositorio de la aplicacion, ejecutando el comando “git clone enlace”. Enlace:
https://github.com/josgarboh/formula-world.git
3. Clonado el repositorio, nos situaremos en la carpeta del mismo. Para ello,
escribimos en la consola “cd formula-world” (siempre que sigamos en la carpeta
anterior, en general serıa “cd ruta-que-queramos”).
4. Acto seguido, sera muy recomendable crear un entorno virtual, sirviendonos
del paquete “virtualenv”, con el comando “virtualenv nombre-entorno”.
5. Estando en la cmd y dentro de la carpeta del proyecto, activamos dicho entorno.
El comando es “nombre-entorno\Scripts\activate”. Para verificar que, efectivamente, se ha activado, se deberıa mostrar al principio
de la lınea de los comandos.
6. Con el entorno activado, instalaremos los requisitos del proyecto (paquetes),
los cuales vienen especificados en el archivo “requirements.txt”. Para instalarlos todos, simplemente introducimos “pip install -r requirements.txt”.
Para revisar si dichos paquetes se han instalado, podemos usar el comando “pip
list”.
7. Comenzando con la configuracion del proyecto como tal, lo primero es realizar las migraciones necesarias para establecer los modelos de la aplicacion. Es muy
importante ejecutar los comandos en el orden siguiente:
1. python manage.py makemigrations web.
2. python manage.py migrate web
3. python manage.py makemigrations
4. python manage.py migrate
8. Ejecutados los comandos anteriores, simplemente queda arrancar la aplicacion
y disfrutarla, posible con el comando “python manage.py runserver”.
Se puede acceder a ella introduciendo en cualquier navegador el enlace que acompaña
a “Starting development Server at ...”.



