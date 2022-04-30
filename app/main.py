#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Developed by Slava Tykhonov and Eko Indarto
# Data Archiving and Networked Services (DANS-KNAW), Netherlands
import uvicorn
from fastapi import FastAPI, Request, Response, File, Form, UploadFile
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
#from src.model import Vocabularies, WriteXML
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import shutil
import xml.etree.ElementTree as ET
import requests
import re
import os
import json
import requests
from pyDataverse.api import Api
import urllib3, io

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Semantic Gateway API",
        description="Semantic Gateway is Linked Open Data framework for Dataverse.",
        version="0.1",
        routes=app.routes,
    )

    openapi_schema['tags'] = tags_metadata

    app.openapi_schema = openapi_schema
    return app.openapi_schema

tags_metadata = [
    {
        "name": "country",
        "externalDocs": {
            "description": "Put this citation in working papers and published papers that use this dataset",
            "authors": 'Slava Tykhonov',
            "url": "https://dans.knaw.nl/en",
        },
    },
    {
        "name": "transformer",
        "externalDocs": {
            "description": "Endpoint to transform metadata",
            "authors": 'Slava Tykhonov'
        },
    }
]

app = FastAPI(
    openapi_tags=tags_metadata
)
#templates = Jinja2Templates(directory='templates/')
#app.mount('/static', StaticFiles(directory='static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='https?://.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.openapi = custom_openapi
configfile = '/app/conf/gateway.xml'
if 'config' in os.environ:
    configfile = os.environ['config']
http = urllib3.PoolManager()

@app.get("/")
def search(request: Request):
    input = request.query_params
    return 'hello'

@app.post("/tranform", tags=["tranformer"])
#dv_target, api_token, xsl_url, author_name, author_affiliation, contact_name, contact_email, subject
#def namespace(dv_target: str, api_token: str, xsl_url:str, file: UploadFile = File(...,description="Upload file"), request: Request):
def namespace(file: UploadFile = File(...,description="Upload file"), dataverse: str = Form(...,description="Dataverse"), dv_target: str = Form(...,description="Subdataverse"), api_token: str = Form(...,description="API Token"), xsl_url:str = Form(...,description="XSLT mapping")):    
    artnamespace = {}
    file_location = f"/tmp/{file.filename}"
    r = requests.get(xsl_url)
    xsl_location = "/tmp/mapping.xslt"
    open(xsl_location, 'wb').write(r.content)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file_location:
        workdir = '/tmp/'
        full_input_file = file_location
        full_output_file = "%s.json" % file_location
        #full_input_file = join(workdir, name)

        # prepare output file name with json extension
        #full_output_file = join(output_path, name)
        #pre, ext = os.path.splitext(full_output_file)
        #full_output_file = pre + '.json'

        os.system(f"saxonb-xslt -o {full_output_file} -s {full_input_file} -xsl {xsl_location}")

        base_url = dataverse
        api = Api(base_url, api_token)
        with open(full_output_file) as f:
          metadata = json.load(f)
        resp = api.create_dataset(dv_target, json.dumps(metadata))

    return artnamespace

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9266)
