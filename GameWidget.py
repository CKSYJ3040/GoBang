import sys

import PySide2
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtMultimedia import QSound

from MyButton import MyButton
from Chessman import Chessman


class GameWidget(QWidget):
    goback_signal = Signal()
    start_signal = Signal()
    regret_signal = Signal()
    lose_signal = Signal()
    # 落子信号
    position_signal = Signal(tuple)

    def __init__(self, parent=None):
        super(GameWidget, self).__init__(parent=parent)

        self.setWindowTitle('我的五子棋')

        self.setWindowIcon(QIcon('source/icon.icon'))

        # 设置背景图片
        p = QPalette(self.palette())  # 获得当前的调色板
        brush = QBrush(QImage('source/游戏界面.png'))
        p.setBrush(QPalette.Background, brush)  # 设置调色板
        self.setPalette(p)  # 给窗口设置调色板

        self.setFixedSize(QImage('source/游戏界面.png').size())
        # 返回按钮
        self.goback_button = MyButton(self, 'source/返回按钮_hover.png', 'source/返回按钮_normal.png', 'source/返回按钮_press.png')
        self.goback_button.move(655, 80)
        self.goback_button.clicked_signal.connect(self.goback_signal)
        # 开始按钮
        self.start_button = MyButton(self, 'source/开始按钮_hover.png', 'source/开始按钮_normal.png', 'source/开始按钮_press.png')
        self.start_button.move(640, 240)
        self.start_button.clicked_signal.connect(self.start_signal)
        # 悔棋按钮
        self.regret_button = MyButton(self, 'source/悔棋按钮_hover.png', 'source/悔棋按钮_normal.png', 'source/悔棋按钮_press.png')
        self.regret_button.move(640, 300)
        self.regret_button.clicked_signal.connect(self.regret_signal)
        # 认输按钮
        self.lose_button = MyButton(self, 'source/认输按钮_hover.png', 'source/认输按钮_normal.png', 'source/认输按钮_press.png')
        self.lose_button.move(640, 360)
        self.lose_button.clicked_signal.connect(self.lose_signal)

        # 落子标识
        self.focus_point = QLabel(self)
        self.focus_point.setPixmap(QPixmap('source/标识.png'))
        self.focus_point.hide()

        # 获胜图片
        self.win_lbl = QLabel(self)
        self.win_lbl.hide()

        # 存储棋盘上所有棋子
        self.chessman_list = []

    def resert(self):
        '''
        重置棋盘
        '''
        # range(0,len(self.chessman_list))
        for i in list(range(0, len(self.chessman_list)))[::-1]:  # 下标逆序 从后往前
            self.chessman_list[i].close()  # 关闭棋子显示
            del self.chessman_list[i]  # 销毁棋子
        self.focus_point.hide()  # 隐藏标识
        self.win_lbl.hide()  # 隐藏获胜标识

    def mouseReleaseEvent(self, event: PySide2.QtGui.QMouseEvent):
        '''
        处理鼠标释放事件
        '''
        coord_x = event.x()  # 获得鼠标x坐标
        coord_y = event.y()

        # 坐标转换成位置
        pos = self.reverse_to_position((coord_x, coord_y))
        # 如果位置有效，则发送落子信号
        if pos is None:
            return
        else:
            self.position_signal.emit(pos)

    # position:tuple 为参数指定类型 为tuple，可以不写
    def reverse_to_coordinate(self, position: tuple):
        '''
        将落子位置转换成坐标

        x坐标 = 50 + 水平位置 * 30
        y坐标 = 50 + 垂直位置 * 30
        '''

        x = 50 + position[0] * 30
        y = 50 + position[1] * 30
        return (x, y)

    def reverse_to_position(self, coordinate: tuple) -> tuple:
        '''
        将点击坐标转换成落子位置
        '''
        # 判断落子坐标是否有效
        # 棋盘坐标范围：左 > 35 上 > 35 右 < 590+15 下边 < 590 + 15
        x = coordinate[0]
        y = coordinate[1]
        if x <= 35 or x >= 590 + 15 or y <= 35 or y >= 590 + 15:
            return
        # 将坐标转换为落子位置
        # 思路 相对于35坐标偏向右移多少个30的宽度
        pos_x = (x - 35) // 30
        pos_y = (y - 35) // 30
        return(pos_x,pos_y)

    def down_chess(self, position, color):
        '''
        落子
        position：落子位置
            x：水平位置 19个位置，0~18
            y：垂直位置 19个位置，0~18
        color：棋子颜色
        '''
        # 构建一个棋子
        chessman = Chessman(color, self)  # 棋子颜色、父窗口
        # 将位置转换成坐标，然后将棋子移动到该位置
        coord = QPoint(*self.reverse_to_coordinate(position))
        chessman.move(coord)
        chessman.show()
        chessman.raise_() # 确保棋子显示
        # 播放落子声
        QSound.play('source/luozisheng.wav')
        # 将棋子放到当前棋子列表中
        self.chessman_list.append(chessman)
        # 显示棋子标识、
        self.focus_point.move(coord.x() - 15, coord.y() - 15)
        self.focus_point.show()
        # 让标识在上层显示
        self.focus_point.raise_()

    def goback(self):
        '''
        悔棋
        '''
        # 判断 如果没有棋子，则函数返回
        if len(self.chessman_list) == 0:
            return
        # 获取最后一个棋子
        chessman = self.chessman_list.pop()
        # 从界面删除棋子
        chessman.close()
        # 销毁棋子对象
        del chessman
        # 隐藏标识
        self.focus_point.hide()

    def show_win(self, color):
        '''
        color: 获胜方 颜色
        '''
        if color == 'White':
            # 白棋获胜
            self.win_lbl.setPixmap(QPixmap('source/白棋胜利.png'))
        else:
            # 黑棋获胜
            self.win_lbl.setPixmap(QPixmap('source/黑棋胜利.png'))
        self.win_lbl.move(65, 84)
        self.win_lbl.show()
        self.win_lbl.raise_()



if __name__ == '__main__':
    app = QApplication([])
    w = GameWidget()
    def print_position(position):
        print('print_position:', position)
        w.down_chess(position,'Black')
    # 绑定悔棋按钮与悔棋方法
    w.regret_signal.connect(w.goback)
    # 绑定开始按钮与清空棋盘方法
    w.start_signal.connect(w.resert)
    # 绑定落子信号和打印测试
    w.position_signal.connect(print_position)
    w.show_win('Black')
    w.down_chess((10, 15), 'White')
    w.show()
    sys.exit(app.exec_())
