# NEXU Challenge

Prueba backend para el despliegue de un microservicio de FastAPI para la creacion de una API basica para hacer un CRUD de modelos y marcas de vehiculos utilizando las tecnologias de Python, PostgreSQL, Docker y Docker Compose.

## Características

- Aplicación Backend con **FastAPI**.
- Base de datos **PostgreSQL 16**.
- Gestión de dependencias de Python con **Poetry**.
- Orquestación de contenedores con **Docker Compose**.
- Comandos simplificados para la gestión del entorno con **Makefile**.
- Configuración centralizada y flexible basada en variables de entorno.

---

## Requisitos Previos

- **Docker**: [Instrucciones de instalación](https://docs.docker.com/get-docker/)
- **Docker Compose**: Generalmente se incluye con la instalación de Docker en sus ultimas versiones.

---

## Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto:

### 1. Clona el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>
```

### 2. Configura las Variables de Entorno

El proyecto utiliza un archivo `.env` para gestionar las variables de entorno. Crea un archivo llamado `.env` en la raíz del proyecto.

Puedes copiar el archivo de ejemplo:
```bash
cp .env.example .env
```

Abre el archivo `.env` y asegúrate de que contenga las siguientes variables. La configuración de las variables de entorno dependen de la variable `ENVIRONMENT`.

---

## Uso con Docker

Hemos simplificado la gestión de los contenedores usando un `Makefile`. Aquí están los comandos principales:

### Iniciar la Aplicación
Para construir las imágenes e iniciar los contenedores en segundo plano:
```bash
make up
```
La API estará disponible en `http://localhost:8000`. La documentación interactiva (Swagger UI) se puede encontrar en `http://localhost:8000/docs`.

### Detener la Aplicación
Para detener los contenedores:
```bash
make stop
```

### Detener y Eliminar Todo
Para detener y eliminar los contenedores, redes y volúmenes (¡cuidado, esto borrará los datos de la base de datos si no hay un volumen persistente configurado externamente!):
```bash
make down
```

### Reconstruir las Imágenes
Si has hecho cambios en el `Dockerfile` o en las dependencias de la aplicación:
```bash
make build
```