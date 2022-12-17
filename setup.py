import os
import time
import setuptools
import subprocess
import distutils.cmd
import distutils.log

from string import Template

with open("README.md", "r") as fh:
    long_description = fh.read()


class PostInstallCommand(distutils.cmd.Command):
    """Post-installation for installation mode."""

    def run(self):
        self.announce('Sourcing local profile', level=distutils.log.INFO)
        if os.path.exists('~/.profile'):
            subprocess.check_call(['source', '~/.profile'])
        self.announce('Please set config', level=distutils.log.INFO)
        time.sleep(5)
        subprocess.check_call(['set-config'])


# Update pip to the latest version so it can find binaries required for package
# installation like `cmake`
os.system("sudo pip3 install --upgrade pip")

# update to ensure package data is up to date
os.system("sudo apt update")
# sqlite stores temperature and humidity data locally
os.system("sudo apt install sqlite3")

# cmake is used to build binary extensions for some dependencies
os.system("sudo apt install cmake")


setuptools.setup(
    name="openplant",
    version="0.1.7",
    author="Genspace",
    description="Open Plant Incubator",
    long_description=long_description,
    url="https://github.com/genspace/openplant-incubator",
    packages=setuptools.find_packages(where="./v2/app"),
    package_dir={
        '': 'v2/app'
    },
    entry_points={
        'console_scripts': [
            'say-hello=incubator.raspberrypi.scripts:say_hello',
            'install-requirements=incubator.raspberrypi.scripts:install_requirements',
            'set-config=incubator.raspberrypi.scripts:set_config',
            'test-camera=incubator.raspberrypi.scripts:test_camera',
            'incubate-me=incubator.raspberrypi.basic_all:main'
        ]
    },
    install_requires=[
        'loguru',
        'cowsay',
        'python-dotenv',
        'sqlalchemy',
        'adafruit-circuitpython-htu21d',
        'adafruit-circuitpython-shtc3',
        'picamera',
        'adafruit-blinka',
        'RPI.GPIO',
        'pymysql',
        'dash'
    ],
    package_data={
        "incubator": [
            "raspberrypi/*.txt",
            "raspberrypi/*.ini",
            "raspberrypi/*.gpg",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# TODO: read this and fix this stuff: https://stackoverflow.com/questions/35448758/using-setup-py-to-install-python-project-as-a-systemd-service

# Install the crontab to start recording data. See `incubator.crontab` for more info`
current_user = result = subprocess.check_output(
    'whoami', shell=True).decode("utf-8").strip()
os.system(
    f"crontab -l -u {current_user} | cat - crontab | crontab -u {current_user} -")

current_user_home_dir = f'/home/{current_user}/openplant-incubator/v2/app/incubator/raspberrypi/'

# Run the admin panel on startup. See https://www.tomshardware.com/how-to/run-long-running-scripts-raspberry-pi
# for more info on why this is necessary. Here are some other links.
# manpages: https://man7.org/linux/man-pages/man1/init.1.html
# Debian wiki: https://wiki.debian.org/systemd/Services

# Fill out the template systemd service
with open(f'{current_user_home_dir}/openplant-incubator/v2/app/incubator/raspberrypi/incubator_admin.service.template', 'r') as template:
    src = Template(template.read())
    result = src.substitute({'user': current_user})
    with open(f'{current_user_home_dir}/sincubator_admin.service', 'w') as out:
        out.write(result)

# Put systemd service definition in correct place
os.system(
    f'sudo mv {current_user_home_dir}/incubator_admin.service /etc/systemd/system/incubator_admin_panel.service')

# Launch service
os.system('sudo systemctl daemon-reload')
os.system('sudo systemctl start incubator_admin_panel.service')
