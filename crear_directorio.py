import boto3
import json

def lambda_handler(event, context):
    # Entrada (JSON desde POST)
    body = json.loads(event['body'])
    nombre_bucket = body.get('bucket')
    nombre_directorio = body.get('directorio')

    if not nombre_bucket or not nombre_directorio:
        return {'statusCode': 400, 'mensaje': 'Faltan campos: bucket o directorio.'}

    # Proceso
    s3 = boto3.client('s3')
    try:
        # En S3 los directorios son objetos vacíos que terminan en '/'
        key = f'{nombre_directorio.strip("/")}/'
        s3.put_object(Bucket=nombre_bucket, Key=key)
        mensaje = f'Directorio "{nombre_directorio}" creado en bucket "{nombre_bucket}".'
        codigo = 200
    except Exception as e:
        mensaje = str(e)
        codigo = 500

    # Salida
    return {
        'statusCode': codigo,
        'mensaje': mensaje
    }
