import pygame
import random
import pyautogui
import math
import pygame.rect
import os
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
dir_ = "scoreboard.txt" # 스코어보드를 읽어들이는 코드
scoreboard = []
scoreboardfile = open(dir_)
for scores in scoreboardfile.readlines():
    scoreboard.append (int(scores[0:-1]))
gamestartt = 0
scoreboardfile.close()

#class input

class USERINPUT : #사용자의 입력을 총괄하는 코드
    Q = 0
    W = 0
    E = 0
    R = 0
    
    Mouse = {}
    Mouse["Click"] = {"pos" : [0,0], "applied" : False}
    Mouse["Q"] = {"pos" : [0,0], "applied" : False, "cool" : True, "t" :0, "cooltime" : 2000} #쿨타임과 입력을 통제하기 위한 딕셔너리, QWER 키에 대해 제어함
    Mouse["W"] = {"pos" : [0,0], "applied" : False, "cool" : True, "t" :0, "cooltime" : 1000}
    Mouse["E"] = {"pos" : [0,0], "applied" : False, "cool" : True, "t" :0, "cooltime" : 1000}
    Mouse["R"] = {"pos" : [0,0], "applied" : False, "cool" : True, "t" :0, "cooltime" : 1000}


    def upd(): #입력을 업데이트함
        events = pygame.event.get()
        for event in events:  # 나중에 키보드 입력 함수 따로 만들기
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:  # wasd에 대해 keytense_wasd 지정
                if event.key == pygame.K_q:
                    USERINPUT.Q = 1

                    if USERINPUT.Mouse["Q"]["cool"]:
                        USERINPUT.Mouse["Q"]["cool"] = False
                        USERINPUT.Mouse["Q"]["pos"] = pygame.mouse.get_pos()
                        USERINPUT.Mouse["Q"]["applied"] = False
                        USERINPUT.Mouse["Q"]["t"] = pygame.time.get_ticks()
                elif event.key == pygame.K_w:
                    USERINPUT.W = 1

                    if USERINPUT.Mouse["W"]["cool"]:
                        USERINPUT.Mouse["W"]["cool"] = False
                        USERINPUT.Mouse["W"]["pos"] = pygame.mouse.get_pos()
                        USERINPUT.Mouse["W"]["applied"] = False
                        USERINPUT.Mouse["W"]["t"] = pygame.time.get_ticks()
                elif event.key == pygame.K_e:
                    USERINPUT.E = 1
                    if USERINPUT.Mouse["E"]["cool"]:
                        USERINPUT.Mouse["E"]["cool"] = False
                        USERINPUT.Mouse["E"]["pos"] = pygame.mouse.get_pos()
                        USERINPUT.Mouse["E"]["applied"] = False
                        USERINPUT.Mouse["E"]["t"] = pygame.time.get_ticks()
                elif event.key == pygame.K_r:
                    USERINPUT.R = 1

                    if USERINPUT.Mouse["R"]["cool"]:
                        USERINPUT.Mouse["R"]["cool"] = False
                        USERINPUT.Mouse["R"]["pos"] = pygame.mouse.get_pos()
                        USERINPUT.Mouse["R"]["applied"] = False
                        USERINPUT.Mouse["R"]["t"] = pygame.time.get_ticks()

                elif event.key == pygame.K_ESCAPE:
                    exit()
            elif event.type == pygame.KEYUP:  # wasd, 방향키가 눌리지 않았을 떄
                if event.key == pygame.K_q:
                    USERINPUT.Q = 0
                elif event.key == pygame.K_w:
                    USERINPUT.W = 0
                elif event.key == pygame.K_e:
                    USERINPUT.E = 0
                elif event.key == pygame.K_r:
                    USERINPUT.R = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                USERINPUT.Mouse["Click"]["pos"] = pygame.mouse.get_pos()
                USERINPUT.Mouse["Click"]["applied"] = False
        for keys in ["Q", "W", "E", "R"]: #쿨타임 적용
            if USERINPUT.Mouse[keys]["cool"] == False and (pygame.time.get_ticks()-USERINPUT.Mouse[keys]["t"] >= USERINPUT.Mouse[keys]["cooltime"]) :
                USERINPUT.Mouse[keys]["cool"] = True

#class - physics #init surf, pos
class Physics : #물리적인 요소들에 대한 정의  (위치, 속도, 각속도, 각도 등), 충돌, 겹침등에 대한 함수 또한 구현
    Physicslist = [] #지금까지 정의된 Physics를 다 집어넣음

    #    위치 (x, y) 와 직사각형에 대해 (x, y)를 중심으로 가지는 직사각형이 "온전히" 화면 안에 있는지의 여부 판단
    def inscreen(pos, rect):
        if pos[0] - rect.center[0] >= 0 and pos[0] + rect.center[0] <= Graphics.screen_size[0] and 0 <= pos[1] - rect.center[
            1] and \
                pos[1] + rect.center[1] <= Graphics.screen_size[1]:
            return True
        return False

    def get_center_coord(object):  # 오브젝트의 중심 반환
        return (object.physics.pos[0] - object.physics.rect.center[0], object.physics.pos[1] - object.physics.rect.center[1]) #이게 중심이 맞음?  #중심점 위치

    #init
    def __init__(self, surf: pygame.Surface, pos = (0,0), show = False): # physics - (surf, pos, vel, angle, show)
        self.rect = surf.get_rect()
        self.show = show

        self.pos = pos  # object의 pos는 center위치로 저장되어있음
        self.vel = [0, 0]
        self.acceleration = [0, 0]

        self.angle = 0
        self.ang_v = 0
        self.ang_a = 0

        self.arg = lambda x, y: True


        Physics.Physicslist.append(self)

    #충돌
    def collision(self, object):
        self_rect = self.rect  # 이후 object 의 rect를 상대위치만큼 이동시켜 줌
        # (centerx, centery) 된거니까

        # (-self.pos[0] + self_rect.centerx, -self.pos[1] + self_rect.centery)만큼 이동시킨거니까

        object_rect = object.rect
        object_rect.centerx += object.pos[0] - self.pos[0]  # + self_rect.centerx
        object_rect.centery += object.pos[1] - self.pos[1]  # + self_rect.centery
        # (true일때 부딫힘)
        val = self_rect.colliderect(object_rect) and (self.show and object.show)
        object_rect.centerx -= object.pos[0] - self.pos[0]  # + self_rect.centerx
        object_rect.centery -= object.pos[1] - self.pos[1]  # + self_rect.centery


        return val

    #벽충돌
    def wallcollision(self):  # 화면 벽과 부딪혔는지의 여부 반환
        self_rect = self.rect
        return not Physics.inscreen(self.pos, self_rect)
    #화면에서 나감?
    def outofscreen(self):  # 오브젝트가 화면 밖으로 나갔는지의 여부
        rect = self.rect
        pos = self.pos
        if pos[0] + rect.center[0] <= 0 or pos[0] - rect.center[0] >= Graphics.screen_size[0] or 0 >= pos[1] + rect.center[1] or \
                pos[1] - rect.center[1] >= Graphics.screen_size[1]:
            return True
        else:
            return False
    #움직여
    # vel 만큼 이동시켜줌
    def move(self):  # move의 vel은 단위벡터 두개
        vel = self.vel
        rect = self.rect
        next = [self.pos[0], self.pos[1]]

        next[0] += vel[0]
        next[1] += vel[1]

        if self.arg(next, rect):  # 제약 조건, 화면을 나가는 걸 허용할 지의 여부
            self.pos[0] = next[0]
            self.pos[1] = next[1]
    #돌아
    def spin(self):
        angle_ = self.ang_v / Graphics.FPS
        self.angle += angle_
    #지금까지 정의된 PHYSICS 객체에 대해, show =참이면 업데이트를 진행함 (속도, 각속도 등)
    def PHYSICS_upd():
        #속도 업데이트 하는 것 넣기
        for physics in Physics.Physicslist:
            if physics.show :
                physics.move()
                if physics.ang_v != 0:
                    physics.spin()

