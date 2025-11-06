import boto3
import base64
import json

def lambda_handler(event, context):
    # Entrada (JSON desde POST)
    body = json.loads(event['body'])
    nombre_bucket = body.get('bucket')
    directorio = body.get('directorio', '')
    nombre_archivo = body.get('archivo')
    contenido_base64 = body.get('contenido')

    if not nombre_bucket or not nombre_archivo or not contenido_base64:
        return {'statusCode': 400, 'mensaje': 'Faltan campos obligatorios.'}

    # Proceso
    s3 = boto3.client('s3')
    try:
        # Decodificar el contenido (viene en base64)
        contenido = base64.b64decode(contenido_base64)
        key = f'{directorio.strip("/") + "/" if directorio else ""}{nombre_archivo}'
        s3.put_object(Bucket=nombre_bucket, Key=key, Body=contenido)

        mensaje = f'Archivo "{nombre_archivo}" subido correctamente a "{key}".'
        codigo = 200
    except Exception as e:
        mensaje = str(e)
        codigo = 500

    # Salida
    return {
        'statusCode': codigo,
        'mensaje': mensaje
    }
