import json
import io
from io import BufferedReader, BufferedWriter
import zipfile
from app.config import app_config

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions


client_id = app_config.adobe_client_id
client_secret = app_config.adobe_client_secret

if not client_id or not client_secret:
    raise ValueError("client secret or client id not set")



adobe_credentials = Credentials.service_principal_credentials_builder().with_client_id(
            client_id).with_client_secret(client_secret).build()
json_file_name = "structuredData.json"


def extract(adobe_credentials: ServicePrincipalCredentials, input_stream: BufferedReader):
    execution_context = ExecutionContext.create(adobe_credentials)
    extract_pdf_operation = ExtractPDFOperation.create_new()
    source = FileRef.create_from_stream(input_stream, media_type="application/pdf")
    extract_pdf_operation.set_input(source)
    extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
                .with_element_to_extract(ExtractElementType.TEXT) \
                .with_element_to_extract(ExtractElementType.TABLES) \
                .build()
    extract_pdf_operation.set_options(extract_pdf_options)
    result: FileRef = extract_pdf_operation.execute(execution_context)
    
    result.save_as("/tmp/anything")
    
    return unzip_file()

def unzip_file():
    with zipfile.ZipFile("/tmp/anything", 'r') as zip_ref:
        # zip_ref.extractall("/tmp/anything")
        file_contents = zip_ref.read(json_file_name).decode("utf-8")
    
    return json.loads(file_contents)






