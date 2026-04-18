import hmac
import hashlib
import subprocess
import os
from flask import Blueprint, request, abort

# Creamos el Blueprint
webhook_bp = Blueprint('webhook', __name__)

GITHUB_SECRET = os.environ.get('GITHUB_WEBHOOK')

def verify_signature(data, signature):
    mac = hmac.new(GITHUB_SECRET.encode(), msg=data, digestmod=hashlib.sha256)
    return hmac.compare_digest('sha256=' + mac.hexdigest(), signature)

@webhook_bp.route('/update_server', methods=['POST'])
def update_server():
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature or not verify_signature(request.data, signature):
        abort(403)

    # Solo actuamos si es un push a la rama 'main'
    payload = request.json
    # OJO: Aquí verificas si el push es a 'Carlos' o a 'main'
    # Si trabajas en la rama Carlos, cámbialo aquí:
    if payload.get('ref') == 'refs/heads/Carlos': 
        print("Push en rama Carlos detectado. Actualizando...")
        
        # CORRECCIÓN DE RUTA: de ./scripts/ a ./utilities/
        subprocess.Popen(["/bin/bash", "./utilities/deploy.sh"])
        
        return "Actualización iniciada", 200