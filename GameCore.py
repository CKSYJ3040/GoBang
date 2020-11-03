from PySide2.QtCore import QObject


class GameCore(QObject):

    def __init__(self):
        super().__init__()

        # 定义一个二维列表存储棋盘信息
        # 子列表存储一行棋盘棋子信息（19个）
        # 总共19行
        # None：无棋子  White：白棋  Black：黑棋
        '''
        [
            [None,None,...,None],
            [],
            [],
            ......
        ]
        '''
        # 构建一个19个None的列表：[None for i in range(19)]
        self.chessboard = [[None for i in range(19)] for j in range(19)]

    def init_game(self):
        for i in range(19):  # 遍历每一行
            for j in range(19):  # 遍历每一列
                self.chessboard[i][j] = None

    def down_chessman(self, x: int, y: int, color: str):
        '''
            落子
            参数：x：水平位置 对应列，
                  y：垂直位置 对应行
                  str：棋子颜色
            返回：获胜结果 Black White Down
        '''

        # 不为None 表示有子，不能落子
        if self.chessboard[y][x] != None:
            return None
        # self.chessboard[行][列]
        self.chessboard[y][x] = color
        # 判断获胜
        return self.judge_win(x, y, color)

    def regret(self, x: int, y: int) -> bool:
        '''
        悔棋
        参数：棋子位置
        返回：成功或失败
        '''
        # 判断当前位置有没有棋子,没有棋子则不能悔棋
        if self.chessboard[y][x] is None:
            return False
        else:
            self.chessboard[y][x] = None
            return True

    def judge_win(self, x, y, color) -> str:
        '''
        判断输赢
        参数：x，y,color, 落子颜色
        结果：如果获胜，则返回棋子颜色，否则，返回Down
        '''
        # 判断每一条线（水平、竖直、正斜线、反斜线）是否五子连珠

        # 判断水平是否构成五子连珠
        count = 1  # 计数
        # 右方向
        i = x + 1  # 位置x偏移
        while i <= 18:  # 不能超出棋盘
            # 判断位置如果没有棋子或者颜色不一致，则不再继续
            if self.chessboard[y][i] == None or self.chessboard[y][i] != color:
                break
            count += 1  # 棋子颜色一致，计数加一
            i += 1  # 查找下一个位置
        # 左方向
        i = x - 1
        while i >= 0:
            if self.chessboard[y][i] == None or self.chessboard[y][i] != color:
                break
            count += 1
            i -= 1  # 继续向左
        # 判断连子数量，如果大于等于5，表示获胜
        if count >= 5:
            return color

        # 判断竖直是否构成五子连珠
        count = 1
        # 下方
        j = y + 1
        while j <= 18:
            if self.chessboard[j][x] == None or self.chessboard[j][x] != color:
                break
            count += 1
            j += 1
        # 上方
        j = y - 1
        while j >= 0:
            if self.chessboard[j][x] == None or self.chessboard[j][x] != color:
                break
            count += 1
            j -= 1
        # 判断连子数量，如果大于等于5，表示获胜
        if count >= 5:
            return color

        # 判断正斜线是否构成五子连珠
        # 正斜线/
        count = 1
        # 右上 x+ y-
        i = x + 1  # 水平位置
        j = y - 1  # 垂直位置
        while j >= 0 and i <= 18:
            if self.chessboard[j][i] == None or self.chessboard[j][i] != color:
                break
            count += 1
            i += 1
            j -= 1
        # 左下 x- y+
        i = x - 1  # 水平位置
        j = y + 1  # 垂直位置
        while i >= 0 and j <= 18:
            if self.chessboard[j][i] == None or self.chessboard[j][i] != color:
                break
            count += 1
            i -= 1
            j += 1

        if count >= 5:
            return color

        # 反斜线\
        count = 1
        # 左上 x- y-
        i = x - 1  # 水平位置
        j = y - 1  # 垂直位置
        while j >= 0 and i >= 0:
            if self.chessboard[j][i] == None or self.chessboard[j][i] != color:
                break
            count += 1
            i -= 1
            j -= 1
        # 右下 x+ y+
        i = x + 1  # 水平位置
        j = y + 1  # 垂直位置
        while j <= 18 and i <= 18:
            if self.chessboard[j][i] == None or self.chessboard[j][i] != color:
                break
            count += 1
            i += 1
            j += 1

        if count >= 5:
            return color
        return 'Down'
