import os
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

def test_qml_engine_carrega_main():
    app = QGuiApplication.instance() or QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    qml_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'Main.qml')
    engine.load(qml_path)
    
    assert engine.rootObjects(), "Falha ao carregar o Main.qml. Verifique os imports e a sintaxe."