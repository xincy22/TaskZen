from PyQt5.QtCore import (
    Qt,
    QPoint,
    QRect
)


class ResizableFrame:
    def __init__(self, parent, edge_thickness=2):
        self.parent = parent
        self.edge_thickness = edge_thickness
        self.dragPos = None
        self.resizing = None

    def mousePressEvent(self, event):
        print("reached PressEvent")
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos()
            self.resizing = self.which_edge(event.pos())
            event.accept()

    def mouseMoveEvent(self, event):
        print("reached MoveEvent")
        if self.resizing is not None:
            print("resizing")
            delta = event.globalPos() - self.dragPos
            new_rect = QRect(self.parent.geometry())

            if self.resizing == 'bottom_right':
                new_rect.setRight(new_rect.right() + delta.x())
                new_rect.setBottom(new_rect.bottom() + delta.y())
            elif self.resizing == 'left':
                new_rect.setLeft(new_rect.left() + delta.x())
            elif self.resizing == 'right':
                new_rect.setRight(new_rect.right() + delta.x())
            elif self.resizing == 'top':
                new_rect.setTop(new_rect.top() + delta.y())
            elif self.resizing == 'bottom':
                new_rect.setBottom(new_rect.bottom() + delta.y())

            self.parent.setGeometry(new_rect)
            self.dragPos = event.globalPos()
            event.accept()
        elif event.buttons() == Qt.LeftButton:
            print("moving")
            self.parent.move(self.parent.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
        else:
            print("setting Cursor")
            if self.is_on_right_edge(event.pos()) and self.is_on_bottom_edge(event.pos()):
                self.parent.setCursor(Qt.SizeFDiagCursor)
            elif self.is_on_left_edge(event.pos()) or self.is_on_right_edge(event.pos()):
                self.parent.setCursor(Qt.SizeHorCursor)
            elif self.is_on_top_edge(event.pos()) or self.is_on_bottom_edge(event.pos()):
                self.parent.setCursor(Qt.SizeVerCursor)
            else:
                self.parent.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        print("reached ReleaseEvent")
        self.resizing = None
        self.parent.setCursor(Qt.ArrowCursor)
        event.accept()

    def which_edge(self, pos):
        if self.is_on_right_edge(pos) and self.is_on_bottom_edge(pos):
            return 'bottom_right'
        elif self.is_on_left_edge(pos):
            return 'left'
        elif self.is_on_right_edge(pos):
            return 'right'
        elif self.is_on_top_edge(pos):
            return 'top'
        elif self.is_on_bottom_edge(pos):
            return 'bottom'
        else:
            return None

    def is_on_left_edge(self, pos):
        return pos.x() <= self.edge_thickness

    def is_on_right_edge(self, pos):
        return pos.x() >= self.parent.width() - self.edge_thickness

    def is_on_top_edge(self, pos):
        return pos.y() <= self.edge_thickness

    def is_on_bottom_edge(self, pos):
        return pos.y() >= self.parent.height() - self.edge_thickness
