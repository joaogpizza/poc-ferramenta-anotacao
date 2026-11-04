import argparse
import os
import sys

def main():
    # =====================================================================
    # [ATENÇÃO - NÃO REMOVA] BLOCO RESERVADO PARA CI/CD
    # O argumento --version é utilizado pelo GitHub Actions (release.yml)
    # para realizar o Smoke Test do executável compilado.
    # Removê-lo ou alterar seu comportamento quebrará o pipeline de deploy.
    # =====================================================================
    parser = argparse.ArgumentParser(description="PoC Annotation Tool")
    parser.add_argument("--version", action="store_true", help="Mostra a versão e sai")
    args = parser.parse_args()

    if args.version:
        print("MyAppPoC v0.1.0")
        sys.exit(0)
    # =====================================================================
    # FIM DO BLOCO RESERVADO PARA CI/CD
    # =====================================================================

    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlApplicationEngine

    from backend.home_view_model import HomeViewModel

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    qml_dir = os.path.join(os.path.dirname(__file__), "qml")

    # Permite ao QML achar os módulos locais (Windows, Pages, Components).
    engine.addImportPath(qml_dir)

    # Python cria o ViewModel e o entrega ao Main.qml (required property).
    # A variável precisa continuar viva enquanto o app roda.
    home_view_model = HomeViewModel()
    engine.setInitialProperties({"homeViewModel": home_view_model})

    engine.load(os.path.join(qml_dir, "Main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
