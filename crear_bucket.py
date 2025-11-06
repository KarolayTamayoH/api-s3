import boto3
import json

def lambda_handler(event, context):
    # Entrada (JSON desde POST)
    body = json.loads(event['body'])
    nombre_bucket = body.get('bucket')

    if not nombre_bucket:
        return {'statusCode': 400, 'mensaje': 'Falta el nombre del bucket.'}

    # Proceso
    s3 = boto3.client('s3')
    try:
        s3.create_bucket(Bucket=nombre_bucket)
        mensaje = f'Bucket "{nombre_bucket}" creado correctamente.'
        codigo = 200
    except Exception as e:
        mensaje = str(e)
        codigo = 500

    # Salida
    return {
        'statusCode': codigo,
        'mensaje': mensaje
    }
