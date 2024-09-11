# custom-exporter
Daemon to export processsus metrics to a target url.
## What it does
Sends specified processus informations to a target url at a specified frequency. <br><br>
<b>Environment variables </b>: 
- CUSTOM_EXPORTER_CONFIG : path to the yml configuration file, default : ```/etc/custom-exporter/config.yml```
- CUSTOM_EXPORTER_LOG : path to the log file used, default : ```/usr/local/custom-exporter/logs```(the user of the process must have 'write' permission on it) </ul>
<b> Configuration </b> :  <br>
<ul>
<li>target.url : http target  </li>
<li>fields : information to extract from the processes</li>
<li>frequency : (seconds) interval between 2 requests</li>
</ul>

## Setup steps 
Python version used : 3.10.12 <br>
** As most commands below require privileges, it may ease up to run those in an elevated terminal.
### 1. Create binary
1. In a python environment, install dependencies :
```
pip install -r requirements.txt
```
2. Generate the binary
```
python3 pyinstaller custom-exporter.py
```
3. Put all in one file
```
mkdir custom-exporter
mv build custom-exporter/
mv dist custom-exporter/
```
### 2. Setup configuration
0. (optional) Set the following environment variable
```
export SERVICE=custom-exporter
```
1. Add the folder where configuration will be stored
```
mkdir /etc/$SERVICE
```
2. Copy your configuration file
```
cp config.yml /etc/$SERVICE/
```
### 3. Create application folder
1. Match the service file path to your binaries <br>
By default the binaries are expected to be found at : ```/usr/local/$SERVICE/dist/$SERVICE/$SERVICE``` <br>
Either setup this folder or modify the service file.<br>
```
cp $SERVICE /usr/local/bin
```
2. Create log file and ensure your service user as proper rights to write on it : 
```
touch /usr/local/$SERVICE/logs 
```
### 4. Add the service to system
1. Save your folder (prevention)
```
cp -r /etc/systemd/system /etc/systemd/system.save$(date +%Y%m%d)
```

2. Add your service 
```
cp ./$SERVICE.service /etc/systemd/system/
```
### 5. Create user
1. Create group
```
groupadd $SERVICE
```
2. Create user (with the same name as the service)
```
adduser --system --no-create-home $SERVICE 
```
3. Add the user to the group
```
adduser $SERVICE $SERVICE 
```
4. Check by listing the users 
```
less /etc/passwd
```
** To delete a user ```deluser $SERVICE```
### 6. Start service
1. Reload services
```
systemctl daemon-reload
``` 
2. Run the service
```
systemctl start $SERVICE
```
3. Check its status
```
systemctl status $SERVICE
```
To troubleshoot, see the logs or the message displayed by the status.

<b>Optional</b>: let the system start the service at each boot
```
systemctl enable $SERVICE
```

## Reference
- service creation : https://doc.ubuntu-fr.org/creer_un_service_avec_systemd
- .service reference : https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
## Cite and share 
Please add the license to your work or add a star ✨ to the repository 😊 
## Notes
As the main goal of this "exercise" was to explore system capabilities and improve the knowledge of Linux filesystem, the python code provided is really poor so don't use it as a reference. Like no authentication feature is present, etc ...
