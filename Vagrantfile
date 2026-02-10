Vagrant.configure("2") do |config|
  # Utilitzem Ubuntu 22.04 LTS
  config.vm.box = "ubuntu/jammy64"

  # Ports: 8000 per Django i 5432 per Postgres
  config.vm.network "forwarded_port", guest: 8000, host: 8000, auto_correct: true
  config.vm.network "forwarded_port", guest: 5432, host: 5432, auto_correct: true

  config.vm.provider "virtualbox" do |vb|
    vb.name = "M03-IncidentTracker-VM"
    vb.gui = true         # ACTIVEM LA FINESTRA per veure errors d'arrencada
    vb.memory = "1024"    # Baixem a 1GB per evitar que Ubuntu la pausi per falta de RAM
    vb.cpus = 1
    
    # Millores de compatibilitat per VirtualBox 6/7
    vb.customize ["modifyvm", :id, "--vtxvpid", "on"]
    vb.customize ["modifyvm", :id, "--hwvirtex", "on"]
    # Intentar forçar que VirtualBox no es baralli amb KVM
    vb.customize ["modifyvm", :id, "--nested-hw-virt", "off"]
  end

  # PROVISIONAMENT
  config.vm.provision "shell", inline: <<-SHELL
    set -e
    echo "--- Instal·lant dependències del sistema ---"
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -y
    apt-get install -y docker.io python3-pip python3-venv libpq-dev

    # Configurar Docker
    usermod -aG docker vagrant

    echo "--- Aixecant PostgreSQL en Docker ---"
    if [ ! "$(docker ps -q -f name=db-incidents)" ]; then
        if [ "$(docker ps -aq -f status=exited -f name=db-incidents)" ]; then
            docker rm db-incidents
        fi
        docker run --name db-incidents \
          -e POSTGRES_PASSWORD=supersecret \
          -e POSTGRES_DB=incident_db \
          -p 5432:5432 -d postgres
    fi

    echo "--- Configurant l'entorn de Python ---"
    cd /vagrant
    # Re-creem l'entorn virtual per assegurar que és compatible amb el Linux de la VM
    rm -rf .venv
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

    echo "--- Esperant la DB i fent migracions ---"
    sleep 10
    python manage.py migrate

    echo "--- Creant usuaris (admin/admin123 i analista1/analista123) ---"
    python manage.py shell <<EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
if not User.objects.filter(username='analista1').exists():
    User.objects.create_user('analista1', 'analista@example.com', 'analista123')
EOF

    echo "--------------------------------------------------"
    echo " TOT LLEST! Arrenca el server amb:"
    echo " python manage.py runserver 0.0.0.0:8000"
    echo "--------------------------------------------------"
  SHELL
end