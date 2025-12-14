DARK_STYLESHEET = """
/* Global Reset & Base */
* {
    outline: none;
}

QWidget {
    background-color: #18181b; /* Zinc-950 */
    color: #f4f4f5; /* Zinc-100 */
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}

/* Tooltips */
QToolTip {
    background-color: #27272a;
    color: #f4f4f5;
    border: 1px solid #3f3f46;
    border-radius: 4px;
    padding: 6px;
}

/* Main Window Containers */
#inputFrame, #queueFrame {
    background-color: #27272a; /* Zinc-900 */
    border: 1px solid #3f3f46; /* Zinc-700 */
    border-radius: 12px;
}

/* Line Edit */
QLineEdit {
    background-color: #18181b;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 8px 12px;
    color: #f4f4f5;
    selection-background-color: #6366f1; /* Indigo-500 */
}
QLineEdit:focus {
    border: 1px solid #6366f1;
}

/* Buttons */
QPushButton {
    background-color: #6366f1; /* Indigo-500 */
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #4f46e5; /* Indigo-600 */
}
QPushButton:pressed {
    background-color: #4338ca; /* Indigo-700 */
}
QPushButton:disabled {
    background-color: #3f3f46;
    color: #71717a;
}

/* Secondary/Icon Buttons */
QPushButton#settingsBtn {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    color: #a1a1aa;
}
QPushButton#settingsBtn:hover {
    background-color: #3f3f46;
    color: #f4f4f5;
    border: 1px solid #52525b;
}

/* ComboBox */
QComboBox {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 8px 12px;
    min-width: 100px;
}
QComboBox:hover {
    border: 1px solid #52525b;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
    border-left-width: 0px;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #a1a1aa;
    margin-right: 10px;
}
QComboBox QAbstractItemView {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    selection-background-color: #6366f1;
    selection-color: #ffffff;
    outline: none;
    padding: 4px;
    border-radius: 8px;
}

/* List Widget (Queue) */
QListWidget {
    background-color: transparent;
    border: none;
    outline: none;
}
QListWidget::item {
    background-color: transparent;
    padding: 4px;
}
QListWidget::item:selected {
    background-color: transparent;
}

/* ScrollBar */
QScrollBar:vertical {
    border: none;
    background: #18181b;
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #3f3f46;
    min-height: 20px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #52525b;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Labels */
QLabel {
    color: #f4f4f5;
}
QLabel#headerLabel {
    font-size: 18px;
    font-weight: 700;
    color: #f4f4f5;
}

/* Video Card */
#videoCard {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 8px;
}
#videoCard:hover {
    border: 1px solid #52525b;
}

/* Progress Bar */
QProgressBar {
    background-color: #18181b;
    border: none;
    border-radius: 4px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background-color: #6366f1;
    border-radius: 4px;
}

/* Cancel Button (Negative Action) */
#cancelBtn {
    background-color: transparent;
    color: #a1a1aa;
    border: none;
    border-radius: 4px;
    font-size: 16px;
}
#cancelBtn:hover {
    background-color: #3f3f46;
    color: #ef4444; /* Red-500 */
}
#cancelBtn:pressed {
    background-color: #52525b;
}
"""

