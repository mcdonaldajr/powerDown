#!/bin/sh
set -eu

SERVICE_NAME="powerDown.service"
INSTALL_DIR="${INSTALL_DIR:-/home/pi/powerDown}"
REPO_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

if [ "$(id -u)" -ne 0 ]; then
    echo "Please run this installer with sudo:"
    echo "  sudo ./install.sh"
    exit 1
fi

echo "Installing powerDown to ${INSTALL_DIR}"

install -d -m 755 "${INSTALL_DIR}"

SOURCE_SCRIPT="${REPO_DIR}/powerDown.py"
TARGET_SCRIPT="${INSTALL_DIR}/powerDown.py"

if [ "${SOURCE_SCRIPT}" = "${TARGET_SCRIPT}" ]; then
    echo "Source already in install directory; skipping script copy."
else
    install -m 755 "${SOURCE_SCRIPT}" "${TARGET_SCRIPT}"
fi

sed "s#__INSTALL_DIR__#${INSTALL_DIR}#g" "${REPO_DIR}/${SERVICE_NAME}" > "/etc/systemd/system/${SERVICE_NAME}"
chmod 644 "/etc/systemd/system/${SERVICE_NAME}"

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

echo
echo "Installed and started ${SERVICE_NAME}."
echo "Check status with:"
echo "  sudo systemctl status ${SERVICE_NAME}"
echo "View logs with:"
echo "  sudo journalctl -u ${SERVICE_NAME} -f"
