from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout


class AspectRatioWidget(QWidget):
    def __init__(self, child, ratio=4/3):
        super().__init__()
        self.child = child
        self.ratio = ratio

        layout = QVBoxLayout(self)
        layout.addWidget(self.child, alignment=Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()

        target_w = w
        target_h = int(w / self.ratio)

        if target_h > h:
            target_h = h
            target_w = int(h * self.ratio)

        self.child.resize(target_w, target_h)
