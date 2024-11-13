# Simple certificate metrics exporter for windows

## Description

Exporting expire date and some more date from certificate.

## Configure

Сертификаты будут по умолчанию экспортироваться из хранилища `Cert:\CurrentUser\My\` если хотите изменить стандартное место, то поменяйте значение в **12 строчке** в файле `Cert.ps1`

## Installing

1. For installing you need first install requirements for python script:
```pip
pip install pywin32 prometheus_client
```
2. Next, clone this repository or download the scripts from the `SignDateExporter` folder and place these files on the `C` drive. It should look like this:

```fs
C/
|--SignDateExporter/
    |--Cert.ps1
    |--CertExporterService.py
```

3. Installing like win service.
Move in your terminal (cmd or powershell) to `C:\SignDateExporter\`.
Installing with command:
```cmd
python .\SCertExporterService.py --username .\YourUserName --password YourPassword --startup delayed install
```
Start with command:
```cmd
python .\SCertExporterService.py start
```
**OR**
use `sc.exe` for installing/deleting service.

4. Check `localhost:8000/metrics` must be:

```metrics
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
...
# HELP cert_not_before Start time of the certificate
# TYPE cert_not_before gauge
cert_not_before{cn="YourCertCN",instance="YourHostname",pubkey="YourPubkeyHexFormat",thumbprint="YourThumbprint"} 1.708332493e+09
# HELP cert_not_after Expiration time of the certificate
# TYPE cert_not_after gauge
cert_not_after{cn="YourCertCN",instance="YourHostname",pubkey="YourPubkeyHexFormat",thumbprint="YourThumbprint"} 1.714232493e+02
```


## DONT FORGET

* Open 8000 (default) port in windows firewall (add inbound rule for TCP 8000)
* You can change default values in `CertExporterService.py` (default *port*, default *updatetime* metrics)
* Add new target in your prometheus
* Add new (dashboard)[https://grafana.com/grafana/dashboards/22294]