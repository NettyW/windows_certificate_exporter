$folderPath = "C:\SignDateExporter"
$filePath = "$folderPath\CertExpire.txt"

if (-not (Test-Path -Path $folderPath)) {
    New-Item -Path $folderPath -ItemType Directory
}

if (Test-Path -Path $filePath) {
    Remove-Item -Path $filePath
}

$data = Get-ChildItem Cert:\CurrentUser\My\ |
Select-Object Thumbprint, Subject, NotAfter, NotBefore, PublicKey |
ForEach-Object {
    $cn = ($_.'Subject' -match 'CN=([^,]+)') | Out-Null
    $notAfter = $_.NotAfter.ToString("dd.MM.yyyy HH:mm:ss")
    $notBefore = $_.NotBefore.ToString("dd.MM.yyyy HH:mm:ss")
    $publicKeyBytes = $_.PublicKey.EncodedKeyValue.RawData
    $publicKeyHex = (-join ($publicKeyBytes | ForEach-Object { $_.ToString("X2") }) -replace '(.{2})', '$1 ').ToLower()
    [PSCustomObject]@{
        Thumbprint = $_.Thumbprint
        CN         = $matches[1]
        NotAfter   = $notAfter
        NotBefore  = $notBefore
        PublicKey  = $publicKeyHex
    }
}

$data | Format-Table -AutoSize

$data | ForEach-Object { "$($_.Thumbprint),$($_.CN),$($_.NotAfter),$($_.NotBefore),"$($_.PublicKey)"" } | Out-File -FilePath $filePath -Encoding utf8
