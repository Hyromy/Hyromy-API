# Hyromy API

![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-A30000?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?logo=poetry&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

REST API publica para mi mismo.

Sirve info sobre mi actividad en github u otros medios, guarda y protege credenciales y tokens para centralizar los datos de consulta.

Proyecto auxiliar a [Hyromy Garden](https://github.com/Hyromy/Hyromy-Garden)

## Ejecutar proyecto

1. Clonar repositorio
```sh
git clone https://github.com/Hyromy/Hyromy-API.git # HTTPS
git clone git@github.com:Hyromy/Hyromy-API.git     # SSH

cd Hyromy-API
```

2. Instalar dependencias
```sh
poetry install
```

3. Ejecutar entorno de desarrollo
```sh
poetry run manage.py runserver
```
