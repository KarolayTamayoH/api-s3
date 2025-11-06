import boto3
import json

def lambda_handler(event, context):
    # --- Entrada ---
    try:
        body = json.loads(event.get('body', '{}'))
        nombre_bucket = body.get('bucket')
        nombre_directorio = body.get('directorio')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'mensaje': f'Error en el body: {str(e)}'})
        }

    if not nombre_bucket or not nombre_directorio:
        return {
            'statusCode': 400,
            'body': json.dumps({'mensaje': 'Faltan parámetros: bucket o directorio.'})
        }

    # --- Proceso ---
    s3 = boto3.client('s3')
    try:
        # En S3 no hay directorios reales, se simulan creando un objeto con sufijo "/"
        key = nombre_directorio.rstrip('/') + '/'
        s3.put_object(Bucket=nombre_bucket, Key=key)
        mensaje = f'Directorio "{nombre_directorio}" creado en bucket "{nombre_bucket}".'
        codigo = 200
    except Exception as e:
        mensaje = str(e)
        codigo = 500

    # --- Salida ---
    return {
        'statusCode': codigo,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'mensaje': mensaje})
    }
