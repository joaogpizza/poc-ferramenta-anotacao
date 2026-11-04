# poc-ferramenta-anotacao
PoC para testar CI/CD

## Como executar

```bash
pip install -r requirements.txt
python src/main.py             # abre a aplicação
python src/main.py --version   # imprime a versão (usado pelo release.yml)
```

## Testes

```bash
PYTHONPATH=src pytest tests/unidade/
```

## Estrutura da integração QML/Python

- `src/qml/`: interface em QML (janelas, páginas e componentes).
- `src/backend/`: ViewModels em Python, expostos ao QML como o módulo `Backend`.
- `src/logica_anotacao.py`: regras de negócio em Python puro, sem depender de Qt.
- `src/main.py`: cria o ViewModel e o entrega ao `Main.qml` (`setInitialProperties`).
- `tests/unidade/`: testes unitários (rodam no CI).
