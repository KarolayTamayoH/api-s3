import boto3
import json
import base64

def lambda_handler(event, context):
    # --- Entrada ---
    try:
        body = json.loads(event.get('body', '{}'))
        nombre_bucket = body.get('bucket')
        nombre_archivo = body.get('archivo')
        contenido_base64 = body.get('contenido')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'mensaje': f'Error en el body: {str(e)}'})
        }

    if not nombre_bucket or not nombre_archivo or not contenido_base64:
        return {
            'statusCode': 400,
            'body': json.dumps({'mensaje': 'Faltan parámetros: bucket, archivo o contenido.'})
        }

    # --- Proceso ---
    s3 = boto3.client('s3')
    try:
        # Decodificamos el contenido desde base64
        contenido_bytes = base64.b64decode(contenido_base64)

        # Subimos el archivo al bucket
        s3.put_object(Bucket=nombre_bucket, Key=nombre_archivo, Body=contenido_bytes)
        mensaje = f'Archivo "{nombre_archivo}" subido correctamente al bucket "{nombre_bucket}".'
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
