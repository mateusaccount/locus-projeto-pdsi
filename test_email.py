# test_email.py

import smtplib

# --- PREENCHA COM SUAS INFORMAÇÕES EXATAS DO settings.py ---
GMAIL_USER = 'mercyzo33gln@gmail.com'
GMAIL_PASSWORD = 'mlbmkxufqearghso'
# ---------------------------------------------------------

print("Tentando se conectar ao servidor do Gmail (smtp.gmail.com)...")

try:
    # Tenta estabelecer a conexão
    server = smtplib.SMTP('smtp.gmail.com', 587)
    
    # Inicia a comunicação com o servidor
    server.ehlo()
    
    # Inicia a criptografia TLS (mesmo que EMAIL_USE_TLS = True)
    server.starttls()
    
    print("Conexão TLS estabelecida. Tentando fazer login...")
    
    # Tenta fazer o login com suas credenciais
    server.login(GMAIL_USER, GMAIL_PASSWORD)
    
    print("\n-------------------------------------------")
    print(" SUCESSO! Login no Gmail funcionou.")
    print(" Isso significa que suas credenciais estão corretas e a conexão de rede está funcionando.")
    print("-------------------------------------------\n")

except Exception as e:
    print("\n-------------------------------------------")
    print(" FALHA! A conexão com o Gmail falhou.")
    print(" O erro foi:")
    print(f" {e}")
    print("\n Isso confirma que o problema NÃO está no seu código Django, mas sim em um bloqueio de rede.")
    print("-------------------------------------------\n")

finally:
    # Fecha a conexão, se ela foi aberta
    if 'server' in locals():
        server.quit()