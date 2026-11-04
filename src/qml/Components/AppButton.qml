import QtQuick
import QtQuick.Controls.Basic

// Botão do projeto: customiza o Button do estilo Basic (nunca de um estilo nativo).
Button {
    id: control

    property bool primary: false

    implicitHeight: Theme.controlHeight
    leftPadding: Theme.spacingMedium
    rightPadding: Theme.spacingMedium

    contentItem: Text {
        text: control.text
        font: control.font
        color: control.enabled ? Theme.textPrimary : Theme.disabled
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle {
        radius: Theme.radius
        border.width: control.primary ? 0 : 1
        border.color: Theme.border
        color: {
            if (!control.enabled)
                return Theme.surface;
            if (!control.primary)
                return control.down ? Theme.border : Theme.surface;
            if (control.down)
                return Theme.primaryPressed;
            return control.hovered ? Theme.primaryHover : Theme.primary;
        }
    }
}
