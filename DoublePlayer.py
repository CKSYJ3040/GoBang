import sys

from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QApplication

from GameCore import GameCore
from GameWidget import GameWidget


class DoublePlayer(QObject):
    exit_clicked = Signal()

    def __init__(self):
        super(DoublePlayer, self).__init__()
        self.game_widget = GameWidget()
        self.game_core = GameCore()
        self.current_color = 'Black'  # 当前落子颜色
        self.is_active = False  # 游戏状态，是否进行中
        self.history = []  # 记录落子位置

        # 绑定游戏窗口信号 到 醋逻辑处理函数
        self.game_widget.goback_signal.connect(self.stop_game)
        self.game_widget.start_signal.connect(self.start_game)
        self.game_widget.regret_signal.connect(self.regret_game)
        self.game_widget.lose_signal.connect(self.lose_game)
        self.game_widget.position_signal.connect(self.down_chess)

    def get_reverse_color(self, color: str):
        '''
        功能函数，获得相反颜色
        '''
        if color == 'Black':
            return 'White'
        else:
            return 'Black'

    def switch_color(self):
        '''
        切换当前棋子颜色
        '''
        self.current_color = self.get_reverse_color(self.current_color)

    def start_game(self):
        self.init_game()
        self.is_active = True  # 游戏开始
        self.game_widget.show() # 显示游戏窗口

    def stop_game(self):
        self.exit_clicked.emit()
        self.game_widget.close() # 关闭

    def init_game(self):
        '''
        游戏初始化
        '''
        self.game_widget.resert()  # 初始化界面
        self.game_core.init_game()  # c初始化棋盘
        self.history.clear()
        self.current_color = 'Black'

    def down_chess(self, position):
        '''
        落子
        '''
        # 判断游戏状态,状态为False，不能落子
        if self.is_active is False:
            return
        res = self.game_core.down_chessman(position[0], position[1], self.current_color)
        # 判断落子是否成功
        if res is None:
            return
        #添加落子记录
        self.history.append(position)
        # 成功则显示棋子
        self.game_widget.down_chess(position,self.current_color)
        # 判断是否获胜
        if res == 'Down':
            # 继续游戏，切换颜色
            self.switch_color()
            return
        self.game_win(res)

    def game_win(self, color):
        self.is_active = False
        self.game_widget.show_win(color)

    def lose_game(self):
        if self.is_active is False:
            return
        self.is_active = False
        self.game_widget.show_win(self.get_reverse_color(self.current_color))

    def regret_game(self):
        if self.is_active is False:
            return

        # 如果棋盘中少于两个棋子，不能悔棋
        if len(self.history) < 1:
             return
        # 撤销两个棋子
        # for i in range(2):
        position = self.history.pop()
        res = self.game_core.regret(*position)
        if res is False:
            return
        self.game_widget.goback()
        self.current_color = self.get_reverse_color(self.current_color)



if __name__ == '__main__':
    app = QApplication([])
    game = DoublePlayer()
    game.start_game()
    sys.exit(app.exec_())