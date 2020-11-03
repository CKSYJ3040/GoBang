from PySide2.QtCore import QObject


class GobangAlgorithm(QObject):

    def __init__(self, chessboard):
        super().__init__()
        self.chessboard = chessboard

    def get_point(self):
        '''
        返回落子点

        分析：获胜概率大的一个点，
        让自己获胜，同时阻止对方获胜，
        考虑哪个颜色先成功
        每个位置要考虑两种颜色的情况
        尝试在空白位置模拟落子（黑，白）
        每个位置获得一个分数，找到一个最高分位置
        然后返回。
        '''
        # import random
        # while True:
        #     # position(水平，垂直)
        #     position = (random.randint(0, 18), random.randint(0, 18))
        #     # chessboard[行：数字位置][列：水平位置]
        #     if self.chessboard[position[1]][position[0]] is None:
        #         return position

        # 定义两个列表分别记录白棋和黑棋分数
        white_score = [[0 for i in range(19)] for j in range(19)]
        black_score = [[0 for i in range(19)] for j in range(19)]
        # 模拟在棋盘上每个空白点下黑棋或白棋，记录分数
        for j in range(19):
            for i in range(19):
                if self.chessboard[j][i] is None:
                    # 模拟黑棋
                    self.chessboard[j][i] = 'Black'
                    black_score[j][i] = self.get_point_score(i, j, 'Black')
                    self.chessboard[j][i] = None
                    # 模拟白棋
                    self.chessboard[j][i] = 'White'
                    white_score[j][i] = self.get_point_score(i, j, 'White')
                    self.chessboard[j][i] = None

        # 二维列表转换成一维列表
        r_white_score = []
        r_black_score = []
        for i in white_score:  # i依次指向子列表
            r_white_score.extend(i)
        for i in black_score:
            r_black_score.extend(i)
        # 将两个一维列表中对应位置的最大值放到新的列表中
        score_list = []
        # 遍历每个对应的位置,将对应位置最大值放到score_list中
        for i in range(19 * 19):
            if r_white_score[i] < r_black_score[i]:
                score_list.append(r_black_score[i])
            else:
                score_list.append(r_white_score[i])

        # 获得score_list中最大值的棋子下标
        index = score_list.index(max(score_list))
        print(index)
        # 将下标转换成棋子位置
        x = index % 19  # 水平位置 列 19
        y = index // 19  # 垂直位置 行 19

        return x, y

    def get_point_score(self, x: int, y: int, color: str) -> int:
        '''
        获得点的分数
            该点附近相邻相同颜色棋子数量越多，分数越高
            考虑四条线：水平，竖直，正斜线，反斜线
            x：水平位置
            y：竖直位置
            color：棋子颜色
            return：int 分数
        '''

        # 定义两个列表 分别记录每条线 空白和同色棋子的分数
        # 水平 竖直 正斜线 反斜线
        blank_score = [0, 0, 0, 0]  # 记录每条 线空白分数
        # 记录每条线同色棋分数
        color_score = [0, 0, 0, 0]
        # 统计每条线 5子内 空白、同色分数
        # 从当前这个点开始统计
        # 水平
        # 右边：判断棋子颜色，
        # 如果同色棋，同色分数+1 继续
        # 如果空白，空白分数+1 并停止
        # 如果是其他颜色，停止
        # 下标变化
        i = x  # 列 -> 水平位置
        j = y  # 行 -> 竖直位置
        # 右边：行不变 列++
        while i <= 18:

            if self.chessboard[j][i] is None:
                # 位置是空白
                blank_score[0] += 1
                break
            elif self.chessboard[j][i] == color:
                # 位置有同色棋
                color_score[0] += 1
            else:
                # 位置是其他颜色
                break
            # 判断5子即可
            if i >= x + 5:
                break
            i += 1

            # 左边：行不变，列--
        i = x
        j = y
        while i >= 0:
            if self.chessboard[j][i] is None:
                blank_score[0] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score[0] += 1
            else:
                break

            if i <= x - 5:
                break
            i -= 1

        # 竖直
        # 上方 行-- 列不变
        i = x  # 列
        j = y  # 行
        while j >= 0:
            if self.chessboard[j][i] is None:
                blank_score[1] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score[1] += 1
            else:
                break

            if j <= y - 5:
                break
            j -= 1

        # 下方
        i = x  # 列
        j = y  # 行
        while j <= 18:
            if self.chessboard[j][i] is None:
                blank_score[1] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score[1] += 1
            else:
                break

            if j >= y + 5:
                break
            j += 1

        # 正斜
        # 右上方 行-- 列++
        i = x  # 列
        j = y  # 行
        while j >= 0 and i <= 18:
            if self.chessboard[j][i] is None:
                blank_score[2] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score[2] += 1
            else:
                break

            if j <= y - 5:
                break
            i += 1
            j -= 1

        # 左下方
        i = x  # 列
        j = y  # 行
        while j <= 18 and i >= 0:
            if self.chessboard[j][i] is None:
                blank_score[2] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score[2] += 1
            else:
                break

            if j >= y + 5:
                break
            i -= 1
            j += 1

        # 反斜
        # 左上方 行-- 列--
        i = x  # 列
        j = y  # 行
        while j >= 0 and i >= 0:
            if self.chessboard[j][i] is None:
                blank_score[3] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score[3] += 1
            else:
                break

            if j <= y - 5:
                break
            i -= 1
            j -= 1

        # 右下方
        i = x  # 列
        j = y  # 行
        while j <= 18 and i <= 18:
            if self.chessboard[j][i] is None:
                blank_score[3] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score[3] += 1
            else:
                break

            if j >= y + 5:
                break
            i += 1
            j += 1
        # 计算每条线颜色分数是否大于5，大于5，返回100
        for i in color_score:
            if i >= 5:
                return 100
        # 将每条线的空白分数和颜色分数相加，得到新的列表
        score_list = []
        for i in range(4):
            score_list.append(blank_score[i] + color_score[i])

        print(score_list)
        # score_list = [blank_score[i] + color_score[i] for i in range(4)]
        return max(score_list)
