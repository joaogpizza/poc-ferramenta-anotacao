import QtQuick
import QtQuick.Controls

import Backend
import Components
import Pages

ApplicationWindow {
    id: mainWindow

    required property HomeViewModel homeViewModel

    signal settingsRequested()

    width: 800
    height: 600
    minimumWidth: 400
    minimumHeight: 300
    visible: true
    title: qsTr("Projeto Pró-Africa")
    color: Theme.background

    header: ToolBar {
        background: Rectangle {
            color: Theme.surface
        }

        AppButton {
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.rightMargin: Theme.spacingMedium
            text: qsTr("Configurações")
            onClicked: mainWindow.settingsRequested()
        }
    }

    HomePage {
        anchors.fill: parent
        viewModel: mainWindow.homeViewModel
    }
}
