pragma Singleton

import QtQuick

// Tokens visuais centralizados: cores, espaçamentos e tipografia.
QtObject {
    readonly property color background: "#111827"
    readonly property color surface: "#1f2937"
    readonly property color border: "#374151"
    readonly property color textPrimary: "#f9fafb"
    readonly property color textSecondary: "#9ca3af"
    readonly property color primary: "#2563eb"
    readonly property color primaryHover: "#3b82f6"
    readonly property color primaryPressed: "#1d4ed8"
    readonly property color disabled: "#6b7280"

    readonly property int spacingSmall: 8
    readonly property int spacingMedium: 12
    readonly property int spacingLarge: 24

    readonly property int radius: 8
    readonly property int controlHeight: 36

    readonly property int titleSize: 24
    readonly property int bodySize: 15
}
