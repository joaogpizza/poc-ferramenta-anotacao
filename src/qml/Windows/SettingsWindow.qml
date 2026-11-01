import QtQuick
import QtQuick.Controls

import Components

ApplicationWindow {
    id: settingsWindow

    width: 400
    height: 300
    title: qsTr("Configurações")
    color: Theme.background

    AppButton {
        anchors.centerIn: parent
        text: qsTr("Fechar")
        onClicked: settingsWindow.close()
    }
}
