import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import Backend
import Components

// Página: recebe o ViewModel e só desenha / repassa ações.
Item {
    id: homePage

    required property HomeViewModel viewModel

    ColumnLayout {
        anchors.centerIn: parent
        spacing: Theme.spacingMedium

        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Welcome to the Main Window")
            color: Theme.textPrimary
            font.pixelSize: Theme.titleSize
        }

        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Cliques: %1").arg(homePage.viewModel.clickCount)
            color: Theme.textSecondary
            font.pixelSize: Theme.bodySize
        }

        AppButton {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Click Me")
            primary: true
            onClicked: homePage.viewModel.registerClick()
        }
    }
}