#Graphics
class Graphics : #Graphics. 화면 제어, 화면에 블릿하고 surface에 대한 처리 등을 함.
    width, height = pyautogui.size()
    screen_size = [width * 0.7, height * 0.8]
    width = screen_size[0]
    height = screen_size[1]
    obj_scale = 1.0
    charactersize = 3 * int(1 / 30 * width)  # 우선 가로만 맞추는걸로
    FPS = 60

    # colors\
    white = (255, 255, 255)
    sexy_pink = (245, 69, 221)
    toxic_green = (22, 241, 4)  # (0, 0, 0)#(140, 12, 80)#(1, 255, 251 )
    sexy_blue = (1, 255, 251)
    blue = (16, 34, 217)
    yello = (255, 243, 0)
    current_BG = "white"
    BG_list = {"white": pygame.image.load('./img/backgrounds/white.png')}


    def addBG(BGname, BG): #배경화면 추가
        Graphics.BG_list[BGname] = BG

    def resizeimg(surface, width):  # 이미지를 너비 기준으로 확대/축소
        rect = surface.get_rect()
        a = width / rect.width
        return pygame.transform.scale(surface, (width, rect.height * a))

    # 그림자 글씨
    def dropShadowText(screen, text, size, x, y, colour=(255, 255, 255), drop_colour=(128, 128, 128),
                       font='./public-pixel-font/arcadelit.ttf'):
        # how much 'shadow distance' is best?
        dropshadow_offset = 1 + (size // 15)
        text_font = pygame.font.Font(font, size)
        # make the drop-shadow
        text_bitmap = text_font.render(text, True, drop_colour)
        r1 = text_bitmap.get_rect()
        r1.center = (x + dropshadow_offset, y + dropshadow_offset)
        screen.blit(text_bitmap, r1)
        # make the overlay text
        text_bitmap = text_font.render(text, True, colour)
        r2 = text_bitmap.get_rect()
        r2.center = (x, y)
        screen.blit(text_bitmap, r2)

    def __init__(self): # physics - (pos, vel, angle, show, move)  / damagewp{} / attackwp{} / gameplay (charactertense, HP, init pos)
        self.surface = 0
        self.surfacedic = {}
        self.size = 100
        self.org_size = 100
        self.sizeincrement = 0

    #그래픽에 대한 변화등을 화면에 blit할때 적용함 (배경, 크기변화, 회전 rotation, position등)
    def GRAPHICS_upd():  # blit by center coordinate
        global fpstick
        fpstick += 1


        screen.blit(Graphics.resizeimg(Graphics.BG_list[Graphics.current_BG], Graphics.width * 1), (0, 0))
        for obj in  Effect.Effectlist+Character.Characterlist+Weapon.Weaponlist:
            if obj.physics.show:
                obj.graphics.size += obj.graphics.sizeincrement
                screen.blit(obj.graphics.surface, Physics.get_center_coord(obj))

                obj.graphics.surface = pygame.transform.rotate(Graphics.resizeimg(obj.graphics.surfacedic[obj.tense], obj.graphics.size), obj.physics.angle%360)

    #화면 초기 설정
    def set_screen():
        global screen, fpsClock, fpstick
        pygame.init()
        screen = pygame.display.set_mode(Graphics.screen_size)
        fpsClock = pygame.time.Clock()
        fpstick = 0

        pygame.display.set_caption('Jammin likes Jumin')
        jam_face_icon = pygame.image.load('./img/icon/jam_face.jpg')
        pygame.display.set_icon(jam_face_icon)

        pygame.mixer.init()

class attack : #attack 에 대해서 정의함
    def __init__(self, attackbool = False, attackpos = (0, 0), destinationpos = (0,0), intensity = 0):
        self.attackbool = attackbool # attack이 진행되고 있는지
        self.attackpos = attackpos #attack이 시작된 위치
        self.destinationpos = destinationpos # 발사 각도
        self.intensity = intensity # 발사 강도
        self.attackapplied = False #attack이 적용되었는가?
        self.attackcharacter = False #attack을 진행한 character가 누구인가

#class - weapon
class Weapon :
    Weaponlist = [] #지금까지 정의된 무기
    #throw, fly, hit, miss
    def __init__(self): #physics, graphics, effects, 이것에 대한 제어를 담은 physics_ctrls까지 담아서 선언함
        self.physics = 0
        self.physics_ctrls = {}
        self.graphics = Graphics()
        self.damage_cnst = 10
        self.tense = False
        self.effects = {}
        self.attackinf = attack()

        self.damagechk = False
        self.damagelogic = 0

        self.gifspeed = -1

        Weapon.Weaponlist.append(self)

    def collide (self) : #데미지를 입을 수 있는 상대와 접촉 했는가 ? (어딘가 맞았는지 여부, "hit")으로 리턴
        for character in Character.Characterlist:
            if character == self.attackinf.attackcharacter :
                continue
            if self.physics.collision(character.physics): #충돌했다면
                if self in character.damagewp:
                    return True
        return False

    def attack (self, attackpos : list, destinationpos : list, attackcharacter, intensity : int = 100): #날라가고, 충돌 대상과 intensity 전달
        if self.attackinf.attackbool == False:

            self.attackinf = attack(True, attackpos, destinationpos, intensity)
            self.attackinf.attackapplied = False
            self.attackinf.attackcharacter = attackcharacter
            self.physics.pos = attackpos
    #무기 업데이트
    def WEAPON_upd():
        for wpn in Weapon.Weaponlist:
            if wpn.attackinf.attackbool :
                wpn.physics.show =True
            else :
                wpn.physics.show = False
                continue
            wpn_collide = wpn.collide()


            if wpn_collide and wpn.attackinf.attackbool: #hit
                wpn.physics_ctrls["hit"](wpn)
            elif wpn.physics.outofscreen(): #self.attack= (True, attackpos, intensity) #fly

                wpn.physics_ctrls["out"](wpn)
            elif wpn.attackinf.attackbool :
                wpn.physics_ctrls["fly"](wpn)

            if wpn.attackinf.attackbool == False :
                wpn.damagechk = False

            if wpn.gifspeed != -1 and wpn.attackinf.attackbool == True:
                if not fpstick % wpn.gifspeed :
                    wpn.tense+=1
                    if wpn.tense == len(wpn.graphics.surfacedic):
                        wpn.attackinf.attackbool = False
                        wpn.tense = 0
                        wpn.damagechk = False

    #슬리퍼 제어
    def dmglgc_slipper (character, wpn) :
        character.HP -= wpn.damage_cnst * wpn.attackinf.intensity//100
        global Sounds
        if id(character) in [id(Jammin) , id(Billy), id(Bodyguard), id(Bodyguard_2)] :
            Sounds["oof"].play()
        elif id(character) == id(Loopy) :
            Sounds["loopyhit"].play()
        character.damage["cool"] = False
        character.damage["t"] = pygame.time.get_ticks()
        character.damage["character"] = wpn.attackinf.attackcharacter

    #Yell 제어
    def dmglgc_yell(character, wpn) :
        if wpn.damagechk == False :
            wpn.damagechk = True
            character.HP -= wpn.damage_cnst * wpn.attackinf.intensity//100
            if id(character) == id(Jammin):
                Sounds["oof"].play()
            elif id(character) == id(Loopy):
                Sounds["loopyhit"].play()
            character.damage["cool"] = False
            character.damage["t"] = pygame.time.get_ticks()
            character.damage["character"] = character
            if id(character) == id(Loopy) :
                Loopy.tense = "angry"

    #빌리 제어
    def dmglgc_gay(character, wpn):
        if wpn.damagechk == False :
            wpn.damagechk = True

            x = Billy.physics.pos[0] - character.physics.pos[0]
            y = Billy.physics.pos[1] - character.physics.pos[1]
            size = (x**2 + y**2)**0.5
            multiplier = 1

            character.physics.pos[0] += x*multiplier*(size/Graphics.width)
            character.physics.pos[1] += y*multiplier*(size/Graphics.width)

            Sounds["throw"].play()
            character.physics.vel = [0,0]

            x = Billy.physics.pos[0] - character.physics.pos[0]
            y = Billy.physics.pos[1] - character.physics.pos[1]
            size = (x ** 2 + y ** 2) ** 0.5

            if size <= 300:
                character.HP -= wpn.damage_cnst * wpn.attackinf.intensity//100
                Sounds["oof"].play()
                character.damage["cool"] = False
                character.damage["t"] = pygame.time.get_ticks()
                character.damage["character"] = character
    def dmglgc_ICE(character, wpn): #얼음제어
        if wpn.damagechk == False :
            wpn.damagechk = True

            character.HP -= wpn.damage_cnst * wpn.attackinf.intensity // 100
            Sounds["oof"].play()
            character.damage["cool"] = False
            character.damage["t"] = pygame.time.get_ticks()
            character.damage["character"] = character
class Character: #캐릭터 선언

    Characterlist = []

    # throw, fly, hit, miss
    def __init__(self):
        self.physics = 0
        self.physics_ctrls = lambda x : True
        self.graphics = Graphics()
        self.HP = 100
        self.damagewp = []
        self.attackwp = []
        self.tense = "default"
        self.initpos = (0,0)
        self.effects = {}

        self.damage = {"cool": True, "t": 0, "cooltime": 1000, "character" : 0}
        self.deathapply = False
        self.deathfinish = False
        self.throwed = False
        Character.Characterlist.append(self)

    #다 숨기기
    def hideall () :
        for char in Character.Characterlist:
            char.physics.show = False
    #부딫힘?
    def collide(self):
        for wpn in self.damagewp:
            if (self.physics.collision(wpn.physics)): #충돌했다면
                wpn.damagelogic(self, wpn)
                #effect 지랄 염병
    #업데이트 해
    def CHARACTER_upd():
        for character in Character.Characterlist:
            if character.HP > 0 and character.physics.show == True:
                character.collide()
                if not (character.throwed):
                    character.physics_ctrls(character)
                if not character.damage["cool"]:
                    character.tense = "damage"

                if pygame.time.get_ticks() - character.damage["t"] >= character.damage["cooltime"] and character.tense == "damage":
                    character.damage["cool"] = True
                    character.tense = "default"
                    if id(character) == id(Loopy) and character:
                        character.tense = "angry"
                if character.throwed :
                    if character.physics.outofscreen():
                        character.physics.vel = [0, 0]
                        character.physics.ang_v = 0
                        character.physics.angle = 0
                        character.physics.pos = [Graphics.width // 2, Graphics.height // 2]
                        character.physics.arg = lambda x, y: True
                        character.throwed = False
                        character.tense = "default"

            if character.HP <= 0 and character.physics.show == True:
                Effect.dyingeffect(character)

    #던지기
    def throw(self, character):
        if self.throwed == False :
            self.tense = "damage"
            self.throwed= True
            self.physics.vel = PhysicsControl.cal_vel(character.physics.pos, self.physics.pos, 25)
            self.physics.ang_v = 400
            if self.physics.vel[0] ==0 and self.physics.vel[1] == 0 :
                self.physics.vel = [25, 0]
            self.physics.arg = lambda x, y : True

#제어
class PhysicsControl :
    shatterinf = {"bool" : False, "t" : 0, "cooltime" : 1000}
    loveinf= {"bool" : False, "t" : 0, "cooltime" : 1000}
    bloodinf = {"bool": False, "t": 0, "cooltime": 1000}
    bloodinf2 = {"bool": False, "t": 0, "cooltime": 1000}
#한 점에서 다른점으로 향해 가는 속도 벡터
    def cal_vel(pos, coordinate, vel):
        x = coordinate[0] - pos[0]
        y = coordinate[1] - pos[1]

        size = int ((x**2 + y **2)**0.5)

        if size == 0 :
            return [0, 0]

        return [int(vel*x/size), int(vel*y/size)] #
#한점에서 다른점으로 향해 가는 벡터의 편각
    def cal_angle(pos1, pos2):
        x = pos2[0] - pos1[0]
        y = -(pos2[1] - pos1[0])




        if x== 0 :
            if y > 0:
                return 90
            elif y <0 :
                return 270
            else :
                return 0


        elif x > 0 :

            atan = math.degrees(math.atan(y / x))
            if atan >= 0 :
                return atan
            elif atan <0 :
                return atan + 360
        elif x < 0:

            atan = math.degrees(math.atan(y / x))
            return atan + 180
    #재민이 컨트롤
    def LOL_JAM_ctrl (character : Character): #이거 obj로 잡아야 할것 같은데 일단 character 다 만들고 하기
        global Sounds, Slipper
        if not USERINPUT.Mouse["Click"]["applied"] and USERINPUT.Mouse["Q"]["cool"]:
            vel = 10 # 나중에 꼭 바꿔 씨발아

            character.physics.vel = PhysicsControl.cal_vel(character.physics.pos ,USERINPUT.Mouse["Click"]["pos"], vel)
            USERINPUT.Mouse["Click"]["applied"] = True
            USERINPUT.Mouse["R"]["cool"] = True

        mouseblocksize = 120
        mouseblock = pygame.Rect((USERINPUT.Mouse["Click"]["pos"][0]-mouseblocksize//2, USERINPUT.Mouse["Click"]["pos"][1]-mouseblocksize//2), (mouseblocksize, mouseblocksize))

        if mouseblock.collidepoint(character.physics.pos):
            character.physics.vel = [0,0]
        #추가 구현 : dash, 고함, 등 꼴리는대로 구

        if USERINPUT.Mouse["Q"]["cool"] and USERINPUT.Mouse["R"]["cool"]:
            character.tense = "default"
            fire.activated = False
            Sounds["jamminscream"].stop()
        elif not USERINPUT.Mouse["Q"]["cool"] and not USERINPUT.Mouse["Q"]["applied"]:
            character.physics.vel = [0,0]
            USERINPUT.Mouse["Q"]["applied"] = True
            character.tense = "angry"
            fire.activated = True
            fire.physics.pos = [character.physics.pos[0], character.physics.pos[1] -50]
            global Yell
            Yell.attack([character.physics.pos[0], character.physics.pos[1]], USERINPUT.Mouse["Q"]["pos"], character)
            Sounds["jamminscream"].play()

        if USERINPUT.W and Slipper.attackinf.attackbool == False and USERINPUT.Mouse["W"]["applied"] == False:

            USERINPUT.Mouse["W"]["applied"] = True
            Slipper.attack([character.physics.pos[0], character.physics.pos[1]], USERINPUT.Mouse["W"]["pos"], character)
            Sounds["throw"].play()

        elif not USERINPUT.Mouse["R"]["cool"] and not USERINPUT.Mouse["R"]["applied"]:
            character.tense = "dash"
            if USERINPUT.Mouse["Click"]["pos"][0] >= character.physics.pos[0] :
                character.tense += "R"
            else :
                character.tense += "L"


            character.physics.vel = [character.physics.vel[0]*3, character.physics.vel[1]*3]
            USERINPUT.Mouse["R"]["applied"] = True

        if Jammin.HP <= 0 :
            fire.activated = False
    #루피 컨트롤, 밑에 쭉 캐릭터 컨트롤
    def NPC_LOOPY_ctrl (character : Character):
        if character.tense == "default":

            ranpos = [-500,-500]

            if not fpstick%60:
                if random.randint(0,2) == 1:
                    vel = 6 # 나중에 꼭 바꿔 씨발아
                    ranpos = [random.randint(0, Graphics.screen_size[0]//3), random.randint(0, Graphics.screen_size[1]//3)]

                    character.physics.vel = PhysicsControl.cal_vel(character.physics.pos ,ranpos, vel)
                else :
                    vel = [0,0]
                    character.physics.vel = vel

            mouseblocksize = 120
            mouseblock = pygame.Rect((ranpos[0]-mouseblocksize//2, ranpos[1]-mouseblocksize//2), (mouseblocksize, mouseblocksize))

            if mouseblock.collidepoint(character.physics.pos):
                character.physics.vel = [0,0]

        elif character.tense == "angry" :
            vel = 6  # 나중에 꼭 바꿔 씨발아
            character.physics.vel = PhysicsControl.cal_vel(character.physics.pos, Jammin.physics.pos, vel)

            if  abs(character.physics.vel[0]) >= abs(character.physics.vel[1]) :
                character.physics.vel[1] = 0
            else :
                character.physics.vel[0] = 0

        if not fpstick%60:
            global Mirror
            if random.randint(0,2) == 1 and character.tense == "angry" and not Mirror.attackinf.attackbool:
                global Sounds
                Sounds["loopythrow"].play()
                Mirror.attack([character.physics.pos[0], character.physics.pos[1]], [Jammin.physics.pos[0], Jammin.physics.pos[1]], character)
    def NPC_Billy_ctrl (character : Character):

        if character.tense == "default":
            ranpos = [-500,-500]

            if not fpstick%60:
                if random.randint(0,2) == 1:
                    vel = 6 # 나중에 꼭 바꿔 씨발아
                    ranpos = [random.randint(0, int(Graphics.screen_size[0]*0.8)), random.randint(0, int(Graphics.screen_size[1]*0.8))]
                    character.physics.vel = PhysicsControl.cal_vel(character.physics.pos ,ranpos, vel)
                else :
                    vel = [0,0]
                    character.physics.vel = vel

            mouseblocksize = 120
            mouseblock = pygame.Rect((ranpos[0]-mouseblocksize//2, ranpos[1]-mouseblocksize//2), (mouseblocksize, mouseblocksize))

            if mouseblock.collidepoint(character.physics.pos):
                character.physics.vel = [0,0]

        if not fpstick%60:
            global And #mirror 말고 하트?
            if random.randint(0,2) == 1 and Ang.attackinf.attackbool == False:
                global Sounds
                Sounds["throw"].play()
                Ang.attack([character.physics.pos[0], character.physics.pos[1]],
                              [Jammin.physics.pos[0], Jammin.physics.pos[1]], character)
    def NPC_Bodyguard_ctrl (character : Character):

        vel = 6  # 나중에 꼭 바꿔 씨발아
        character.physics.vel = PhysicsControl.cal_vel(character.physics.pos, Jammin.physics.pos, vel)

        if  abs(character.physics.vel[0]) >= abs(character.physics.vel[1]) :
            character.physics.vel[1] = 0
        else :
            character.physics.vel[0] = 0

        character.physics.vel[0] += random.randint(-10, 10)
        character.physics.vel[1] += random.randint(-10, 10)

        if not fpstick%60:
            global Bullet
            if random.randint(0,4) != 1 and not Bullet.attackinf.attackbool:
                global Sounds
                Sounds["gunshot"].set_volume(0.3)
                Sounds["gunshot"].play()
                Bullet.attack([character.physics.pos[0], character.physics.pos[1]], [Jammin.physics.pos[0], Jammin.physics.pos[1]], character)
    def NPC_Bodyguard_2_ctrl (character : Character):
        vel = 6  # 나중에 꼭 바꿔 씨발아
        character.physics.vel = PhysicsControl.cal_vel(character.physics.pos, Jammin.physics.pos, vel)

        character.physics.vel[0] += random.randint(-10, 10)
        character.physics.vel[1] += random.randint(-10, 10)

        if abs(character.physics.vel[0]) >= abs(character.physics.vel[1]):
            character.physics.vel[1] = 0
        else:
            character.physics.vel[0] = 0

        if not fpstick % 60:
            global Bullet_2
            if random.randint(0, 4) != 1 and not Bullet_2.attackinf.attackbool:
                global Sounds
                Sounds["gunshot"].set_volume(0.3)
                Sounds["gunshot"].play()
                Bullet_2.attack([character.physics.pos[0], character.physics.pos[1]],
                              [Jammin.physics.pos[0], Jammin.physics.pos[1]], character)
    def NPC_Dongsuk_ctrl (character : Character):
        if not fpstick %3:
            vel = 6  # 나중에 꼭 바꿔 씨발아
            character.physics.vel = PhysicsControl.cal_vel(character.physics.pos, Jammin.physics.pos, vel)

            if  abs(character.physics.vel[0]) >= abs(character.physics.vel[1]) :
                character.physics.vel[1] = 0
            else :
                character.physics.vel[0] = 0

        x = Jammin.physics.pos[0] - character.physics.pos[0]
        y = Jammin.physics.pos[1] - character.physics.pos[1]
        distance = (x ** 2 + y ** 2) ** 0.5

        if distance <= 100 and Jammin.throwed == False:
            character.tense = "punch"
            Jammin.throw(character)
        else :
            character.tense = "default"
    def NPC_Karina_ctrl (character : Character):

        global Sounds
        #random.move, Jammin 근처로

        if not fpstick%20 and random.randint(0, 3) == 0:
            distance = random.randint(100, 200)
            dpos = PhysicsControl.cal_vel([0, 0], [random.randint(-10, 10), random.randint(-10, 10)], distance)
            Sounds["shuk"].play()
            character.physics.pos = [Jammin.physics.pos[0]-dpos[0], Jammin.physics.pos[1]-dpos[1]]
            global ICE
            if random.randint(0,2) == 1 and not ICE.attackinf.attackbool:
                Sounds["he"].play()
                ICE.attack([character.physics.pos[0], character.physics.pos[1]], [Jammin.physics.pos[0], Jammin.physics.pos[1]], character)
    #선형운동 + 회전
    def linear_spin(obj, vel, ang_v): # obj는 weapon, character 둘다 됨
        obj.physics.vel = vel
        obj.physics.ang_v = ang_v
    #무기 선형운동 +회전
    def wpn_linear_spin(wpn):  # obj는 weapon, character 둘다 됨
        if wpn.attackinf.attackapplied ==False :
            wpnvel = 25
            wpn.physics.show = True
            wpn.physics.vel = PhysicsControl.cal_vel(wpn.attackinf.attackpos, wpn.attackinf.destinationpos, wpnvel)
            wpn.physics.ang_v = 500

            wpn.attackinf.attackapplied = True
    #Yell.physics_ctrls = {"fly": PhysicsControl.expand_linear_spin, "hit": PhysicsControl.expand_linear_spin, "out" : PhysicsControl.out}
    #커지면서 선형운동 + 회전
    def expand_linear_spin(obj, vel, ang_v, expansion):
        obj.graphics.size += expansion
        obj.physics.vel = vel
        obj.physics.ang_v = ang_v
    #무기 커지면서 선형운동 + 회전
    def wpn_expand_linear_spin(wpn):
        if wpn.attackinf.attackapplied ==False :
            wpnvel = 25
            wpn.physics.show = True
            wpn.graphics.sizeincrement = 5
            wpn.physics.vel = PhysicsControl.cal_vel(wpn.attackinf.attackpos, wpn.attackinf.destinationpos, wpnvel)
            wpn.physics.ang_v = 500

            wpn.attackinf.attackapplied = True
    #무기 선형 운동
    def wpn_linear(wpn):  # obj는 weapon, character 둘다 됨
        if wpn.attackinf.attackapplied ==False :
            wpnvel = 25
            wpn.physics.show = True
            wpn.physics.vel = PhysicsControl.cal_vel(wpn.attackinf.attackpos, wpn.attackinf.destinationpos, wpnvel)

            wpn.attackinf.attackapplied = True
    def out(obj): #화면을 나간 무기에 대한 처리
        obj.graphics.size =obj.graphics.org_size
        obj.physics.vel = [0,0]
        obj.physics.ang_v = 0
        obj.physics.show = False
        obj.attackinf.attackbool = False
    def shatter(obj):#거울 박살효과
        if PhysicsControl.shatterinf["bool"] == False :
            PhysicsControl.shatterinf["bool"] = True
            PhysicsControl.shatterinf["t"] = pygame.time.get_ticks()
            obj.graphics.size = obj.graphics.org_size
            obj.tense = "mirrorshatter"
            obj.physics.vel = [0, 0]
            obj.physics.ang_v = 0
            global Sounds
            Sounds["shatter"].play()
    def blood(obj): #총기 피 효과
        if PhysicsControl.bloodinf["bool"] == False :
            PhysicsControl.bloodinf["bool"] = True
            PhysicsControl.bloodinf["t"] = pygame.time.get_ticks()
            obj.graphics.size = obj.graphics.org_size
            obj.tense = "blood"
            obj.physics.vel = [0, 0]
            obj.physics.ang_v = 0
            global Sounds
            Sounds["oof"].play()
    def blood2(obj):
        if PhysicsControl.bloodinf2["bool"] == False :
            PhysicsControl.bloodinf2["bool"] = True
            PhysicsControl.bloodinf2["t"] = pygame.time.get_ticks()
            obj.graphics.size = obj.graphics.org_size
            obj.tense = "blood"
            obj.physics.vel = [0, 0]
            obj.physics.ang_v = 0
            global Sounds
            Sounds["oof"].play()
    def love(obj): #빌리 사랑효과
        if PhysicsControl.loveinf["bool"] == False :
            PhysicsControl.loveinf["bool"] = True
            PhysicsControl.loveinf["t"] = pygame.time.get_ticks()
            obj.graphics.size = obj.graphics.org_size
            obj.tense = "love"
            obj.physics.vel = [0, 0]
            obj.physics.ang_v = 0
            global Sounds
            Sounds["ang"].play()
    def ICEctrl(obj : Weapon) : # 얼음 컨트롤
        if obj.attackinf.attackbool and not obj.attackinf.attackapplied:
            obj.attackinf.attackapplied = True
            obj.attackinf.destinationpos = [Jammin.physics.pos[0], Jammin.physics.pos[1]]
            obj.attackinf.attackpos = [Karina.physics.pos[0], Karina.physics.pos[1]]
            dpos = PhysicsControl.cal_vel(obj.attackinf.attackpos, obj.attackinf.destinationpos, 300)
            dangle = PhysicsControl.cal_angle(obj.attackinf.attackpos, obj.attackinf.destinationpos)

            ICE.physics.angle = dangle-90
            ICE.physics.pos = [obj.attackinf.attackpos[0] + dpos[0], obj.attackinf.attackpos[1] + dpos[1]]
    def PHYCTRL_upd():
        if (pygame.time.get_ticks()- PhysicsControl.shatterinf["t"] >= PhysicsControl.shatterinf["cooltime"]) and Mirror.tense == "mirrorshatter":

            Mirror.attackinf.attackbool = False
            Mirror.tense = "default"
            PhysicsControl.shatterinf["bool"] = False

        if (pygame.time.get_ticks()- PhysicsControl.loveinf["t"] >= PhysicsControl.loveinf["cooltime"]) and Ang.tense == "love":

            Ang.attackinf.attackbool = False
            Ang.tense = "default"
            PhysicsControl.loveinf["bool"] = False


        if (pygame.time.get_ticks()- PhysicsControl.bloodinf["t"] >= PhysicsControl.bloodinf["cooltime"]) and Bullet.tense == "blood":

            Bullet.attackinf.attackbool = False
            Bullet.tense = "default"
            PhysicsControl.bloodinf["bool"] = False
        if (pygame.time.get_ticks() - PhysicsControl.bloodinf2["t"] >= PhysicsControl.bloodinf2[
            "cooltime"]) and Bullet_2.tense == "blood":
            Bullet_2.attackinf.attackbool = False
            Bullet_2.tense = "default"
            PhysicsControl.bloodinf2["bool"] = False

class Effect : #이펙트 gif 등
    Effectlist = []

    def __init__(self):
        self.physics = 0
        self.graphics = Graphics()
        self.tense = 0
        self.gifspeed = 5
        self.activated = False

        Effect.Effectlist.append(self)

    def EFFECT_upd():
        global fpstick
        for effect in Effect.Effectlist:
            if effect.activated :
                effect.physics.show = True
                effect.tense = (fpstick//(effect.gifspeed))% len(effect.graphics.surfacedic)
            else :
                effect.physics.show = False

    def dyingeffect (character : Character) : #죽고 난 다음엔 init을 꼭 다시 때려줄 것

        if not character.physics.outofscreen(): #나갈때까지 굴림
            if character.deathapply == False :
                character.deathapply = True
                character.physics.arg = lambda x, y : True
                character.tense = "damage"

                character.physics.vel= [0,10]
                character.physics.ang_v = 400
                if id(character) == id(Jammin):
                    Sounds["oooooof"].play()
                elif id(character) == id(Loopy):
                    Sounds["loopydie"].play()
        else :
            character.physics.show = False
            character.physics.vel = [0,0]
            character.physics.ang_v = 0
            character.deathfinish = True

class initobj : #모든 초기화 함수
    def init_jammin():
        global Jammin
        Jammin = Character()

        Jammin.graphics = Graphics()
        Jammin.graphics.size = 150
        res = []
        dir_path = "./img/JAMMIN"
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)

        for p in res:
            path = dir_path + '/' + p
            Jammin.graphics.surfacedic[p[7:-4]] = Graphics.resizeimg(pygame.image.load(path), Jammin.graphics.size)
        Jammin.graphics.surface = Jammin.graphics.surfacedic["default"]

        Jammin.physics = Physics(surf = Jammin.graphics.surfacedic["default"], show = True)
        Jammin.physics.pos = [300, 300]
        Jammin.physics_ctrls = PhysicsControl.LOL_JAM_ctrl
        Jammin.physics.arg = lambda x, y: Physics.inscreen(x, y)

        Jammin.HP = 100
        Jammin.damagewp = [Mirror, Ang, Bullet, Bullet_2, ICE]
        Jammin.attackwp = [Slipper, Yell] # [Badminton]
        Jammin.tense = "default"
        Jammin.initpos = (0,0)
    def init_Loopy():
        global Loopy
        Loopy = Character()

        Loopy.graphics = Graphics()
        Loopy.graphics.size = 100
        res = []
        dir_path = "./img/loopy"
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)

        for p in res:
            path = dir_path + '/' + p
            Loopy.graphics.surfacedic[p[6:-4]] = Graphics.resizeimg(pygame.image.load(path), Loopy.graphics.size)
        Loopy.graphics.surface = Loopy.graphics.surfacedic["default"]
        Loopy.physics = Physics(surf = Loopy.graphics.surfacedic["default"], show = False)
        Loopy.physics.pos = [Graphics.width//2, Graphics.height//2]
        Loopy.physics_ctrls = PhysicsControl.NPC_LOOPY_ctrl
        Loopy.physics.arg = lambda x, y: Physics.inscreen(x, y)


        Loopy.HP = 30
        Loopy.damagewp = [Slipper, Yell]
        Loopy.attackwp = [Mirror] # [Badminton]
        Loopy.tense = "default"
        Loopy.initpos = (0,0)
    def init_Billy():
        global Billy
        Billy = Character()

        Billy.graphics = Graphics()
        Billy.graphics.size = 100
        res = []
        dir_path = "./img/Billy"
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)

        for p in res:
            path = dir_path + '/' + p
            Billy.graphics.surfacedic[p[6:-4]] = Graphics.resizeimg(pygame.image.load(path), Billy.graphics.size)
        Billy.graphics.surface = Billy.graphics.surfacedic["default"]
        Billy.physics = Physics(surf = Billy.graphics.surfacedic["default"], show = False)
        Billy.physics.pos = [300, 300]
        Billy.physics_ctrls = PhysicsControl.NPC_Billy_ctrl
        Billy.physics.arg = lambda x, y: Physics.inscreen(x, y)

        Billy.HP = 100
        Billy.damagewp = [Slipper, Yell]
        Billy.attackwp = [] # [Badminton]
        Billy.tense = "default"
        Billy.initpos = (0,0)
    def init_Bodyguard():
        global Bodyguard
        Bodyguard = Character()

        Bodyguard.graphics = Graphics()
        Bodyguard.graphics.size = 100
        res = []
        dir_path = "./img/Bodyguard"
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)

        for p in res:
            path = dir_path + '/' + p
            Bodyguard.graphics.surfacedic[p[10:-4]] = Graphics.resizeimg(pygame.image.load(path), Bodyguard.graphics.size)
        Bodyguard.graphics.surface = Bodyguard.graphics.surfacedic["default"]
        Bodyguard.physics = Physics(surf = Bodyguard.graphics.surfacedic["default"], show = False)
        Bodyguard.physics.pos = [900, 300]
        Bodyguard.physics_ctrls = PhysicsControl.NPC_Bodyguard_ctrl
        Bodyguard.physics.arg = lambda x, y: Physics.inscreen(x, y)

        Bodyguard.HP = 40
        Bodyguard.damagewp = [Slipper, Yell]
        Bodyguard.attackwp = [Bullet] # [Badminton]
        Bodyguard.tense = "default"
        Bodyguard.initpos = (0,0)
    def init_Bodyguard_2():
        global Bodyguard_2
        Bodyguard_2 = Character()

        Bodyguard_2.graphics = Graphics()
        Bodyguard_2.graphics.size = 100
        res = []
        dir_path = "./img/Bodyguard"
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)

        for p in res:
            path = dir_path + '/' + p
            Bodyguard_2.graphics.surfacedic[p[10:-4]] = Graphics.resizeimg(pygame.image.load(path), Bodyguard_2.graphics.size)
        Bodyguard_2.graphics.surface = Bodyguard_2.graphics.surfacedic["default"]
        Bodyguard_2.physics = Physics(surf=Bodyguard_2.graphics.surfacedic["default"])
        Bodyguard_2.physics.pos = [300, 300]
        Bodyguard_2.physics_ctrls = PhysicsControl.NPC_Bodyguard_2_ctrl
        Bodyguard_2.physics.arg = lambda x, y: Physics.inscreen(x, y)

        Bodyguard_2.HP = 40
        Bodyguard_2.damagewp = [Slipper, Yell]
        Bodyguard_2.attackwp = [Bullet_2]  # [Badminton]
        Bodyguard_2.tense = "default"
        Bodyguard_2.initpos = (0, 0)
    def init_Dongsuk():
        global Dongsuk
        Dongsuk = Character()

        Dongsuk.graphics = Graphics()
        Dongsuk.graphics.size = 100
        res = []
        dir_path = "./img/Dongsuk"
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)

        for p in res:
            path = dir_path + '/' + p
            Dongsuk.graphics.surfacedic[p[8:-4]] = Graphics.resizeimg(pygame.image.load(path), Dongsuk.graphics.size)
        Dongsuk.graphics.surface = Dongsuk.graphics.surfacedic["default"]
        Dongsuk.physics = Physics(surf=Dongsuk.graphics.surfacedic["default"])
        Dongsuk.physics.pos = [300, 300]
        Dongsuk.physics_ctrls = PhysicsControl.NPC_Dongsuk_ctrl
        Dongsuk.physics.arg = lambda x, y: Physics.inscreen(x, y)

        Dongsuk.HP = 100
        Dongsuk.damagewp = [Slipper, Yell]
        Dongsuk.attackwp = []  # [Badminton]
        Dongsuk.tense = "default"
        Dongsuk.initpos = (0, 0)
    def init_Karina():
        global Karina
        Karina = Character()

        Karina.graphics = Graphics()
        Karina.graphics.size = 100
        res = []
        dir_path = "./img/Karina"
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)

        for p in res:
            path = dir_path + '/' + p
            Karina.graphics.surfacedic[p[7:-4]] = Graphics.resizeimg(pygame.image.load(path), Karina.graphics.size)
        Karina.graphics.surface = Karina.graphics.surfacedic["default"]
        Karina.physics = Physics(surf=Karina.graphics.surfacedic["default"])
        Karina.physics.pos = [300, 300]
        Karina.physics_ctrls = PhysicsControl.NPC_Karina_ctrl
        Karina.physics.arg = lambda x, y: Physics.inscreen(x, y)

        Karina.HP = 100
        Karina.damagewp = [Slipper, Yell]
        Karina.attackwp = [Mirror]  # [Badminton]
        Karina.tense = "default"
        Karina.initpos = (0, 0)

    def init_Jumin():
        global Jumin
        Jumin = Character()
        Jumin.deathfinish = True

        Jumin.graphics = Graphics()
        Jumin.graphics.size = 150

        path = "./img/juminface.png"
        Jumin.graphics.surface = Jumin.graphics.surfacedic["default"] = Graphics.resizeimg(pygame.image.load(path), Jumin.graphics.size)

        Jumin.physics = Physics(surf = Jumin.graphics.surfacedic["default"])
        Jumin.physics.pos = [300, 300]
        Jumin.HP = 100
        Jumin.tense = "default"
    #"STAGE 2 : Billie" : [Billie], "STAGE 3 : Bodyguards" : [Bodyguard1, Bodyguard2], "STAGE 4 : Dongsuk" : [Dongsuk], "BOSS STAGE : Karina" : [Karina]
    def init_yell () :
        global Yell
        Yell = Weapon()

        Yell.physics_ctrls = {"fly": PhysicsControl.wpn_expand_linear_spin, "hit": PhysicsControl.wpn_expand_linear_spin, "out" : PhysicsControl.out}

        Yell.graphics = Graphics()
        Yell.graphics.size = 150

        Yell.graphics.surface = Yell.graphics.surfacedic["default"] = Graphics.resizeimg(pygame.image.load("./img/yell/yell.png"), Yell.graphics.size)

        Yell.physics = Physics(surf=Yell.graphics.surfacedic["default"], show=False)
        Yell.physics.pos = [300, 300]
        Yell.tense = "default"
        Yell.damage_cnst = 10
        Yell.damagelogic = Weapon.dmglgc_yell
    def init_slipper () :
        global Slipper
        Slipper = Weapon()

        Slipper.physics_ctrls = {"fly": PhysicsControl.wpn_linear_spin, "hit": PhysicsControl.out, "out" : PhysicsControl.out}

        Slipper.graphics = Graphics()
        Slipper.graphics.size = 30
        Slipper.graphics.org_size = 30

        Slipper.graphics.surface = Slipper.graphics.surfacedic["default"] = Graphics.resizeimg(pygame.image.load("./img/Slipper.png"), Slipper.graphics.size)

        Slipper.physics = Physics(surf=Slipper.graphics.surfacedic["default"], show=False)
        Slipper.physics.pos = [300, 300]
        Slipper.tense = "default"
        Slipper.damage_cnst = 10

        Slipper.damagelogic= Weapon.dmglgc_slipper
    def init_mirror () :
        global Mirror
        Mirror = Weapon()

        Mirror.physics_ctrls = {"fly": PhysicsControl.wpn_linear_spin, "hit": PhysicsControl.shatter, "out" : PhysicsControl.out}

        Mirror.graphics = Graphics()
        Mirror.graphics.size = 100
        Mirror.graphics.org_size = 100

        Mirror.graphics.surface = Mirror.graphics.surfacedic["default"] = Graphics.resizeimg(pygame.image.load("./img/mirror/mirror.png"), Mirror.graphics.size)
        Mirror.graphics.surfacedic["mirrorshatter"] = Graphics.resizeimg(pygame.image.load("./img/mirror/mirrorshatter.png"),Mirror.graphics.size*2)

        Mirror.physics = Physics(surf=Mirror.graphics.surfacedic["default"], show=False)
        Mirror.physics.pos = [300, 300]
        Mirror.tense = "default"
        Mirror.damage_cnst = 10

        Mirror.damagelogic= Weapon.dmglgc_yell
    def init_ang():
        global Ang
        Ang = Weapon()

        Ang.physics_ctrls = {"fly": PhysicsControl.wpn_linear, "hit": PhysicsControl.love,
                                "out": PhysicsControl.out}

        Ang.graphics = Graphics()
        Ang.graphics.size = 100
        Ang.graphics.org_size = 100

        Ang.graphics.surface = Ang.graphics.surfacedic["default"] = Graphics.resizeimg(
            pygame.image.load("./img/ang.png"), Ang.graphics.size)
        Ang.graphics.surfacedic["love"] = Graphics.resizeimg(
            pygame.image.load("./img/lovebilly.png"), Ang.graphics.size * 2)

        Ang.physics = Physics(surf=Ang.graphics.surfacedic["default"], show=False)
        Ang.physics.pos = [500, 500]
        Ang.tense = "default"
        Ang.damage_cnst = 10

        Ang.damagelogic = Weapon.dmglgc_gay

    def init_bullet():
        global Bullet
        Bullet = Weapon()

        Bullet.physics_ctrls = {"fly": PhysicsControl.wpn_linear_spin, "hit": PhysicsControl.blood,
                                "out": PhysicsControl.out}

        Bullet.graphics = Graphics()
        Bullet.graphics.size = 100
        Bullet.graphics.org_size = 100

        Bullet.graphics.surface = Bullet.graphics.surfacedic["default"] = Graphics.resizeimg(
            pygame.image.load("./img/Bodyguard/Bodyguard_bullet.png"), Bullet.graphics.size)
        Bullet.graphics.surfacedic["blood"] = Graphics.resizeimg(
            pygame.image.load("./img/Bodyguard/Bodyguard_blood.png"), Bullet.graphics.size * 2)

        Bullet.physics = Physics(surf=Bullet.graphics.surfacedic["default"], show=False)
        Bullet.physics.pos = [300, 300]
        Bullet.tense = "default"
        Bullet.damage_cnst = 5

        Bullet.damagelogic = Weapon.dmglgc_yell
    def init_bullet_2():
        global Bullet_2
        Bullet_2 = Weapon()

        Bullet_2.physics_ctrls = {"fly": PhysicsControl.wpn_linear_spin, "hit": PhysicsControl.blood2,
                                "out": PhysicsControl.out}

        Bullet_2.graphics = Graphics()
        Bullet_2.graphics.size = 100
        Bullet_2.graphics.org_size = 100

        Bullet_2.graphics.surface = Bullet_2.graphics.surfacedic["default"] = Graphics.resizeimg(
            pygame.image.load("./img/Bodyguard/Bodyguard_bullet.png"), Bullet_2.graphics.size)
        Bullet_2.graphics.surfacedic["blood"] = Graphics.resizeimg(
            pygame.image.load("./img/Bodyguard/Bodyguard_blood.png"), Bullet_2.graphics.size * 2)

        Bullet_2.physics = Physics(surf=Bullet_2.graphics.surfacedic["default"], show=False)
        Bullet_2.physics.pos = [300, 300]
        Bullet_2.tense = "default"
        Bullet_2.damage_cnst = 5

        Bullet_2.damagelogic = Weapon.dmglgc_yell

    def init_fireeffect():
        global fire
        fire = Effect()

        fire.graphics.size = 150
        res = []
        dir_path = "./img/fireeffect"

        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)
        for i in range(len(res)):
            p = res[i]
            path = dir_path + '/' + p
            fire.graphics.surfacedic[i] = Graphics.resizeimg(pygame.image.load(path), fire.graphics.size)
        fire.graphics.surface = fire.graphics.surfacedic[fire.tense]

        fire.physics = Physics(surf=fire.graphics.surfacedic[fire.tense], show=False)
        fire.physics.pos = [0, 0]


        fire.activated = False
    def init_ICE():
        global ICE
        ICE = Weapon()

        ICE.graphics.size = 800
        res = []
        dir_path = "./img/ice"

        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)
        for i in range(len(res)):
            p = res[i]
            path = dir_path + '/' + p
            ICE.graphics.surfacedic[i] =pygame.Surface.convert_alpha(Graphics.resizeimg(pygame.image.load(path), ICE.graphics.size))
        ICE.graphics.surface = ICE.graphics.surfacedic[ICE.tense]
        ICE.tense = 0
        ICE.gifspeed = 3
        ICE.physics = Physics(surf=ICE.graphics.surfacedic[ICE.tense], show=False)
        ICE.physics.pos = [0, 0]

        ICE.physics_ctrls = {"fly": PhysicsControl.ICEctrl, "hit": PhysicsControl.ICEctrl,
                                 "out": PhysicsControl.ICEctrl}
        ICE.damage_cnst = 10

        ICE.damagelogic = Weapon.dmglgc_ICE

        ICE.activated = False
    def init_sounds() :
        global Sounds
        Sounds = {}
        res = []
        dir_path = "./audio"
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)

        for p in res:
            path = dir_path + '/' + p
            Sounds[p[0:-4]] = pygame.mixer.Sound(path)

    def winimg():
        global jamminwin, juminwin
        jamminwin_count = 4

        jamminwin = []

        # import winning images
        size = Graphics.charactersize * 3
        pos_ = [Graphics.screen_size[0] / 2, Graphics.screen_size[1] * 0.2]

        for i in range(1, jamminwin_count + 1):
            img = pygame.image.load('./img/jammin_win/' + str(i) + '.png')
            j = Character()
            j.graphics.surface = j.graphics.surfacedic["default"] = Graphics.resizeimg(img, size)
            j.physics = Physics(j.graphics.surface, pos_)
            jamminwin.append(j)

        juminwin_count = 2

        juminwin = []

        # import winning images

        for i in range(1, juminwin_count + 1):
            img = pygame.image.load('./img/jumin_win/' + str(i) + '.png')
            j = Character()
            j.graphics.surface = j.graphics.surfacedic["default"] = Graphics.resizeimg(img, size)
            j.physics = Physics(j.graphics.surface, pos_)
            juminwin.append(j)

    def bg():
        res = []
        dir_path = "./img/backgrounds"
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)

        for p in res:
            path = dir_path + '/' + p
            Jammin.graphics.surfacedic[p[7:-4]] = pygame.image.load(path)
            Graphics.addBG(p[0:-4], pygame.Surface.convert(pygame.image.load(path)))

    def init():
        initobj.init_sounds()
        initobj.init_fireeffect()
        initobj.init_ICE()
        initobj.init_yell()

        initobj.init_slipper()
        initobj.init_mirror()
        initobj.init_bullet()
        initobj.init_bullet_2()
        initobj.init_ang()
        initobj.init_Jumin()

        initobj.init_jammin()
        initobj.init_Loopy()
        initobj.init_Billy()
        initobj.init_Bodyguard()
        initobj.init_Bodyguard_2()
        initobj.init_Dongsuk()
        initobj.init_Karina()

        initobj.winimg()
        initobj.bg()



def start_screen():  # 시작화면
    text_scale = int(1 / 40 * Graphics.screen_size[0] * Graphics.obj_scale)
    screen.fill(Graphics.white)
    screen_center = (Graphics.screen_size[0] / 2, Graphics.screen_size[1] / 2)
    # screen, text, size, x, y,

    juminface_spinned = Graphics.resizeimg(pygame.image.load("./img/juminface.png"), Graphics.charactersize)
    juminface_spinned = pygame.transform.rotate(juminface_spinned, 45)

    jamminface_spinned = Graphics.resizeimg(pygame.image.load("./img/jamminface.png"), Graphics.charactersize)
    jamminface_spinned = pygame.transform.rotate(jamminface_spinned, 0)

    # 주민이의 얼굴과 재민이와 하트와 text를 출력한다.
    love2 = pygame.image.load("./img/love.png")
    love2 = Graphics.resizeimg(love2, 3 * Graphics.charactersize)
    love_rect = love2.get_rect()

    introimg = pygame.Surface.convert(pygame.image.load("./img/intro.png"))

    clock = pygame.time.Clock()

    BLINK_EVENT = pygame.USEREVENT + 0

    pygame.time.set_timer(BLINK_EVENT, 1000)
    proceed = False
    while not (proceed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                proceed = True
        screen.fill((255, 255, 255))

        screen.blit(Graphics.resizeimg(introimg, Graphics.width), [0,0])
        pygame.display.update()
        clock.tick(60)
    proceed = False
    tense = True
    while not (proceed):
        for event in pygame.event.get():
            if event.type == BLINK_EVENT:
                tense = not tense
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                proceed = True
        screen.fill((255, 255, 255))

        if tense:
            Graphics.dropShadowText(screen, "Press any key to start", int(1 * text_scale), screen_center[0],
                           screen_center[1] + 3 * text_scale, Graphics.sexy_pink, Graphics.yello)

        screen.blit(juminface_spinned, (screen_center[0] * 0.3, 300))
        screen.blit(jamminface_spinned, (screen_center[0] * 1.5, 350))
        screen.blit(love2, (screen_center[0] - love_rect.centerx, screen_center[1] - love_rect.centery - 300))
        Graphics.dropShadowText(screen, "Jammin likes Jumin", int(2 * text_scale), screen_center[0], screen_center[1], Graphics.sexy_pink,
                       Graphics.yello)
        pygame.display.update()
        clock.tick(60)

def main_play():
    global running
    running = True
    global loop1, end, gamestate, gamestartt, scoreboard
    gamestartt = pygame.time.get_ticks()
    loop1 = True
    end = False

    gamedict = {"STAGE 1 : Loopy": [Loopy], "STAGE 2 : Billy" : [Billy], "STAGE 3 : Bodyguards" : [Bodyguard, Bodyguard_2],
                "STAGE 4 : Dongsuk" : [Dongsuk], "BOSS STAGE : Karina" : [Karina], "Scoreboard" : [Jumin],"end" : 0}
    bgdict = {"STAGE 1 : Loopy": "hanriver", "STAGE 2 : Billy" : "gay", "STAGE 3 : Bodyguards" : "house",
                "STAGE 4 : Dongsuk" : "dongsukroom", "BOSS STAGE : Karina" : "karina","Scoreboard" : "white", "end" : 0}
    chartofunc = {id(Loopy) : initobj.init_Loopy, id(Billy) : initobj.init_Billy, id(Bodyguard) : initobj.init_Bodyguard,
                  id(Bodyguard_2) : initobj.init_Bodyguard_2, id(Dongsuk) : initobj.init_Dongsuk, id(Karina) : initobj.init_Karina}
    gamestates = iter(gamedict.keys())

    while loop1 :
        global text_scale, screen_center, jamminwin, scoreboard
        gamestate = next(gamestates)
        #gamestate = "BOSS STAGE : Karina"
        if gamestate == "end" :
            end = True
            break

        #해당 스테이지 init 처리
        Character.hideall()
        Jammin.physics.show = True
        for char in gamedict[gamestate]:
            #chartofunc[id(char)]()
            char.physics.show = True
        running = True
        Graphics.current_BG = bgdict[gamestate]

        while running:

            USERINPUT.upd()
            Physics.PHYSICS_upd()

            Effect.EFFECT_upd()
            Character.CHARACTER_upd()
            Graphics.GRAPHICS_upd()
            Weapon.WEAPON_upd()
            PhysicsControl.PHYCTRL_upd()
            t = True
            for character in gamedict[gamestate]:
                t = t and character.deathfinish

            if t or Jammin.deathfinish:
                running = False

            fpsClock.tick(Graphics.FPS)
            pygame.display.flip()


        Character.hideall()
        # 판별용 화면
        # Jammin win
        if gamestate != "Scoreboard" :
            if Jammin.HP > 0 :
                black = (0, 0, 0)
                global gta_ending, text_scale, screen_center, jamminwin
                screen_center = (Graphics.screen_size[0] / 2, Graphics.screen_size[1] / 2)
                text_scale = int(1 / 40 * Graphics.screen_size[0] * Graphics.obj_scale)

                # screen, text, size, x, y, colour=(255,255,255), drop_colour=(128,128,128), font=None
                Graphics.current_BG = "gta_background"

                clock = pygame.time.Clock()

                BLINK_EVENT = pygame.USEREVENT + 0

                pygame.time.set_timer(BLINK_EVENT, 1000)
                proceed = False
                tense = True

                random.choice(jamminwin).physics.show =True

                Sounds["gta_ending"].play()
                while not (proceed):
                    for event in pygame.event.get():
                        if event.type == BLINK_EVENT:
                            tense = not tense
                        if event.type == pygame.QUIT:
                            exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                exit()
                            proceed = True

                    Graphics.GRAPHICS_upd()
                    if tense:  # 여기에 깜빡일거 넣기
                        Graphics.dropShadowText(screen, "Press any key for next", int(1.5 * text_scale), screen_center[0],
                                                screen_center[1] + 3 * text_scale, colour=black,
                                                drop_colour=Graphics.toxic_green)

                    # 여기에 상시 출력할 것 넣기
                    text_scale = int(1 / 60 * Graphics.screen_size[0] * Graphics.obj_scale)
                    screen_center = (Graphics.screen_size[0] / 2, Graphics.screen_size[1] / 2)

                    Graphics.dropShadowText(screen, "Jammin won " + gamestate + '!', int(2 * text_scale), screen_center[0],
                                            screen_center[1],
                                            colour=black, drop_colour=Graphics.toxic_green)

                    pygame.display.flip()
                    pygame.display.update()
                    clock.tick(60)
                Sounds["gta_ending"].fadeout(1000)
            elif Jammin.HP <= 0:  # Jammin lose
                black = (0, 0, 0)
                screen_center = (Graphics.screen_size[0] / 2, Graphics.screen_size[1] / 2)
                text_scale = int(1 / 40 * Graphics.screen_size[0] * Graphics.obj_scale)
                Graphics.current_BG = "sadpepe"
                # new code
                Graphics.GRAPHICS_upd()
                pygame.display.flip()
                pygame.display.update()
                clock = pygame.time.Clock()

                BLINK_EVENT = pygame.USEREVENT + 0

                pygame.time.set_timer(BLINK_EVENT, 1000)
                proceed = False
                tense = True
                random.choice(jamminwin).physics.show =  True

                Sounds["jamminsad"].play()
                while not (proceed):
                    for event in pygame.event.get():
                        if event.type == BLINK_EVENT:
                            tense = not tense
                        if event.type == pygame.QUIT:
                            exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                exit()
                            proceed = True

                    Graphics.GRAPHICS_upd()
                    if tense:  # 여기에 깜빡일거 넣기
                        Graphics.dropShadowText(screen, "COME BACK JUMIN..!!!", int(1.5 * text_scale), screen_center[0],
                                                screen_center[1] + 3 * text_scale, colour=black,
                                                drop_colour=Graphics.toxic_green)

                    # 여기에 상시 출력할 것 넣기
                    text_scale = int(1 / 60 * Graphics.screen_size[0] * Graphics.obj_scale)
                    screen_center = (Graphics.screen_size[0] / 2, Graphics.screen_size[1] / 2)

                    Graphics.dropShadowText(screen, "Jammin lost Jumin...", int(2 * text_scale), screen_center[0],
                                            screen_center[1],
                                            colour=black, drop_colour=Graphics.toxic_green)

                    pygame.display.flip()
                    pygame.display.update()
                    clock.tick(60)
                Sounds["jamminsad"].fadeout(1000)
                loop1 = False
        else :
            black = (0, 0, 0)
            screen_center = (Graphics.screen_size[0] / 2, Graphics.screen_size[1] / 2)
            text_scale = int(1 / 40 * Graphics.screen_size[0] * Graphics.obj_scale)

            # screen, text, size, x, y, colour=(255,255,255), drop_colour=(128,128,128), font=None
            Graphics.current_BG = "white"

            clock = pygame.time.Clock()

            BLINK_EVENT = pygame.USEREVENT + 0

            pygame.time.set_timer(BLINK_EVENT, 1000)
            proceed = False
            tense = True
            Jumin.show = True
            Jumin.graphics.size = 200
            score_ = (pygame.time.get_ticks() - gamestartt)//1000


            scoreboard.append(score_)

            scoreboard.sort()
            while not (proceed):
                for event in pygame.event.get():
                    if event.type == BLINK_EVENT:
                        tense = not tense
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            exit()
                        proceed = True

                Graphics.GRAPHICS_upd()
                if tense:  # 여기에 깜빡일거 넣기
                    Graphics.dropShadowText(screen, "Press any key to end", int(1.5 * text_scale), screen_center[0],
                                            screen_center[1] + 3 * text_scale, colour=black,
                                            drop_colour=Graphics.toxic_green)

                # 여기에 상시 출력할 것 넣기
                text_scale = int(1 / 60 * Graphics.screen_size[0] * Graphics.obj_scale)
                screen_center = (Graphics.screen_size[0] / 2, Graphics.screen_size[1] / 2)
                n = scoreboard.index(score_)
                Graphics.dropShadowText(screen, "Your " + str(n) + " place" + gamestate + '!', int(2 * text_scale), screen_center[0],
                                        screen_center[1],
                                        colour=black, drop_colour=Graphics.toxic_green)
                pygame.display.flip()
                pygame.display.update()
                clock.tick(60)

#메인 화면
Graphics.set_screen()
initobj.init()
start_screen()
main_play()

#스코어텍스트에 저장
dir_ = "scoreboard.txt"
scoreboardfile = open(dir_, 'w')
for scores in scoreboard:
    scoreboardfile.write(str(scores) + "\n")
scoreboardfile.close()

