import sys
from PySide2.QtWidgets import QLabel, QApplication
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Signal


class MyButton(QLabel):
    clicked_signal = Signal()  # 定义一个信号

    def __init__(self, parent=None, *args):
        # args 三张图片
        super().__init__(parent=parent)  # 设置父窗口

        # 鼠标悬浮图片:加载一张图片，需要一个图片路径
        self.hover_pixmap = QPixmap(args[0])
        # 正常图片
        self.normal_pixmap = QPixmap(args[1])
        # 鼠标按压图片
        self.press_pixmap = QPixmap(args[2])

        # 给按钮设置默认图片：正常图片
        self.setPixmap(self.normal_pixmap)

        # 设置按钮大小 固定大小，宽和高
        self.setFixedSize(self.normal_pixmap.size())

        # 鼠标悬浮状态
        self.enter_state = False

    def enterEvent(self, event):
        '''
        重写进入事件函数，event：事件具体信息
        '''
        self.setPixmap(self.hover_pixmap)
        self.enter_state = True

    def leaveEvent(self, event):
        '''
        重写离开事件函数
        '''
        self.setPixmap(self.normal_pixmap)
        self.enter_state = False

    def mousePressEvent(self, event):
        '''
        重写鼠标按压事件
        '''
        self.setPixmap(self.press_pixmap)

    def mouseReleaseEvent(self, event):
        '''
        重写鼠标释放事件
        '''
        if self.enter_state:
            # 鼠标在按钮上释放
            self.setPixmap(self.hover_pixmap)
        else:
            self.setPixmap(self.normal_pixmap)

        self.clicked_signal.emit()  # 发射信号


if __name__ == '__main__':
    app = QApplication([])
    mybtn = MyButton('source/开始按钮_hover.png', 'source/开始按钮_normal.png', 'source/开始按钮_press.png')
    mybtn.show()
    mylabel = QLabel('按钮被点击！')
    # 绑定按钮点击信号 当信号发生时，显示label
    mybtn.clicked_signal.connect(mylabel.show)
    sys.exit(app.exec_())
