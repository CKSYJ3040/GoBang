import sys

from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QApplication

from GameCore import GameCore
from GameWidget import GameWidget
from DoublePlayer import DoublePlayer
from GobangAlgorithm import GobangAlgorithm


class SinglePlayer(DoublePlayer):

    def __init__(self):
        super(SinglePlayer, self).__init__()

    def computer_down_chess(self):
        if self.is_active is False:
            return

        # 获得电脑落子位置
        # position = (0, 0)
        #
        position = GobangAlgorithm(self.game_core.chessboard).get_point()

        res = self.game_core.down_chessman(position[0], position[1], self.current_color)
        # 判断落子是否成功
        if res is None:
            return
        # 添加落子记录
        self.history.append(position)
        # 成功则显示棋子
        self.game_widget.down_chess(position, self.current_color)
        # 判断是否获胜
        if res == 'Down':
            # 继续游戏，切换颜色
            self.switch_color()
            return
        self.game_win(res)

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
        # 添加落子记录
        self.history.append(position)
        # 成功则显示棋子
        self.game_widget.down_chess(position, self.current_color)
        # 判断是否获胜
        if res == 'Down':
            # 继续游戏，切换颜色
            self.switch_color()
            # 电脑落子
            self.computer_down_chess()
            return
        self.game_win(res)


if __name__ == '__main__':
    app = QApplication([])
    game = SinglePlayer()
    game.start_game()
    sys.exit(app.exec_())