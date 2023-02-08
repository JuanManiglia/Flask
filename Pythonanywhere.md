## <img src="https://www.pythonanywhere.com/static/anywhere/images/PA-logo-large-icononly.png"  width="50%" height="40%"> 
# [Pythonanywhere](https://www.pythonanywhere.com/)

## Beginner

- Entramos en la pestaña `WEB`
- Seleccionamos ***Flask***
- Seleccionamos ***Python 3.9***
- **No** cambiamos el directorio para que nos crea una app de bienvenida
- Entramos en la pestaña `Files` 
- En la carpeta ***mysite/*** cargamos nuestra app y el modelo entrenado
- Buscamos `WSGI` y entramos en el editor
- Modificamos donde dice ***flask_app*** lo cambiamos por el nombre de nuestra app
- Recargamos con el botón verde
- Et voilà

## Intermediate

- Creamos un repositorio en [GitHub](https://github.com/)
- Crear una app **Flask** con python 3.9 en el apartado `WEB`
- En la pestaña `Consoles` creamos una consola ***bash***
- Creamos el un entorno virtual con el comando
> mkvirtualenv --python=/usr/bin/python3.8 my-virtualenv
- Instalamos Flask con el comando
> pip install flask
- Clonamos el repositorio de [GitHub](https://github.com/) con 
> git clone `https://github.com/{**nombre de usuario**}/{**nombre del repositorio**}.git`
- En la pestaña `Web` modificamos ***Source code*** con el **nombre del repositorio** de [GitHub](https://github.com/)
> /home/{**nombre usuario pythonanywhere**}/{**nombre del repositorio**}
- Buscamos `WSGI` y entramos en el editor
- Modificamos donde dice ***flask_app*** lo cambiamos por el nombre de nuestra app
- Modificamos ***project_home***
> project_home = '/home/{**nombre de usuario pythonanywhere**}/{**nombre del repositorio**}'
- Recargamos con el botón verde
- Et voilà

### Advanced

- Los mismos pasos que Intermediate
- En el repositorio de [GitHub](https://github.com/) vamos a la pestaña `Settings`
- En el menu de la izquierda buscamos `Webhooks`
- ***Add webhook***
- En ***Payload URL*** colocamos el url de [Pythonanywhere](https://www.pythonanywhere.com/)
> http://{**nombre de usuario**}.pythonanywhere.com/git_update
- En **Content type** elegimos `application/json`
- Seleccionamos `Just the push event.`
- En el código de la app incluimos justo debajo de `app = Flask()` los siguiente
> @app.route('/git_update', methods=['POST'])
 def git_update():
>>    repo = git.Repo('./pythonanywhere')
    origin = repo.remotes.origin
    repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200
- Ejecutamos el comando 
> git push
- En [Pythonanywhere](https://www.pythonanywhere.com/) en la pestaña `Consoles` en la consola que creamos anteriormente nos desplazamos al repositorio con el comando
> cd {**nombre del repositorio**}
- Estando dentro ejecutamos el comando
> git pull (dos veces)
- Et voilà ya cada vez que hagas una modificación en local y haga un git push hacia [GitHub](https://github.com/) se cargaran los datos en [Pythonanywhere](https://www.pythonanywhere.com/)
- Solo faltaría darle al botón verde para visualizarlo

### Expert

- Los mismos pasos que Advanced pero ahora vamos a configurar para no darle al botón verde
- En [Pythonanywhere](https://www.pythonanywhere.com/) en la pestaña `Consoles` en la consola que creamos anteriormente nos desplazamos a la dirección
> cd .git/hooks
- Ejecutamos el comando
> nano post-merge
- Se despliega un editor en el cual escribimos
> #!/bin/sh
touch + /var/www/{**nombre de usuario**}_pythonanywhere_com_wsgi.py
- Guardamos y cerramos con `Ctrl + x`
- Le asignamos permisos con el comando
> chmod +x post-merge