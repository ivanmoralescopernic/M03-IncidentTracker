Vagrant.configure("2") do |config|
  # Utilitzem la imatge oficial d'Ubuntu 22.04
  config.vm.box = "ubuntu/jammy64"

  # Ports: 8000 per Django i 5432 per Postgres
  config.vm.network "forwarded_port", guest: 8000, host: 8000, auto_correct: true
  config.vm.network "forwarded_port", guest: 5432, host: 5432, auto_correct: true

  # CONFIGURACIÓ DE LA CARPETA COMPARTIDA (Sincronització)
  config.vm.synced_folder ".", "/vagrant", 
    type: "virtualbox",
    owner: "vagrant",
    group: "vagrant",
    mount_options: ["dmode=775,fmode=664"]

  config.vm.provider "virtualbox" do |vb|
    vb.name = "M03-IncidentTracker-VM"
    vb.gui = true           # Deixem la finestra oberta per veure si hi ha errors de boot
    vb.memory = "1024"
    vb.cpus = 1
    
    # FIX PER A DISCOS NVMe/THUNDERBOLT: Desactiva el cau d'I/O que provoca el VERR_DEV_IO_ERROR
    vb.customize ["modifyvm", :id, "--graphicscontroller", "vmsvga"]
    vb.customize ["modifyvm", :id, "--uartmode1", "disconnected"]
  end

  # PROVISIONAMENT (Instal·lació de tot el software)
  config.vm.provision "shell", inline: <<-SHELL
    set -e # Atura el script si hi ha qualsevol error
    
    echo "--- 1. Comprovant si la carpeta compartida funciona ---"
    if [ ! -f "/vagrant/requirements.txt" ]; then
      echo "ERROR: La carpeta compartida no s'ha muntat correctament."
      echo "Si estàs en un disc Thunderbolt NTFS/exFAT, mou el projecte a la teva /home interna."
      exit 1
    fi

    echo "--- 2. Instal·lant Docker i Python ---"
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -y
    apt-get install -y docker.io python3-pip python3-venv libpq-dev
    usermod -aG docker vagrant

    echo "--- 3. Aixecant PostgreSQL en Docker ---"
    if [ ! "$(docker ps -q -f name=db-incidents)" ]; then
        docker run --name db-incidents \
          -e POSTGRES_PASSWORD=supersecret \
          -e POSTGRES_DB=incident_db \
          -p 5432:5432 -d postgres
    fi

    echo "--- 4. Creant l'entorn virtual (.venv) ---"
    cd /vagrant
    # Creem el venv dins de la carpeta compartida
    python3 -m venv .venv
    source .venv/bin/activate
    
    echo "--- 5. Instal·lant requeriments de Django ---"
    pip install --upgrade pip
    pip install -r requirements.txt

    echo "--- 6. Migracions i Usuaris ---"
    sleep 10 # Esperem que Postgres estigui llest
    python manage.py migrate
    
    python manage.py shell <<EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
if not User.objects.filter(username='analista1').exists():
    User.objects.create_user('analista1', 'analista@example.com', 'analista123')
EOF
    echo "--------------------------------------------------"
    echo " PROJECTE CONFIGURAT AMB ÈXIT"
    echo "--------------------------------------------------"
  SHELL
end