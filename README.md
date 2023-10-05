# Omni Lock Adapter

## Api Documentation
### Check if lock connected at least once the running adapter process
##### Request
```bash
curl --location 'http://[ADAPTER_HOST]/[IMEI]'
```
##### Response
Status codes:
- 200: Lock has connected to adapter
- 502: Lock has not connected to adapter/check imei
### Ask lock for general information update
##### Request
```bash
curl --location 'http://[ADAPTER_HOST]/[IMEI]/info'
```
##### Response
Status codes:
- 200: General information has been requested from lock
- 502: Lock has not connected to adapter/check imei
### Ask lock for position update
##### Request
```bash
curl --location 'http://[ADAPTER_HOST]/[IMEI]/position'
```
##### Response
Status codes:
- 200: GPS position has been requested from lock
- 502: Lock has not connected to adapter/check imei
### Unlock lock
##### Request
```bash
curl --location 'http://[ADAPTER_HOST]/[IMEI]/unlock'
```
##### Response
Status codes:
- 200: Lock will be unlocked shortly
- 502: Lock has not connected to adapter/check imei
### Ring lock (beep)
##### Request
```bash
curl --location 'http://[ADAPTER_HOST]/[IMEI]/ring/[AMOUNT]'
```
##### Response
Status codes:
- 200: Lock will beep [AMOUNT] times
- 502: Lock has not connected to adapter/check imei
