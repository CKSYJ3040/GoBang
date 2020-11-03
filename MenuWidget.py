import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from MyButton import MyButton


class MenuWidget(QWidget):
    # 信号
    single_clicked = Signal()
    double_clicked = Signal()
    network_clicked = Signal()

    def __init__(self):
        super().__init__()

        # 设置标题
        self.setWindowTitle('我的五子棋')
        # 窗口固定大小
        self.setFixedSize(760, 650)

        # 设置背景
        p = QPalette(self.palette())  # 获得当前的调色板
        brush = QBrush(QImage('source/五子棋界面.png'))
        p.setBrush(QPalette.Background, brush)  # 设置调色板
        self.setPalette(p)  # 给窗口设置调色板
        # 单人模式按钮
        self.single_btn = MyButton(self,'source/人机对战_hover.png','source/人机对战_normal.png','source/人机对战_press.png')
        self.single_btn.move(250,300)

        # 绑定按钮点击信号，当点击单机战按钮点击时，发送single_clicked
        self.single_btn.clicked_signal.connect(self.single_clicked)
        # 双人模式
        self.double_btn = MyButton(self,'source/双人对战_hover.png', 'source/双人对战_normal.png', 'source/双人对战_press.png')
        self.double_btn.move(250, 400)

        #
        self.double_btn.clicked_signal.connect(self.double_clicked)
        # 联机模式
        self.network_btn = MyButton(self,'source/联机对战_hover.png', 'source/联机对战_normal.png', 'source/联机对战_press.png')
        self.network_btn.move(250, 500)

        #
        self.network_btn.clicked_signal.connect(self.network_clicked)


if __name__ == '__main__':
    app = QApplication([])
    label1 = QLabel('点击单机对战按钮')
    label2 = QLabel('点击双人对战按钮')
    label3 = QLabel('点击联机对战按钮')
    w = MenuWidget()
    w.single_clicked.connect(label1.show)
    w.double_clicked.connect(label2.show)
    w.network_clicked.connect(label3.show)
    w.show()
    sys.exit(app.exec_())
