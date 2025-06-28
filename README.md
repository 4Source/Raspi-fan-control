# Setup
### 1. Clone the repository 
Clone the repository into ``/usr/local/bin``
```sh
cd /usr/local/bin
sudo git clone https://github.com/4Source/Raspi-fan-control.git
```

### 2. Install requirements
Create a virtual environment
```sh
cd Raspi-fan-control
sudo python3 -m venv .venv
```
Ensure ``.vent`` is active
```sh
source .venv/bin/activate
```
Install requirements in virtual environment
```sh
sudo .venv/bin/pip install -r requirements.txt
```

### 3. Test the Script is working
```sh
sudo .venv/bin/python3 fancontrol.py --test
```
**Hint:** When the script is running the fan should turn for 10s and than stop again

### 4. Systemd Service auto run
Create as sudo a Systemd Unit ``/etc/systemd/system/fancontrol.service`` with the following content
```ini
[Unit]
Description=Script to control the fan depending on the CPU temperature

[Service]
ExecStart=/usr/local/bin/Raspi-fan-control/.venv/bin/python3 /usr/local/bin/Raspi-fan-control/fancontrol.py
User=<your-user-name>
```
**Hint:** Make sure you replace ``<your-user-name>`` with your user name. For security reasons do not use root.

Create as sudo a timer ``/etc/systemd/system/fancontrol.timer`` to let the script start ``5min`` after boot and than every ``10min`` to run again.
```ini
[Unit]
Description=Timer for fancontrol

[Timer]
OnBootSec=5min
OnUnitActiveSec=10min
Unit=fancontrol.service

[Install]
WantedBy=timers.target
```

### 5. Activate and run
```sh
sudo systemctl daemon-reload
sudo systemctl enable --now fancontrol.timer
```

### 6. Check the timer is running
```sh
systemctl status fancontrol.timer
```

### 7. Visit log file
```sh
tail -f /var/log/fancontrol.log
```