# semaf-service
SEMAF microservice

# Usage
Start SEMAF service with Docker Compose:
```
docker-compose up -d
```
Use this command to transform metadata in XML with XSLT mapping and deposit in Dataverse:
```
curl -X 'POST' \
  'http://0.0.0.0:8089/tranform' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@sample-dataset.xml;type=text/xml' \
  -F 'dataverse=https://datasets.dataverse' \
  -F 'dv_target=root' \
  -F 'api_token=8f02e8f9-d9b0-4eef-a2f1-a6a4ccf12xxx' \
  -F 'xsl_url=https://raw.githubusercontent.com/Dans-labs/saxon-in-docker/main/xslt/easy-odissei.xsl'
```
