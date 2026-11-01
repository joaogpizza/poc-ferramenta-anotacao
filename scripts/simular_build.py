import os
import py_compile

ARQS_REQUIRIDOS = ['src/main.py', 'src/qml/Main.qml', 'src/logica_anotacao.py']

print("Verificando arquivos essenciais para o build...")
for filepath in ARQS_REQUIRIDOS:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo necessário ausente: {filepath}")
    
    if filepath.endswith('.py'):
        py_compile.compile(filepath, doraise=True)

print("Build simulado concluído com sucesso. Integridade dos arquivos validada.")