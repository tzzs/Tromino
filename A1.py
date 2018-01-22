from tkinter import *
import time


class point():
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def output(self):
        print('x:', self.x, ' y:', self.y)


class Square():
    """
    begin:方块起点
    end：方块终点
    n：方块个数
    """

    def __init__(self, begin, end, n):
        self.begin = begin
        self.end = end
        self.n = int(n)

    def output(self):
        self.begin.output()
        self.end.output()
        print('n:', self.n, '\n')


width = 50  # 方块宽度
n = 8  # 初始宽度
begin = point(0, 0)  # 初始方块坐标
end = point(n, n)  #
fill = point(3, 2)  # 已填充方块
step = 0
Square_list = [([step] * (n + 1)) for i in range(n + 1)]

Square_list[fill.x][fill.y] = -1  # 已填充方块置-1


# print(len(Square_list))
# print(Square_list)


def cutBlock(b, x):
    """
    切割方块为4部分
    :param b: 要分割的方块
    :param x: 返回第x部分
    :return: 切割完成的方块
    """
    bb = b.begin
    be = b.end
    n = b.n
    if x == 1:
        bx = bb
        ex = point((bb.x + be.x) / 2, (bb.y + be.y) / 2)
        bx = Square(bb, ex, n / 2)
    elif x == 2:
        beginx = point((bb.x + be.x) / 2, bb.y)
        endx = point(be.x, (bb.y + be.y) / 2)
        bx = Square(beginx, endx, n / 2)
    elif x == 3:
        beginx = point(bb.x, (bb.y + be.y) / 2)
        endx = point((bb.x + be.x) / 2, be.y)
        bx = Square(beginx, endx, n / 2)
    elif x == 4:
        beginx = point((be.x + bb.x) / 2, (bb.y + be.y) / 2)
        endx = point(be.x, be.y)
        bx = Square(beginx, endx, n / 2)
    # bx.output()
    return bx


def inblock(b, fb):
    """
    查询fb是否在b块中
    :param b: 被查找的块
    :param fb: 查找的块
    :return: True False
    """
    if fb.x <= b.end.x and fb.y <= b.end.y and fb.x > b.begin.x and fb.y > b.begin.y:
        return True
    else:
        return False


def circulation(b, fb):
    """
    计算方块填充
    :param b: 方块对象
    :param fb: 填充块
    :return: 递归调用
    """
    global step
    if b.n > 2:  # 继续分割
        block1 = cutBlock(b, 1)
        block2 = cutBlock(b, 2)
        block3 = cutBlock(b, 3)
        block4 = cutBlock(b, 4)
        # block1.output()
        # block2.output()
        # block3.output()
        # block4.output()
        cb1 = block1.end
        cb2 = point(block1.end.x + 1, block1.end.y)
        cb3 = point(block1.end.x, block1.end.y + 1)
        cb4 = point(block1.end.x + 1, block1.end.y + 1)
        step += 1
        # print('step:', step)

        if inblock(block1, fb):
            Square_list[cb2.x][cb2.y] = step
            Square_list[cb3.x][cb3.y] = step
            Square_list[cb4.x][cb4.y] = step

            circulation(block1, fb)
            circulation(block2, cb2)
            circulation(block3, cb3)
            circulation(block4, cb4)
        elif inblock(block2, fb):
            Square_list[cb1.x][cb1.y] = step
            Square_list[cb3.x][cb3.y] = step
            Square_list[cb4.x][cb4.y] = step

            circulation(block1, cb1)
            circulation(block2, fb)
            circulation(block3, cb3)
            circulation(block4, cb4)

        elif inblock(block3, fb):
            Square_list[cb1.x][cb1.y] = step
            Square_list[cb2.x][cb2.y] = step
            Square_list[cb4.x][cb4.y] = step

            circulation(block1, cb1)
            circulation(block2, cb2)
            circulation(block3, fb)
            circulation(block4, cb4)
        elif inblock(block4, fb):
            Square_list[cb1.x][cb1.y] = step
            Square_list[cb2.x][cb2.y] = step
            Square_list[cb3.x][cb3.y] = step

            circulation(block1, cb1)
            circulation(block2, cb2)
            circulation(block3, cb3)
            circulation(block4, fb)

    else:
        """
        2*2  划分为4块 进行填充
        """
        c1 = cutBlock(b, 1)
        c2 = cutBlock(b, 2)
        c3 = cutBlock(b, 3)
        c4 = cutBlock(b, 4)
        step += 1
        # print('step::::', step)
        if fb.x == c1.end.x and fb.y == c1.end.y:
            Square_list[b.end.x][b.end.y - 1] = step
            Square_list[b.end.x - 1][b.end.y] = step
            Square_list[b.end.x][b.end.y] = step
        # step += 1
        if fb.x == c2.end.x and fb.y == c2.end.y:
            Square_list[b.end.x - 1][b.end.y - 1] = step
            Square_list[b.end.x - 1][b.end.y] = step
            Square_list[b.end.x][b.end.y] = step
        # step += 1
        if fb.x == c3.end.x and fb.y == c3.end.y:
            Square_list[b.end.x - 1][b.end.y - 1] = step
            Square_list[b.end.x][b.end.y - 1] = step
            Square_list[b.end.x][b.end.y] = step
        # step += 1
        if fb.x == c4.end.x and fb.y == c4.end.y:
            Square_list[b.end.x - 1][b.end.y - 1] = step
            Square_list[b.end.x][b.end.y - 1] = step
            Square_list[b.end.x - 1][b.end.y] = step


def drawboard1(s, colors, startx=50, starty=50, cellwidth=50):
    """
    绘制方块
    :param colors: 颜色数组
    :param startx: 起点x
    :param starty: 起点y
    :param cellwidth: 方块宽度
    :return:
    """
    width = 2 * startx + len(s) * cellwidth
    height = 2 * starty + len(s) * cellwidth
    canvas.config(width=width, height=height)

    canvas.create_rectangle(50 * fill.x, 50 * fill.y, 50 * (fill.x + 1), 50 * (fill.y + 1), fill='black',
                            outline='black')
    canvas.create_text(50 * (fill.x + 0.5), 50 * (fill.y + 0.5), text='0', fill='white')
    canvas.update()
    time.sleep(0.5)
    max = int((len(s) * len(s) - 1) / 3)
    # x = 1
    for m in range(1, max + 1):
        for i in range(len(s)):
            for j in range(len(s)):
                if s[i][j] == m:
                    color = colors[m % len(colors)]
                    canvas.create_rectangle(50 * (i + 1), 50 * (j + 1), 50 * (i + 2), 50 * (j + 2),
                                            fill=color, outline='black')
                    canvas.create_text(50 * (i + 1.5), 50 * (j + 1.5), text=m, fill='white')
        time.sleep(0.5)
        canvas.update()


if __name__ == '__main__':
    block = Square(begin, end, n)
    print('block:')
    block.output()
    print(Square_list)
    circulation(block, fill)
    # print(Square_list)
    # 去除第一行第一列
    s = [([step] * (n)) for i in range(n)]
    for i in range(1, len(Square_list)):
        for j in range(1, len(Square_list)):
            s[i - 1][j - 1] = Square_list[i][j]
    print(s)

    root = Tk()
    root.title("Tromino谜题")
    canvas = Canvas(root, bg="white")
    canvas.pack()
    colors = ['red', 'orange', 'gray', 'green', 'blue', '#726dd1']
    # colors = ['#81C2D6', '#8192D6', '#D9B3E6', '#DCF7A1', '#83FCD8'], 'SkyBlue', 'cyan'
    drawboard1(s, colors)
    root.mainloop()
