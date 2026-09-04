$ErrorActionPreference = 'Stop'
$envPath = Join-Path $PSScriptRoot '.env'

Write-Host 'Real OTP delivery setup'
Write-Host 'Credentials are written only to Login/.env, which is git-ignored.'
Write-Host ''

$smtpHost = Read-Host 'SMTP host (example: smtp.gmail.com)'
$smtpPort = Read-Host 'SMTP port (default 587)'
if ([string]::IsNullOrWhiteSpace($smtpPort)) { $smtpPort = '587' }
$smtpUser = Read-Host 'SMTP username/email'
$smtpPassword = Read-Host 'SMTP password or app password' -AsSecureString
$smtpPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($smtpPassword))
$smtpFrom = Read-Host 'From email address'

$twilioSid = Read-Host 'Twilio Account SID'
$twilioToken = Read-Host 'Twilio Auth Token' -AsSecureString
$twilioTokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($twilioToken))
$twilioFrom = Read-Host 'Twilio phone number in E.164 format'

@"
SIGNUP_DEV_OTP=false
DEFAULT_PHONE_REGION=IN
SMTP_HOST=$smtpHost
SMTP_PORT=$smtpPort
SMTP_TLS=true
SMTP_USER=$smtpUser
SMTP_PASSWORD=$smtpPasswordPlain
SMTP_FROM=$smtpFrom
TWILIO_ACCOUNT_SID=$twilioSid
TWILIO_AUTH_TOKEN=$twilioTokenPlain
TWILIO_FROM_NUMBER=$twilioFrom
"@ | Set-Content -Path $envPath -Encoding UTF8

Write-Host ''
Write-Host "Saved real OTP delivery settings to $envPath"
Write-Host 'Restart the Flask server before testing signup.'
