import QtQml

import ProAfrica.Backend
import ProAfrica.Windows

// Orquestrador: recebe os ViewModels do Python, cria as janelas
// e liga os sinais entre elas. Nenhuma janela conhece a outra.
QtObject {
    id: app

    required property HomeViewModel homeViewModel

    property MainWindow mainWindow: MainWindow {
        homeViewModel: app.homeViewModel

        onSettingsRequested: app.settingsWindow.show()
    }

    property SettingsWindow settingsWindow: SettingsWindow {
        transientParent: app.mainWindow
    }
}
