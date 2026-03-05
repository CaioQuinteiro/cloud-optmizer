import os
import google.auth
from dotenv import load_dotenv

# Carrega a variável GOOGLE_APPLICATION_CREDENTIALS do nosso arquivo .env
load_dotenv()

def testar_conexao_gcp():
    print("Iniciando teste de conexão com o Google Cloud...")
    try:
        # O SDK do Google busca automaticamente a variável de ambiente que configuramos
        credentials, project_id = google.auth.default()
        
        print("\n✅ SUCESSO! O Python conectou ao GCP.")
        print(f"📌 Projeto ID ativo: {project_id}")
        
        # Verifica se estamos usando a Service Account correta
        if hasattr(credentials, 'service_account_email'):
            print(f"🔑 Identidade do Robô: {credentials.service_account_email}")
        else:
            print("🔑 Autenticado, mas não com uma Service Account padrão.")
            
    except Exception as e:
        print("\n❌ ERRO de Autenticação. Verifique o arquivo .env e o JSON.")
        print(f"Detalhe técnico: {e}")

if __name__ == "__main__":
    testar_conexao_gcp()