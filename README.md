# powerDown

`powerDown` is a Raspberry Pi systemd service that watches a UPS power-loss signal on a GPIO pin and shuts the Pi down if power is not restored within a configured grace period.

By default, the script watches BCM GPIO 24. When that pin falls low, it waits 12 seconds, runs `sync`, waits another 3 seconds for disk flushes, then shuts the Pi down.

## Hardware Assumption

The UPS signal should be connected so that BCM GPIO 24 goes low when mains power is lost.

If your UPS uses another GPIO pin or you need a longer grace period, edit these constants in `powerDown.py` before installing:

```python
PIN = 24
POWER_OUTAGE = 12
FLUSH_TO_DISK = 3
```

## Install From Git

On the Raspberry Pi:

```sh
sudo apt update
sudo apt install -y git python3-rpi.gpio
git clone https://github.com/mcdonaldajr/powerDown.git
cd powerDown
sudo ./install.sh
```

The installer copies the script to `/home/pi/powerDown`, installs the systemd unit at `/etc/systemd/system/powerDown.service`, enables it, and starts it.

To install somewhere else:

```sh
sudo INSTALL_DIR=/opt/powerDown ./install.sh
```

## Manage The Service

Check whether the service is running:

```sh
sudo systemctl status powerDown.service
```

View logs:

```sh
sudo journalctl -u powerDown.service -f
```

Restart after editing:

```sh
sudo ./install.sh
```

Stop or disable the service:

```sh
sudo systemctl stop powerDown.service
sudo systemctl disable powerDown.service
```

## Files

- `powerDown.py` - GPIO monitor and shutdown logic.
- `powerDown.service` - systemd service template used by the installer.
- `install.sh` - installer for Raspberry Pi OS.
