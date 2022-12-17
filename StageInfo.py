class Stage1:
    def __init__ (self):
        #플랫폼 위치 (x축 시작 지점, 발판 넓이)
        self.platform_01 = [(-100,3000)] #바닥
        self.platform_02 = [(96,194),(532,96)] #1층 발판
        self.platform_03 = [] #2층 발판
        self.platform_04 = [(176,32),(640,194),(864,96),(1000,96)] #3층 발판 
        self.platform_img = 'sprite/stage/stage_01.png'
        self.ledder = [] # 사다리 x축, y축
        self.flower = [(177,20),(448,169),(1064,20)] # 아이템 - 꽃 x축, y축
        self.enemy_gasi = [(200,181),(863,181),(897,181)]
        self.enemy_monster = [] #몬스터 - 시작위치, 이동범위 (x1, x2)
        self.goal = [150,167]

class Stage2:
    def __init__ (self):
        #플랫폼 위치 (x축 시작 지점, 발판 넓이)
        self.platform_01 = [(-100,3000)] 
        self.platform_02 = [(823,194)]
        self.platform_03 = [(390,30),(1130,62)]
        self.platform_04 = [(18,62),(120,62),(220,62),(1039,62)]
        self.platform_img = 'sprite/stage/stage_02.png'
        self.ledder = [(280,46)] # 사다리 x축, y축
        self.flower = [(32,20),(390,54),(560,170),(1056,20)] # 아이템 - 꽃 x축, y축
        self.enemy_gasi = [(496,181),(620,181)]
        self.enemy_monster = [(103,163,0,2400)] #몬스터 - 시작위치(x,y), 이동범위 (x1, x2)
        self.goal = [1152,52]

class Stage3:
    def __init__ (self):
        #플랫폼 위치 (x축 시작 지점, 발판 넓이)
        self.platform_01 = [(-100,352),(418,2000)] 
        self.platform_02 = [(272,104),(637,30)]
        self.platform_03 = [(758,164),(1121,30)]
        self.platform_04 = [(0,78),(635,62),(990,62)]
        self.platform_img = 'sprite/stage/stage_03.png'
        self.ledder = [(76,46)] # 사다리 x축, y축
        self.flower = [(284,90),(651,20),(837,170),(1121,54),(1170,169)] # 아이템 - 꽃 x축, y축
        self.enemy_gasi = [(706,181),(790,181),(880,181),(970,181)]
        self.enemy_monster = [(170,163,0,249),(870,48,760,950)] #몬스터 - 시작위치(x,y), 이동범위 (x1, x2)
        self.goal = [9,18]


class Stage4:
    def __init__ (self):
        #플랫폼 위치 (x축 시작 지점, 발판 넓이)
        self.platform_01 = [(-100,294),(360,80),(499,194),(1160,30)] 
        self.platform_02 = [(136,194),(425,30),(548,30),(977,194)]
        self.platform_03 = [(718,62),(819,62),(918,90)]
        self.platform_04 = [(609,62),(1008,62)]
        self.platform_img = 'sprite/stage/stage_04.png'
        self.ledder = [] # 사다리 x축, y축
        self.flower = [(425,90),(625,20),(661,170),(1025,20)] # 아이템 - 꽃 x축, y축
        self.enemy_gasi = []
        self.enemy_monster = [] #몬스터 - 시작위치(x,y), 이동범위 (x1, x2)
        self.goal = [1166,168]


class Stage5:
    def __init__ (self):
        #플랫폼 위치 (x축 시작 지점, 발판 넓이)
        self.platform_01 = [(-100,223),(184,130),(370,543),(1063,500)] 
        self.platform_02 = [(110,93),(518,62),(638,62),(917,30)]
        self.platform_03 = [(230,30),(293,30),(359,30)]
        self.platform_04 = [(133,47),(578,62),(813,241)]
        self.platform_img = 'sprite/stage/stage_05.png'
        self.ledder = [(783,46)] # 사다리 x축, y축
        self.flower = [(142,20),(359,54),(596,20),(917,90)] # 아이템 - 꽃 x축, y축
        self.enemy_gasi = [(518,102),(870,32),(970,32)]
        self.enemy_monster = [(146,85,111,146),(1028,14,815,1053)] #몬스터 - 시작위치(x,y), 이동범위 (x1, x2)
        self.goal = [1166,168]


#적 물리치거나 아이템 먹을때의 피드백 있음 good 