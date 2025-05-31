# CodeNews

CodeNews es una plataforma web tipo blog construida en Django cuyo objetivo es unir a la comunidad de tecnología y desarrollo en un solo espacio colaborativo. A través de CodeNews, los usuarios y autores contribuyen con artículos especializados sobre programación, investigación, resolución de bugs y tendencias tecnológicas, nutriendo así un repositorio de conocimiento accesible tanto para principiantes como para expertos.

## Tecnologías

Backend: Django, Django REST Framework
Frontend: HTML5, CSS3, JavaScript, Boostrap5
Base de datos: PostgreSQL

## ¿Por qué CodeNews?

CodeNews reduce la dispersión de recursos técnicos y crea una comunidad inclusiva donde el conocimiento se comparte de manera organizada y motivadora. Si eres desarrollador, investigador o aficionado a la tecnología, ¡únete y aporta tu experiencia!

## Clona este repositorio

```bash
git clone https://github.com/JorgeGlzLlamas-dev/CodeNews
# Accede al directorio del proyecto
cd CodeNews
```

1. Crea un entorno virtual:

```bash
python -m venv venv
# Activa el entorno virtual
.venv/Scripts/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements/base.txt
```

3. Renombra el archivo `.env.example` a `.env`. Luego, rellena los valores de la base de datos.

4. Luego, ejecuta el siguiente comando para crear la base de datos e inicializar los modelos:

```bash
python manage.py migrate
```

5. Finalmente, ejecuta el siguiente comando para iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

