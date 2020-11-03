import sys

from PySide2.QtCore import QObject
from PySide2.QtWidgets import QApplication

from MenuWidget import MenuWidget
from DoublePlayer import DoublePlayer
from SinglePlayer import SinglePlayer


class Main(QObject):

    def __init__(self):
        super().__init__()
        self.menu_widget = MenuWidget()
        # 绑定菜单按钮点击信号
        self.menu_widget.single_clicked.connect(self.start_single_player)
        self.menu_widget.double_clicked.connect(self.start_double_player)
        self.menu_widget.network_clicked.connect(self.start_network_player)

        self.double_player = DoublePlayer()
        self.double_player.exit_clicked.connect(self.start_program)
        self.single_player = SinglePlayer()
        # network_player = NetPlayer()

    def start_program(self):  # 启动游戏
        self.menu_widget.show()

    def start_double_player(self):  # 启动双人
        self.double_player.start_game()
        self.menu_widget.hide()  # 隐藏菜单窗口

    def start_single_player(self):  # 启动单人
        self.single_player.start_game()
        self.menu_widget.hide()


    def start_network_player(self):  # 启动网络对战
        pass


if __name__ == '__main__':
    app = QApplication([])
    main = Main()
    main.start_program()
    sys.exit(app.exec_())
