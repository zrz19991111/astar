from random import randint
import numpy as np


class FindWay():#寻路
    def __init__(self, x, y, g_cost, f_cost=0, pre_entry=None):
        self.x = x
        self.y = y
        # cost move form start entry to this entry
        self.g_cost = g_cost
        self.f_cost = f_cost
        self.pre_entry = pre_entry

    def getPos(self):
        return (self.x, self.y)


class Map():#地图生成
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [["\033[33m0\033[0m" for x in range(self.width)] for y in range(self.height)]

    def generateBlock(self, block_num):#地图障碍生成
        for i in range(block_num):
            x, y = (randint(0, self.width - 1), randint(0, self.height - 1))
            self.map[y][x] = 1

    def generatePos(self, rangeX, rangeY):
        x, y = (randint(rangeX[0], rangeX[1]), randint(rangeY[0], rangeY[1]))
        while self.map[y][x] == 1:
            x, y = (randint(rangeX[0], rangeX[1]), randint(rangeY[0], rangeY[1]))
        return (x, y)


    def showMap(self):#绘制地图边缘
        print("\033[34m+\033[0m" * (3 * self.width + 2))

        for row in self.map:
            s = '\033[34m+\033[0m'
            for entry in row:
                s += ' ' + str(entry) + ' '
            s += '\033[34m+\033[0m'
            print(s)

        print("\033[34m+\033[0m" * (3 * self.width + 2))


def AStarSearch(map, start, final):
    def getNewPosition(map, locatioin, offset):#对扩展位置进行判断
        x, y = (location.x + offset[0], location.y + offset[1])
        if x < 0 or x >= map.width or y < 0 or y >= map.height or map.map[y][x] == 1:
            return None
        return (x, y)

    def getPositions(map, location):#位置扩展
        #direction = [(-1, 0), (0, -1), (1, 0), (0, 1)]#四方向
        direction = [(-1,0), (0, -1), (1, 0), (0, 1), (-1,-1), (1, -1), (-1, 1), (1, 1)]#八方向
        posmap = []
        for offset in direction:
            pos = getNewPosition(map, location, offset)
            if pos is not None:
                posmap.append(pos)
        return posmap

    # imporve the heuristic distance more precisely in future
    def Heuristic(pos, final):#启发函数h（n）
        #return abs(final.x - pos[0]) + abs(final.y - pos[1]) # 曼哈顿距离
        return np.linalg.norm(np.array([final.x, final.y])-np.array([pos[0], pos[1]]))#欧式距离

    def getMoveCost(location, pos):#计算移动代价
        if location.x != pos[0] and location.y != pos[1]:
            return 1.414
        else:
            return 1


    def isInMap(map, pos):#扩展节点是否在pos中
        if pos in map:
            return map[pos]
        return None


    def addAdjacentPositions(map, location, final, openlist, closedlist):#添加可选择的位置结点
        poslist = getPositions(map, location)
        for pos in poslist:
            # if position is already in closedlist, do nothing
            if isInMap(closedlist, pos) is None:
                findEntry = isInMap(openlist, pos)
                h_cost = Heuristic(pos, final)
                g_cost = location.g_cost + getMoveCost(location, pos)
                if findEntry is None:#如果该点不在open表中，添加进open表
                    openlist[pos] = FindWay(pos[0], pos[1], g_cost, g_cost + h_cost, location)
                elif findEntry.g_cost > g_cost:#更新为最小的一个
                    findEntry.g_cost = g_cost
                    findEntry.f_cost = g_cost + h_cost
                    findEntry.pre_entry = location


    def getFastPosition(openlist):#寻找最小代价距离
        fast = None
        for entry in openlist.values():
            if fast is None:
                fast = entry
            elif fast.f_cost > entry.f_cost:
                fast = entry
        return fast

    openlist = {}
    closedlist = {}
    location = FindWay(start[0], start[1], 0.0)
    final = FindWay(final[0], final[1], 0.0)
    openlist[start] = location
    while True:
        location = getFastPosition(openlist)
        if location is None:#没有找到终点
            print("can't find valid path")
            break

        if location.x == final.x and location.y == final.y:#找到最优路径
            break

        closedlist[location.getPos()] = location
        openlist.pop(location.getPos())
        addAdjacentPositions(map, location, final, openlist, closedlist)
        # print("openlist:{}".format(openlist))
        # print("closedlist:{}".format(closedlist))


    for key in closedlist.keys():#标记已经扩展的节点
        map.map[key[1]][key[0]] = "\033[35m3\033[0m"

    while location is not None:#标记最优路径
        map.map[location.y][location.x] = "\033[31m2\033[0m"
        location = location.pre_entry


WIDTH = 20
HEIGHT = 20
BLOCK_NUM = 250
map = Map(WIDTH, HEIGHT)
map.generateBlock(BLOCK_NUM)
map.showMap()

start = (3,3)
final = (16,18)
print("start:", start)
print("final:", final)
AStarSearch(map, start, final)
map.showMap()
