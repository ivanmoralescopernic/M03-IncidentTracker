📋 Estructura del Projecte
L'estructura actual del projecte és la següent:
code
Text
.
├── config/             # Configuració de Django (settings.py, urls.py)
├── core/               # Aplicació principal (Models, vistes de seguretat)
├── templates/          # Interfície d'usuari (HTML)
│   ├── registration/   # Templates de Login
│   └── perfil.html     # Panell d'usuari amb control de rols (RBAC)
├── Vagrantfile         # Automatització de la infraestructura (Ubuntu 22.04)
├── requirements.txt    # Dependències (Django, Psycopg2)
└── manage.py           # Utilitat de gestió
🚀 Com començar (Instal·lació)
L'entorn s'encarrega d'instal·lar Python, Docker, la base de dades i crear els usuaris automàticament.
Aixecar la infraestructura:
Obre un terminal a la carpeta del projecte i executa:
code
Bash
vagrant up
Entrar a la màquina virtual:
code
Bash
vagrant ssh
Executar el servidor de Django:
Dins de la màquina virtual, executa:
code
Bash
cd /vagrant
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000
Accés des de Windows:
Obre el teu navegador a: http://localhost:8000
🔐 Credencials i Rols
El sistema crea automàticament dos usuaris per provar el Control d'Accés Basat en Rols (RBAC):
Usuari	Contrasenya	Rol	Què pot veure?
admin	admin123	Superusuari	Panell d'administració i avisos crítics.
analista1	analista123	Analista	Àrea privada estàndard (lectura).
🏗️ Detalls de la Infraestructura
🗄️ Base de Dades (Docker)
PostgreSQL corre dins d'un contenidor Docker aïllat:
Contenidor: db-incidents
Base de dades: incident_db
Port: 5432
🛠️ Auditoria de Seguretat
Per verificar que les contrasenyes estan xifrades a la base de dades (Hash), pots executar:
code
Bash
vagrant ssh
docker exec -it db-incidents psql -U postgres -d incident_db
# Dins de psql:
SELECT username, password FROM auth_user;
⚠️ Configuracions Crítiques
Perquè el projecte funcioni correctament entre Windows i la màquina virtual, el fitxer config/settings.py ha de tenir:
ALLOWED_HOSTS: ['*'] o ['localhost', '127.0.0.1'].
DATABASES: El HOST ha de ser '127.0.0.1' i el PORT '5432'.
TEMPLATES: El path ha d'estar configurat com 'DIRS': [BASE_DIR / 'templates'].
Autor: Ivan Morales
Projecte: M03 - IncidentTracker (Secure Deployment)
