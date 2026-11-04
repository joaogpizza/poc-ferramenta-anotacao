"""ViewModel da tela inicial: ponte entre o QML e as regras em Python."""

from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

# O QML enxerga esta classe com `import Backend` (nome + versão maior abaixo).
QML_IMPORT_NAME = "Backend"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class HomeViewModel(QObject):
    """Guarda o estado da HomePage e expõe ações para o QML.

    Os nomes em camelCase (clickCount, registerClick) são o contrato com o
    HomePage.qml; por isso não seguem o snake_case do Python.
    """

    # Signal: avisa o QML que clickCount mudou (o binding do Label se atualiza).
    clickCountChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._click_count = 0

    # Property somente leitura: o QML lê, mas só o Python altera o valor.
    @Property(int, notify=clickCountChanged)
    def clickCount(self):
        return self._click_count

    # Slot: método que o QML pode chamar (onClicked do botão).
    @Slot()
    def registerClick(self):
        self._click_count += 1
        self.clickCountChanged.emit()
