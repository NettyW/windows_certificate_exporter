# Simple certificate metrics exporter for windows

## Description

Exporting expire date and some more date from certificate.

## Installing

1. For installing you need first install requirements for python script:
``` pip install pywin32 prometheus_client ```
2. Next, clone this repository or download the scripts from the `SignDateExporter` folder and place these files on the `C` drive. It should look like this:

```fs
C/
|--SignDateExporter/
    |--Cert.ps1
    |--CertExporterService.py
```

3. Installing like win service.
Move in your terminal (cmd or powershell) to `C:\SignDateExporter\`.
Installing with command: `python .\SCertExporterService.py --username .\YourUserName --password YourPassword --startup delayed install`
Start with command: `python .\SCertExporterService.py start`
**OR**
use `sc.exe` for installing/deleting service.

4. Check `localhost:8000/metrics` must be:

## DONT FORGET

* Open 8000 (default) port in windows firewall (add inbound rule for TCP 8000)
* You can change default values in `CertExporterService.py` (default *port*, default *updatetime* metrics)
* Add new target in your prometheus
