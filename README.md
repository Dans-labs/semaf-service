# semaf-service
SEMAF microservice

# Usage
Copy configuration file and fill required parameters: 
```
cp ./config.default.py ./config.py
```

Start SEMAF service with Docker Compose:
```
docker-compose up -d
```

# XSLT mappings
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

## Semantic Mappings with using SEMAF framework
```
curl -X 'POST' \
  'http://192.168.1.101:8089/semaf' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@0b01e41080022527_AKT_1986-01-01.dsc' \
  -F 'default_mappings_url=https://raw.githubusercontent.com/Dans-labs/semaf-client/cmdi/cbs_default_fields.csv' \
  -F 'semaf_mappings_url=https://raw.githubusercontent.com/Dans-labs/semaf-client/cmdi/cbs_mapping_fields.csv'
``` 
