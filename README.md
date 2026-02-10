# IncidentTracker (Secure Deployment)

## 📋 Estructura del Projecte

L'estructura actual del projecte és la següent:

```text
.
├── config/             # Configuració de Django (settings.py, urls.py)
├── core/               # Aplicació principal (Models, vistes de seguretat)
├── templates/          # Interfície d'usuari (HTML)
│   ├── registration/   # Templates de Login
│   └── perfil.html     # Panell d'usuari amb control de rols (RBAC)
├── Vagrantfile         # Automatització de la infraestructura (Ubuntu 22.04)
├── requirements.txt    # Dependències (Django, Psycopg2)
└── manage.py           # Utilitat de gestió
```

🚀 Com començar (Instal·lació)
L'entorn s'encarrega d'instal·lar Python, Docker, la base de dades i crear els usuaris automàticament.

1. Aixecar la infraestructura
Obre un terminal a la carpeta del projecte i executa:

```text
vagrant up
```

2. Entrar a la màquina virtual
```text
vagrant ssh
```

3. Executar el servidor de Django
Dins de la màquina virtual, executa:

```text
cd /vagrant
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

4. Accés des de Windows
Obre el navegador a:

arduino
```text
http://localhost:8000
```


🔐 Credencials i Rols
El sistema crea automàticament dos usuaris per provar el Control d'Accés Basat en Rols (RBAC):

Usuari	Contrasenya	Rol	Què pot veure?
admin	admin123	Superusuari	Panell d'administració i avisos crítics
analista1	analista123	Analista	Àrea privada estàndard (lectura)

🏗️ Detalls de la Infraestructura
🗄️ Base de Dades (Docker)
PostgreSQL corre dins d'un contenidor Docker aïllat:
```text

Contenidor: db-incidents

Base de dades: incident_db

Port: 5432
```

🛠️ Auditoria de Seguretat
Per verificar que les contrasenyes estan xifrades a la base de dades (hash), executa:

```text

vagrant ssh
docker exec -it db-incidents psql -U postgres -d incident_db
```

Dins de psql:
```text
SELECT username, password FROM auth_user;
```


⚠️ Configuracions Crítiques
Perquè el projecte funcioni correctament entre Windows i la màquina virtual, el fitxer config/settings.py ha de tenir:
```text
ALLOWED_HOSTS: ['*'] o ['localhost', '127.0.0.1']

DATABASES:

HOST = '127.0.0.1'

PORT = '5432'

TEMPLATES:

DIRS = [BASE_DIR / 'templates']
```


Autor
Ivan Morales

Projecte: M03 - IncidentTracker (Secure Deployment)
