class Stage1:
    def __init__ (self):
        #플랫폼 위치 (x축 시작 지점, 발판 넓이)
        self.platform_01 = [(96,194),(532,96)]
        self.platform_02 = [(176,32),(640,194),(864,96),(1000,96)]
        self.platform_01_img = 'sprite/stage/stage_01_1.png'
        self.platform_o2_img = 'sprite/stage/stage_01_2.png'
        self.ledder = [(1095,47)] # 사다리 x축, y축
        self.ledder_img = 'sprite/Ledder.png'
        self.flower = [(177,20),(448,169),(1064,20)] # 아이템 - 꽃 x축, y축
        self.flower_img = 'sprite/Flower.png'
        self.enemy_gasi = [(200,181),(798,32),(863,181),(897,181)]
        self.enemy_gasi_img = 'sprite/Enemy_gasi.png'