import os
import csv
import time
import socket
import subprocess
import win32serviceutil
import win32service
import win32event
from prometheus_client import start_http_server, Gauge
from datetime import datetime
port = 8000
updatetime = 3600 # (1 hour)

class CertMetricsService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CertMetricsService"
    _svc_display_name_ = "Certificate Metrics Service"
    _svc_description_ = "Exports certificate expiration metrics to Prometheus"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.run = True
        self.instance_name = socket.gethostname()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.run = False
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.main()

    def main(self):
        file_path = "C:\\SignDateExporter\\CertExpire.txt"
        powershell_script_path = "C:\\SignDateExporter\\Cert.ps1"
        cert_not_before = Gauge('cert_not_before', 'Start time of the certificate', ['cn', 'thumbprint', 'instance', 'pubkey'])
        cert_not_after = Gauge('cert_not_after', 'Expiration time of the certificate', ['cn', 'thumbprint', 'instance', 'pubkey'])

        def run_powershell_script(script_path):
            subprocess.run(["powershell.exe", "-File", script_path], check=True, capture_output=True, text=True)

        def parse_cert_file(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    thumbprint, cn, not_after_str, not_before_str, pubkey = row
                    not_after = datetime.strptime(not_after_str, "%d.%m.%Y %H:%M:%S").timestamp()
                    not_before = datetime.strptime(not_before_str, "%d.%m.%Y %H:%M:%S").timestamp()
                    cert_not_before.labels(cn=cn, thumbprint=thumbprint, instance=self.instance_name, pubkey=pubkey).set(not_before)
                    cert_not_after.labels(cn=cn, thumbprint=thumbprint, instance=self.instance_name, pubkey=pubkey).set(not_after)

        start_http_server(port)

        while self.run:
            run_powershell_script(powershell_script_path)
            parse_cert_file(file_path)
            time.sleep(updatetime)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(CertMetricsService)
