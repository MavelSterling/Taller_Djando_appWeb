# Taller_Djando_appWeb

Objetivo del taller: Desarrollar una aplicación web con DJango permita gestionar
los préstamos de artículos deportivos en Univalle.

INTEGRANTES:

- Edwin Cuaran
- Mavelyn Sterling
- Daniel Vergara

Instrucciones:

- Pasos para visualizar el proyecto:
  - Se accede a la carpeta univalle_project desde la terminal: 
    ```
        cd univalle_proyect
    ```

  - Para ejecutar el proyecto: 
    ```
        python3 manage.py runserver
    ```


Estructura del proyecto:

```

univalle_project/
│
├── manage.py
├── db.sqlite3
├── README.md
│
│
├── _pycache_/ 
│
├── univalle_project/  # Configuración del proyecto
│   ├── _pycache_/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── aspi.py
│   └── wsgi.py
│
└── univalle_app/  # Tu aplicación
    ├── _pycache_/
    ├── migrations/
    ├── static/
    │   └── css
    │       └── reportes.js # <-- Configuración de las tablas y gráficos
    ├── templates/   # <--- La carpeta de plantillas
    │   ├── base.html
    │   ├── multas_por_dia.html
    │   ├── reportes_deportes.html
    │   └── reportes.html
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── serializers.py
    ├── __init__.py
    └── test.py

```

Notas:

En la aplicación, cuando se utiliza los reportes con django framework, en la dirección de URL se debe poner la fecha para que llame a los artículos prestados por deporte y por día:

POR EJEMPLO:

Para reportes por deporte, entre la fecha 2023 - 01 -01 y 2023- 10 -30 y se listan todos los préstamos.

```

http://127.0.0.1:8000/reporte-deporte/?inicio_fecha=2023-01-01&fin_fecha=2023-10-30

```


Para reportes por día, entre la fecha 2023 - 01 -01 y 2023- 10 -30, y se listan todos los préstamos.

```

http://127.0.0.1:8000/reporte-dia/?inicio_fecha=2023-01-01&fin_fecha=2023-10-30

```


Para el reporte de multas se selecciona el rango se fechas y muestra la fecha de la multa junto con el valor de la multa.


- Para el registro de información en la aplicación, se utiliza Django Framework, donde se llena los formularios se da click en POST y en la parte superior al darle click en GET se obtiene la lista de los datos registrados en cada tabla o sección de la app:

Los registros de usuarios como estudiantes o funcionarios se realiza en la sección llama Univallunos

Los registros de los artículos se realiza en la sección "Artículos deportivos"

Los registros de préstamos se realiza en la sección "Préstamos", aquí se tiene relación con los usuarios

Los registros de multas se realiza en la sección "multas"

