import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class Chessman(QLabel):
    def __init__(self, color='Black', parent=None):

        super().__init__(parent=parent)
        self.color = color  # 棋子颜色

        # 设置棋子图片
        self.pic = QPixmap('source/黑子.png')
        if color != 'Black':
            self.pic = QPixmap('source/白子.png')
        self.setPixmap(self.pic)

        # 设置棋子位置
        self.x = 0  # 水平位置
        self.y = 0  # 水平位置

    # 移动棋子到某个坐标位置
    def move(self, point: QPoint):
        # 调用父类的move方法实现棋子移动
        # 默认是移动棋子左上角
        # 要让棋子的中心点移动到指定坐标位置
        # 棋子大小为30*30
        super().move(point.x() - 15, point.y() - 15)

    def set_index(self, x, y):
        # 设置棋子 在棋盘位置 0~18
        # x:水平位置
        # y:垂直位置
        self.x = x
        self.y = y


if __name__ == '__main__':
    app = QApplication([])
    # 构建棋子对象
    white = Chessman('White')
    # 移动棋子对象到某个点的坐标
    white.move(QPoint(100, 200))
    # 显示棋子
    white.show()

    black = Chessman('Black')
    black.move(QPoint(500,100))
    black.show()
    sys.exit(app.exec_())
