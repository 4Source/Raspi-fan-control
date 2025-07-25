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

### 4. Give access to GPIO
Add the group ``gpio`` to your user. Then logout and login again.
```sh
sudo usermod -aG gpio <your-user-name>
```
Create a rule for ``/dev/gpiomem`` so it always has the correct rights in the file ``/etc/udev/rules.d/99-gpiomem.rules`` with content:
```ini
KERNEL=="gpiomem", GROUP="gpio", MODE="0660"
```
Reload the rules and check there are correct
```sh
sudo udevadm control --reload-rules
sudo udevadm trigger
ll /dev/gpiomem
```
```out
crw-rw---- 1 root gpio ...
```

### 5. Systemd Service auto run
Create as sudo a Systemd Unit ``/etc/systemd/system/fancontrol.service`` with the following content
```ini
[Unit]
Description=Control the fan depending on the CPU temperature

[Service]
ExecStartPre=/usr/bin/test ! -f /tmp/fancontrol.lock
ExecStart=/usr/local/bin/Raspi-fan-control/.venv/bin/python3 /usr/local/bin/Raspi-fan-control/fancontrol.py
ExecStartPost=/bin/rm -f /tmp/fancontrol.lock
User=<your-user-name>
StandardOutput=journal
StandardError=journal
Type=oneshot
```
**Hint:** Make sure you replace ``<your-user-name>`` with your user name. For security reasons do not use root.

Create as sudo a timer ``/etc/systemd/system/fancontrol.timer`` to let the script start ``5sec`` after boot and than every ``10sec`` to run again.
```ini
[Unit]
Description=Timer for fancontrol

[Timer]
OnBootSec=5sec
OnUnitActiveSec=10sec
Persistent=false
Unit=fancontrol.service

[Install]
WantedBy=timers.target
```

### 6. Activate and run
```sh
sudo systemctl daemon-reload
sudo systemctl enable --now fancontrol.timer
```

### 7. Check the timer is running
```sh
systemctl status fancontrol.timer
```

### 8. Visit logs
Displays logs live as they happen
```sh
journalctl -u fancontrol.service -u fancontrol.timer -f
```

See the last logs 
```sh
journalctl -u fancontrol.service -u fancontrol.timer -e
```