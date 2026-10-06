import QtQuick

Rectangle {
    id: root
    color: "black"
    property int stage: 0
    property real elapsed: 0
    property date currentTime: new Date()

    Timer {
        interval: 1000
        running: true
        repeat: true
        onTriggered: root.currentTime = new Date()
    }

    readonly property int edgeCount: 225
    readonly property string edgeChar: "S"
    readonly property real orbitRadius: 200
    readonly property real orbitSpeed: 30
    readonly property real centerSpinSpeed: 0
    readonly property real centerPulsePeriod: 8
    readonly property real edgeSpinSpeed: 180
    readonly property real rainbowSpeed: 120

    // All animation periods divide 3600 seconds, so the loop joins smoothly.
    NumberAnimation on elapsed {
        from: 0
        to: 3600
        duration: 3600000
        loops: Animation.Infinite
        running: true
    }

    FontLoader {
        id: orbitFont
        source: "fonts/JBSemibold.ttf"
    }

    FontLoader {
        id: clockFont
        source: "fonts/FiraCode-Light.ttf"
    }

    Image {
        anchors.centerIn: parent
        width: 232
        height: 232
        source: "images/arch.png"
        fillMode: Image.Stretch
        smooth: true
        mipmap: true
        scale: 0.75 + 0.25 * Math.cos(2 * Math.PI * root.elapsed / root.centerPulsePeriod)
        // Qt and pygame use opposite rotation directions.
        rotation: -(root.elapsed * root.centerSpinSpeed) % 360
    }

    Column {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 40
        spacing: 6

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            text: Qt.formatTime(root.currentTime, "HH:mm:ss")
            font.family: clockFont.name
            font.weight: Font.Light
            font.pixelSize: 36
            color: "#a0ffff"
        }

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            text: Qt.formatDate(root.currentTime, "dd.MM.yyyy")
            font.family: clockFont.name
            font.weight: Font.Light
            font.pixelSize: 22
            color: "#a0ffff"
        }
    }

    Repeater {
        model: root.edgeCount
        delegate: Text {
            required property int index
            readonly property real phase: index / root.edgeCount
            readonly property real angle: (phase * 360 + root.elapsed * root.orbitSpeed) * Math.PI / 180
            x: root.width / 2 + Math.cos(angle) * root.orbitRadius - width / 2
            y: root.height / 2 + Math.sin(angle) * root.orbitRadius - height / 2
            text: root.edgeChar
            font.family: orbitFont.name
            font.pixelSize: 64
            color: Qt.hsva(((phase * 360 + root.elapsed * root.rainbowSpeed) % 360) / 360, 1, 1, 1)
            rotation: -(phase * 360 + root.elapsed * root.edgeSpinSpeed) % 360
            transformOrigin: Item.Center
        }
    }
}
