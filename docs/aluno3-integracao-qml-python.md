# Qt/Python, integração e arquitetura

> **Como conectar a interface (QML) aos dados e às regras da aplicação (Python)?**

## 1. Conceitos pesquisados

Separação de responsabilidades:

| Camada | Onde vive | Responsabilidade |
|---|---|---|
| View | `src/qml/` | Desenhar e repassar ações do usuário. Não tem regra de negócio. |
| ViewModel | `src/backend/` (Python) | Guardar o estado da tela e expor ações para o QML. |
| Regras / dados | `src/logica_anotacao.py` e futuros módulos | Lógica pura em Python, sem depender de Qt. |

Os blocos do Qt que fazem a ponte:

- **QObject**: classe base de Qt. Só um `QObject` consegue ter signals, slots e properties visíveis ao QML.
- **Property**: valor que o QML lê (`homePage.viewModel.clickCount`). Com um `notify`, o QML refaz o *binding* sozinho quando o valor muda.
- **Signal**: aviso emitido pelo Python (`clickCountChanged`). É o que atualiza a interface.
- **Slot**: método Python que o QML pode chamar (`registerClick()`).
- **`@QmlElement`**: registra a classe Python como tipo QML. Com `QML_IMPORT_NAME = "Backend"`, o QML usa `import Backend`.
- **Model/View**: para listas, o QML usa `ListView`/`Repeater` ligados a um `QAbstractListModel` em Python. O modelo avisa inserções/remoções e a lista atualiza só o que mudou.

## 2. Alternativas consideradas

A documentação do Qt (Best Practices for QML and Qt Quick) recomenda que o backend "empurre" os dados para o QML, com `required property` + `setInitialProperties`, ou com singletons. O guia de boas práticas do Aluno 2 (seção 1.3) resume essa recomendação.

| Alternativa | Como funciona | Quando serve | Por que não é a escolha principal |
|---|---|---|---|
| `setContextProperty` | Python publica um objeto com um nome global no QML | Protótipos rápidos | Global implícito: o QML não declara o que precisa e o `qmllint` não consegue checar. |
| **`@QmlElement` + `setInitialProperties`** (escolhida) | Tipo registrado no módulo `Backend`; Python cria a instância e entrega ao QML | Apps com várias telas | Contrato explícito (`required property`), checável e testável. |
| Singleton (`@QmlSingleton`) | Uma instância única, acessível de qualquer QML | Dados globais (configurações, sessão) | Também é recomendado pelo Qt, mas para estado de tela o ViewModel por tela é mais claro. |
| Registro manual (`qmlRegisterType`) | Mesmo efeito do decorador, mais verboso | Quando o decorador não basta | Mais código para o mesmo resultado. |
| Lista de dicts em `QVariantList` | Python manda uma lista simples ao QML | Dados pequenos e só de leitura | Atualiza a lista inteira a cada mudança e não permite edição fina (mover/redimensionar). |
| `QAbstractListModel` | Modelo com roles e notificações finas | Listas que mudam (anotações) | Mais código inicial, mas é o caminho certo para a lista de anotações. |

## 3. Demonstração

**O que foi feito.** O `Main.qml` e o `HomePage.qml` (Aluno 2) já esperavam um tipo `HomeViewModel` no módulo `Backend`, com a property `clickCount` e o método `registerClick()`. A PoC implementa esse contrato em Python.

**Arquivos**

- `src/backend/home_view_model.py`: o `HomeViewModel` (QObject com 1 Property, 1 Signal e 1 Slot).
- `src/main.py`: cria o ViewModel e o entrega ao QML (o bloco `--version` não foi alterado).
- `tests/unidade/home_view_model_test.py`: 3 testes unitários, sem abrir janela.

**Fluxo de um clique**

```text
Botão "Click Me" (QML)
  -> onClicked: viewModel.registerClick()           [Slot, Python]
  -> _click_count += 1
  -> clickCountChanged.emit()                       [Signal]
  -> binding do Label reavalia viewModel.clickCount [Property]
  -> texto "Cliques: N" atualiza
```

**Como o Python entrega o ViewModel ao QML (`main.py`)**

1. `from backend.home_view_model import HomeViewModel` registra o tipo `Backend.HomeViewModel`.
2. `engine.addImportPath(qml_dir)` permite o QML achar `Windows`, `Pages` e `Components`.
3. `engine.setInitialProperties({"homeViewModel": vm})` preenche a `required property` do `Main.qml`.
4. `engine.load(...)` cria a interface já com o ViewModel ligado.

**Como verificar**

```bash
PYTHONPATH=src pytest tests/unidade/   # testes do ViewModel e da lógica
python src/main.py                     # abre o app; clicar no botão faz o contador subir
python src/main.py --version           # continua imprimindo MyAppPoC v0.1.0
```

## 4. O código, passo a passo

`src/backend/home_view_model.py`:

| Trecho | O que faz | Por que está aí |
|---|---|---|
| `QML_IMPORT_NAME = "Backend"` | Nome do módulo QML | É o que o QML importa com `import Backend`. |
| `@QmlElement` | Registra a classe como tipo QML | Sem isso, o QML não conhece `HomeViewModel`. |
| `class HomeViewModel(QObject)` | Herda de `QObject` | Requisito para ter signals, slots e properties. |
| `clickCountChanged = Signal()` | Declara o aviso de mudança | O `notify` da property aponta para ele. |
| `self._click_count = 0` | Estado guardado em Python | O QML nunca mexe nele direto. |
| `@Property(int, notify=...)` em `clickCount` | Expõe o valor ao QML, somente leitura | O QML lê; só o Python altera. |
| `@Slot()` em `registerClick` | Método chamável pelo QML | É a "ação" do botão. |
| `self.clickCountChanged.emit()` | Dispara o aviso | Sem o `emit`, o número muda mas o Label não atualiza. |

`src/main.py` (trecho novo, depois do bloco `--version`): cria o `engine`, aponta o caminho de imports, cria o ViewModel, entrega ao QML com `setInitialProperties` e só então carrega o `Main.qml`. A variável `home_view_model` fica viva enquanto o app roda.

## 5. Proposta de aplicação na ferramenta de anotação

1. **Um ViewModel por tela** (`HomeViewModel`, depois algo como `AnnotationViewModel`), todos no módulo `Backend`.
2. **Regras fora do Qt**: funções como `formato_anotacao` ficam em módulos Python puros, testados sem interface.
3. **Lista de anotações com `QAbstractListModel`** (alvo natural do componente de anotação): cada linha tem `label`, `x`, `y` (e depois largura/altura da bounding box). Operações: adicionar, mover, redimensionar, excluir, cada uma notificando a lista.
4. **Do QML para o Python, usar sinais de interação** (por exemplo `onMoved`), e não sinais de mudança (`onValueChanged`), para não gerar laços de atualização. 
5. **Testes em duas camadas**: unitários (ViewModel e modelo, rodam no CI) e integração (carregar o QML com o ViewModel).


