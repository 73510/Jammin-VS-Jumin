# 1 - 모듈 임포트
#from __future__ import absolute_import, division, print_function

import pygame
import random
import pyautogui
import math
# 모든 전역 변수
width, height = pyautogui.size()
screen_size = (width * 0.4, height * 0.8)
width = screen_size[0]
height = screen_size[1]
obj_scale = 1.0
charactersize = 3 * int(1 / 30 * width)  # 우선 가로만 맞추는걸로
FPS = 60

sexy_pink = (245, 69, 221)
toxic_green = (22, 241, 4)  # (0, 0, 0)#(140, 12, 80)#(1, 255, 251 )
sexy_blue = (1, 255, 251)
blue = (16, 34, 217)
yello = (255, 243, 0)


def inscreen(pos, rect):
    if pos[0] - rect.center[0] >= 0 and pos[0] + rect.center[0] <= screen_size[0] and 0 <= pos[1] - rect.center[1] and \
            pos[1] + rect.center[1] <= screen_size[1]:
        return True
    return False


def outofscreen(pos, rect):
    if pos[0] + rect.center[0] <= 0 and pos[0] - rect.center[0] >= screen_size[0] and 0 >= pos[1] + rect.center[1] and \
            pos[1] - rect.center[1] >= screen_size[1]:
        return True
    else:
        return False


# obj를 위한 클래스 생성
class py_object:  # surface(pygame surface), pos(list pair), show(bool)

    # 생성자 함수, surf - surface, pos - position, show - 활성화 여부, lock - 이동시 x축 lock 여부
    def __init__(self, surf, pos, show=True, angle=0, lock=False, org_img=False):
        self.surface = surf
        self.pos = pos  # object의 pos는 center위치로 저장되어있음
        self.show = show
        self.angle = angle
        self.lock = lock  # #l
        self.vel = [0, 0]  # 이건 생성자에 안넣어줬음
        if not org_img:
            self.org_img = surf
        else:
            self.org_img = org_img

    def collision(self, object):
        self_rect = self.surface.get_rect()  # 이후 object 의 rect를 상대위치만큼 이동시켜 줌
        # (centerx, centery) 된거니까

        # (-self.pos[0] + self_rect.centerx, -self.pos[1] + self_rect.centery)만큼 이동시킨거니까

        object_rect = object.surface.get_rect()
        object_rect.centerx += object.pos[0] - self.pos[0]  # + self_rect.centerx
        object_rect.centery += object.pos[1] - self.pos[1]  # + self_rect.centery

        return self_rect.colliderect(object_rect) and (self.show and object.show)

    def wallcollision(self):
        self_rect = self.surface.get_rect()
        return not inscreen(self.pos, self_rect)

    def outofscreen(self):
        rect = self.surface.get_rect()
        pos = self.pos
        if pos[0] + rect.center[0] <= 0 or pos[0] - rect.center[0] >= screen_size[0] or 0 >= pos[1] + rect.center[1] or \
                pos[1] - rect.center[1] >= screen_size[1]:
            return True
        else:
            return False

    def move(self, arg=lambda x, y: True):  # move의 vel은 단위벡터 두개
        vel = self.vel
        rect = self.surface.get_rect()
        next = [self.pos[0], self.pos[1]]
        if self.lock:
            next[0] += vel[0]
        else:
            next[0] += vel[0]
            next[1] += vel[1]

        if arg(next, rect):
            self.pos[0] = next[0]
            self.pos[1] = next[1]

    def spin(self, vel, s_vel, dir):
        self.vel[0] = vel[0]
        self.vel[1] = vel[1]
        angle_ = (s_vel) / FPS
        self.angle += angle_

        self.surface = pygame.transform.rotate(self.org_img, (-1) ** dir * self.angle % 360)

        self.move(lambda x, y: not outofscreen(x, y))

    def throwed(self, vel, s_vel, dir):  # vel을 tuple(x, y)로 만듦)
        self.vel[0] = vel[0]
        self.vel[1] = vel[1]

        if self.show: self.spin(vel, s_vel, dir)

        if self.outofscreen():
            self.show = False

    def applykey(self, keytense4, vel):
        arg = lambda x, y: inscreen(x, y)

        if keytense4[0]:
            self.vel[1] = -vel
        elif keytense4[1]:
            self.vel[1] = +vel
        else:
            self.vel[1] = 0
        if keytense4[2]:
            self.vel[0] = -vel
        elif keytense4[3]:
            self.vel[0] = vel
        else:
            self.vel[0] = 0

        self.move(lambda x, y: inscreen(x, y))


def get_center_coord(object):
    rect = object.surface.get_rect()
    return (object.pos[0] - rect.center[0], object.pos[1] - rect.center[1])


def blit_all(objects):  # blit by center coordinate
    for obj in objects:
        blit_pos = get_center_coord(obj)
        if obj.show:
            screen.blit(obj.surface, blit_pos)


def resizeimg(surface, width):
    rect = surface.get_rect()
    a = width / rect.width
    return pygame.transform.scale(surface, (width, rect.height * a))


# 2 - 게임 변수 초기화
# 2.1 - 게임 화면

def init_game():
    global screen, fpsClock, score, sharkimg_original, sharkimg_resized
    global black, white

    global whamimg, wham, jamminimg, sharkimg_original, sharkimg_resized, juminimg, badmintonimg, badmintonstartpos
    global juminvel, jamminvel, juminstartpos, jamminstartpos, jumin, jammin, badminton, throwvel, throwconst
    global keytense_wsad, keytense_arrow, width, height

    global badminton_var, event_tick, wham_start_t, shark

    global HP_img, HP_jumin_obj, HP_jammin_obj, JAMMIN_HP, JUMIN_HP, love, love_start_t, loveimg, shiftpressed, sibaactivate

    sibaactivate = False
    shiftpressed = False

    global JUMIN_HP_MAX, JAMMIN_HP_MAX
    JUMIN_HP_MAX = 50
    JAMMIN_HP_MAX = 100
    JAMMIN_HP = 100
    JUMIN_HP = 50
    HP_img = []
    HP_jumin_obj = []
    HP_jammin_obj = []

    wham_start_t = 0
    love_start_t = 0

    badminton_var = []  # 0 : throwfinish 1 : jumin 2: jammin 3 : jumbool, 4 : jambool
    event_bad_throwfinished = pygame.event.Event(pygame.USEREVENT, attr1='THROWFINISHEDBAD')
    event_bad_juminthrowstart = pygame.event.Event(pygame.USEREVENT, attr1="JUMINTHROWBAD")
    event_bad_jamminthrowstart = pygame.event.Event(pygame.USEREVENT, attr1="JAMMINTHROWBAD")
    badminton_var.append(event_bad_throwfinished)
    badminton_var.append(event_bad_juminthrowstart)
    badminton_var.append(event_bad_jamminthrowstart)
    badminton_var.append(False)
    badminton_var.append(False)

    global shark_var

    shark_var = []  # 0 : throwfinish 1 : jumin 2: jammin 3 : jumbool, 4 : jambool
    event_shark_throwfinished = pygame.event.Event(pygame.USEREVENT, attr1='THROWFINISHEDshark')
    event_shark_juminthrowstart = pygame.event.Event(pygame.USEREVENT, attr1="JUMINTHROWshark")
    event_shark_jamminthrowstart = pygame.event.Event(pygame.USEREVENT, attr1="JAMMINTHROWshark")
    shark_var.append(event_shark_throwfinished)
    shark_var.append(event_shark_juminthrowstart)
    shark_var.append(event_shark_jamminthrowstart)
    shark_var.append(False)
    shark_var.append(False)

    global jamshoot_var

    jamshoot_var = {}
    '''
    0 : jamshootfinish _evnt
    1 : jamshootstart _evnt
    2 : jamminshooting
    3 : jammin_throwed_tick
    4 : jammin_charged
    5 : jammin_loving
    '''  # 이거 그냥 대충, key press 일때 tick 업데이트하고  keyup일때 shootstart & tick처리 shootfinish
    event_jamshootfinished = pygame.event.Event(pygame.USEREVENT, attr1='jamshootfinished')
    event_jamshootstart = pygame.event.Event(pygame.USEREVENT, attr1="jamshootstart")
    jamshoot_var["finished"] = event_jamshootfinished
    jamshoot_var["start"] = event_jamshootstart
    jamshoot_var["throwing"] = False
    jamshoot_var["thrown_tick"] = 0
    jamshoot_var["charged"] = False
    jamshoot_var["loving"] = False

    throwvel = [0, 0]
    throwconst = 20

    keytense_wsad = [0, 0, 0, 0]
    keytense_arrow = [0, 0, 0, 0]
    black = (0, 0, 0)
    white = (255, 255, 255)

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    fpsClock = pygame.time.Clock()
    # 2.4 - 점수
    score = 0

    pygame.display.set_caption('Jammin likes Jumin')
    jam_face_icon = pygame.image.load('./img/icon/jam_face.jpg')
    pygame.display.set_icon(jam_face_icon)

    pygame.mixer.init()

    try:
        # 3 - 그림과 효과음 삽입
        # 3.1 - 그림 삽입
        sharkimg = pygame.image.load("./img/shark.png")
        jamminimg = pygame.image.load("./img/jamminface.png")
        juminimg = pygame.image.load("./img/juminface.png")
        badmintonimg = pygame.image.load("./img/badminton.png")
        whamimg = pygame.image.load("./img/wham.png")
        loveimg = pygame.image.load("./img/love.png")

        # HP import
        hp_size = width//8
        for i in range(0, 11):
            hp_dir = "./img/HP_/HP_" + str(i) + ".png"
            HP_img.append(resizeimg(pygame.image.load(hp_dir), hp_size))

        # open sounds
        global oooooof, oof, gta_ending, punch, fadeoutlength, throw
        fadeoutlength = 500

        oooooof = pygame.mixer.Sound("./audio/oooooof.mp3")
        oof = pygame.mixer.Sound("./audio/oof.mp3")
        gta_ending = pygame.mixer.Sound('./audio/gta_ending.mp3')
        punch = pygame.mixer.Sound('./audio/punch.mp3')
        throw = pygame.mixer.Sound('./audio/throw.mp3')

        # sound2
        global johncena, juminhurt, wee, lovesounds

        johncena = pygame.mixer.Sound("./audio/johncena.mp3")
        juminhurt = pygame.mixer.Sound("./audio/juminhurt.mp3")

        juminhurt.set_volume(0.4)
        wee = pygame.mixer.Sound("./audio/wee.mp3")
        lovesounds = pygame.mixer.Sound("./audio/lovesounds.mp3")

        # rescaling images
        juminimg = resizeimg(juminimg, charactersize)
        jamminimg = resizeimg(jamminimg, charactersize)
        badmintonimg = resizeimg(badmintonimg, int(charactersize * 0.5))
        whamimg = resizeimg(whamimg, int(charactersize * 2))
        sharkimg = resizeimg(sharkimg, charactersize * 1.8)
        loveimg = resizeimg(loveimg, int(charactersize * 4))
        # 3.2 - 효과음 삽입
        # 3.3 - 폰트 삽입

    except Exception as err:
        print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
        pygame.quit()
        exit(0)

    juminvel = 10
    jamminvel = 10
    jamminstartpos = [width // 2, height // 10 * 8]  # list로 만들어야 됨
    juminstartpos = [width // 2, height - height // 10 * 8]
    badmintonstartpos = [width // 2, height // 2]
    sharkstartpos = [width // 2, height // 2]

    jumin = py_object(juminimg, juminstartpos, 1)
    jammin = py_object(jamminimg, jamminstartpos, 1)  # 마지막꺼 show
    badminton = py_object(badmintonimg, badmintonstartpos, 0)
    shark = py_object(sharkimg, sharkstartpos, 0)
    wham = py_object(whamimg, [100, 100], 0)
    love = py_object(loveimg, [100, 100], 0)

    HP_jumin_pos = [width * 0.1, height * 0.1]
    HP_jammin_pos = [width - width * 0.1, height - height * 0.1]

    for img in HP_img:
        HP_jumin_obj.append(py_object(img, HP_jumin_pos, 0))
        HP_jammin_obj.append(py_object(img, HP_jammin_pos, 0))


class init_object:#물건을 던질 때 초기화되는 항목
    global badminton, jumin, jammin, throwvel, throwconst, shark

    def juminbadmintoninit(): #주민이의 배드민턴 설정
        badminton.show = True
        badminton.pos[0] = jumin.pos[0]
        badminton.pos[1] = jumin.pos[1]

        badminton.vel = [jumin.vel[0], jumin.vel[1] + throwconst]

    def jamminbadmintoninit(): #재민이의 배드민턴 설정
        badminton.show = True
        badminton.pos[0] = jammin.pos[0]
        badminton.pos[1] = jammin.pos[1]

        badminton.vel = [jammin.vel[0], jammin.vel[1] - throwconst]

    def juminsharkinit():# 주민이의 상어
        shark.show = True
        shark.pos[0] = jumin.pos[0]
        shark.pos[1] = jumin.pos[1]

        shark.vel = [jumin.vel[0], jumin.vel[1] + throwconst]

    def jamminsharkinit(): #재민이의 상어
        shark.show = True
        shark.pos[0] = jammin.pos[0]
        shark.pos[1] = jammin.pos[1]

        shark.vel = [jammin.vel[0], jammin.vel[1] - throwconst]

    def jamminrst():
        jammin.lock = True
        jammin.show = True
        jammin.pos = [width // 2, height // 10 * 8]

        jamshoot_var["throwing"] = False
        jamshoot_var["thrown_tick"] = 0
        jamshoot_var["charged"] = False
        jamshoot_var["loving"] = False


# 4 - 글자 출력
def text(arg, coord, fontsize, fontcolor):
    x = coord[0]
    y = coord[1]
    font = pygame.font.Font('./public-pixel-font/arcadelit.ttf', fontsize)
    text = font.render(str(arg), False, fontcolor)
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    screen.blit(text, textRect)


def start_screen():
    text_scale = int(1 / 40 * screen_size[0] * obj_scale)
    screen.fill(white)
    screen_center = (screen_size[0] / 2, screen_size[1] / 2)
    # screen, text, size, x, y,

    juminface_spinned = resizeimg(pygame.image.load("./img/juminface.png"), charactersize)
    juminface_spinned = pygame.transform.rotate(juminface_spinned, 45)

    jamminface_spinned = resizeimg(pygame.image.load("./img/jamminface.png"), charactersize)
    jamminface_spinned = pygame.transform.rotate(jamminface_spinned, 0)


    love2 = pygame.image.load("./img/love.png")
    love2 = resizeimg(love2, 3 * charactersize)
    love_rect = love2.get_rect()

    clock = pygame.time.Clock()

    BLINK_EVENT = pygame.USEREVENT + 0

    pygame.time.set_timer(BLINK_EVENT, 1000)
    proceed = False
    tense = True
    while not (proceed):
        for event in pygame.event.get():
            if event.type == BLINK_EVENT :
                tense = not tense
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                proceed = True
        screen.fill((255, 255, 255))

        if tense :
            dropShadowText(screen, "Press any key to start", int(1 * text_scale), screen_center[0], screen_center[1] + 3 * text_scale, sexy_pink, yello)

        screen.blit(juminface_spinned, (screen_center[0] * 0.3, 300))
        screen.blit(jamminface_spinned, (screen_center[0] * 1.5, 350))
        screen.blit(love2, (screen_center[0] - love_rect.centerx, screen_center[1] - love_rect.centery - 300))
        dropShadowText(screen, "Jammin likes Jumin", int(2 * text_scale), screen_center[0], screen_center[1], sexy_pink,
                       yello)
        pygame.display.update()
        clock.tick(60)


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


def end_screen(winner):
    black = (0, 0, 0)
    global gta_ending, text_scale, screen_center
    screen_center = (screen_size[0] / 2, screen_size[1] / 2)
    text_scale = int(1 / 40 * screen_size[0] * obj_scale)

    juminwin_count = 2
    jamminwin_count = 4

    juminwin = []
    jamminwin = []

    # import winning images
    size = charactersize * 3
    pos_ = [screen_size[0] / 2, screen_size[1] * 0.2]
    for i in range(1, juminwin_count + 1):
        img = pygame.image.load('./img/jumin_win/' + str(i) + '.png')
        juminwin.append(py_object(resizeimg(img, size), pos_, 1))
    for i in range(1, jamminwin_count + 1):
        img = pygame.image.load('./img/jammin_win/' + str(i) + '.png')
        jamminwin.append(py_object(resizeimg(img, size), pos_, 1))
    gta_backgroundimg = pygame.image.load('./img/gta_background.jpg')
    # screen, text, size, x, y, colour=(255,255,255), drop_colour=(128,128,128), font=None


    pygame.display.flip()
    # new code
    clock = pygame.time.Clock()

    BLINK_EVENT = pygame.USEREVENT + 0

    pygame.time.set_timer(BLINK_EVENT, 1000)
    proceed = False
    tense = True
    objects = []
    if winner == "jumin":
        juminpic = random.choice(juminwin)
        objects.append(juminpic)

    if winner == "jammin":
        objects.append(random.choice(jamminwin))

    gta_ending.play()
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

        screen.blit(resizeimg(gta_backgroundimg, width * 2), (0, 0))
        if tense: #여기에 깜빡일거 넣기
            dropShadowText(screen, "Press space to restart", int(1.5 * text_scale), screen_center[0],
                           screen_center[1] + 3 * text_scale, colour=black, drop_colour=toxic_green)


        #여기에 상시 출력할 것 넣기
        text_scale = int(1 / 60 * screen_size[0] * obj_scale)
        screen_center = (screen_size[0] / 2, screen_size[1] / 2)
        if winner == "jumin":
            dropShadowText(screen, "Jumin succeeded to run away!", int(2 * text_scale), screen_center[0],
                           screen_center[1],
                           colour=black, drop_colour=yello)
        if winner == "jammin":
            dropShadowText(screen, "Jammin found his love!", int(2 * text_scale), screen_center[0], screen_center[1],
                           colour=black, drop_colour=toxic_green)

        blit_all(objects)
        pygame.display.update()
        clock.tick(60)
    gta_ending.fadeout(fadeoutlength)


def get_key(events):
    global keytense_wsad, keytense_arrow
    global juminthrow, jamminthrow
    global juminbadmintonposinit
    global jamshoot_var, shiftpressed

    for event in events:  # 나중에 키보드 입력 함수 따로 만들기
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:# wasd에 대해 keytense_wasd 지정
            if event.key == pygame.K_w:
                keytense_wsad[0] = 1
            elif event.key == pygame.K_s:
                keytense_wsad[1] = 1
            elif event.key == pygame.K_a:
                keytense_wsad[2] = 1
            elif event.key == pygame.K_d:
                keytense_wsad[3] = 1

            elif event.key == pygame.K_LEFTBRACKET:# 방향키에 대해 같은 작업(keytense_arrow)
                keytense_arrow[0] = 1
            elif event.key == pygame.K_QUOTE:
                keytense_arrow[1] = 1
            elif event.key == pygame.K_SEMICOLON:
                keytense_arrow[2] = 1
            elif event.key == pygame.K_RETURN:
                keytense_arrow[3] = 1

            if not jamshoot_var['loving']:  # 주민이가 사랑당하고 있지 않다면, 공격키를 적용시켜라
                if event.key == pygame.K_e: pygame.event.post(badminton_var[1])

            if not (jamshoot_var['loving'] or jamshoot_var['throwing']):  # 재민이가 날아가는중, 사랑하는 중엔 공격 불가
                if event.key == pygame.K_MINUS: pygame.event.post(shark_var[2])

            if event.key == pygame.K_EQUALS and jamshoot_var['throwing'] == False and jamshoot_var['loving'] == False:  # 충전키가 눌렸고 날아가는 중이 아닐때
                shiftpressed = True
                jamshoot_var['thrown_tick'] = pygame.time.get_ticks()
            elif event.key == pygame.K_BACKSPACE and jamshoot_var["throwing"] == False and jamshoot_var[
                "charged"]:  # 발사키가 눌렸고, 충전이 되었고 날아가는 중이 아니면

                pygame.event.post(jamshoot_var["start"])  # 날려라

            elif event.key == pygame.K_ESCAPE:
                exit()
        elif event.type == pygame.KEYUP:#wasd, 방향키가 눌리지 않았을 떄
            if event.key == pygame.K_w:
                keytense_wsad[0] = 0
            elif event.key == pygame.K_s:
                keytense_wsad[1] = 0
            elif event.key == pygame.K_a:
                keytense_wsad[2] = 0
            elif event.key == pygame.K_d:
                keytense_wsad[3] = 0
            elif event.key == pygame.K_LEFTBRACKET:
                keytense_arrow[0] = 0
            elif event.key == pygame.K_QUOTE:
                keytense_arrow[1] = 0
            elif event.key == pygame.K_SEMICOLON:
                keytense_arrow[2] = 0
            elif event.key == pygame.K_RETURN:
                keytense_arrow[3] = 0

            elif event.key == pygame.K_EQUALS and jamshoot_var['throwing'] == False and jamshoot_var['loving'] == False: #사랑 충전중
                jamshoot_var["thrown_tick"] = pygame.time.get_ticks() - jamshoot_var["thrown_tick"]
                jamshoot_var["charged"] = True
                shiftpressed = False

        elif event == badminton_var[0]:
            badminton_var[3] = False
            badminton_var[4] = False
        elif event == shark_var[0]:
            shark_var[3] = False
            shark_var[4] = False


        elif event == badminton_var[1] and (badminton_var[3] == False) and (badminton_var[4] == False):
            init_object.juminbadmintoninit()
            badminton_var[3] = True
            throw.stop()
            throw.play()

        elif event == badminton_var[2] and (badminton_var[3] == False) and (badminton_var[4] == False):
            init_object.jamminbadmintoninit()
            badminton_var[4] = True
            throw.stop()
            throw.play()

        elif event == shark_var[1] and (shark_var[3] == False) and (shark_var[4] == False):
            init_object.juminsharkinit()
            shark_var[3] = True
            throw.stop()
            throw.play()

        elif event == shark_var[2] and (shark_var[3] == False) and (shark_var[4] == False):
            init_object.jamminsharkinit()
            shark_var[4] = True
            throw.stop()
            throw.play()

        elif event == jamshoot_var["start"]:  # 발사 명령이 들어왔으면
            jamshoot_var["throwing"] = True  # 발사중을 참으로 바꿔라
            wee.play()

        elif event == jamshoot_var["finished"] and jamshoot_var['loving'] == False:  # 그냥 밖으로 튀어 나간거면
            init_object.jamminrst()

        elif event == jamshoot_var["finished"] and jamshoot_var['loving'] == True:  # 주민이와 충돌한거면
            jamshoot_var['throwing'] = False
            jamshoot_var["charged"] = False


def get_key_siba(events):
    global keytense_wsad, keytense_arrow
    global juminthrow, jamminthrow
    global juminbadmintonposinit
    global jamshoot_var, shiftpressed, qpress, JAMMIN_HP

    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keytense_wsad[0] = 1
            elif event.key == pygame.K_s:
                keytense_wsad[1] = 1
            elif event.key == pygame.K_a:
                keytense_wsad[2] = 1
            elif event.key == pygame.K_d:
                keytense_wsad[3] = 1

            elif event.key == pygame.K_LEFTBRACKET:
                keytense_arrow[0] = 1
            elif event.key == pygame.K_QUOTE:
                keytense_arrow[1] = 1
            elif event.key == pygame.K_SEMICOLON:
                keytense_arrow[2] = 1
            elif event.key == pygame.K_RETURN:
                keytense_arrow[3] = 1
            elif event.key == pygame.K_e:
                throw.play()
                qpress = True

                # check if collides

                global jamfly

                if jumin.collision(jammin) and not jamfly:
                    print("collision occured and jamfly == False")
                    velconst = 30
                    if jammin.pos[0] == jumin.pos[0] :
                        jammin.vel = [0, 50]

                    else :
                        tan_ = (jammin.pos[1] - jumin.pos[1]) / (jammin.pos[0] - jumin.pos[0])
                        sin_ = tan_ / math.sqrt(tan_ ** 2 + 1)
                        cos_ = 1 / math.sqrt(tan_ ** 2 + 1)

                        if jammin.pos[0] < jumin.pos[0]:
                            jammin.vel = [-velconst*cos_, velconst * sin_]
                        else :
                            jammin.vel = [velconst * cos_, velconst * sin_]
                    print(jammin.vel)
                    jamfly = True
                    JAMMIN_HP -= 30
                    oof.play()
                    punch.play()
                    throw.play()

            elif event.key == pygame.K_ESCAPE:
                exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keytense_wsad[0] = 0
            elif event.key == pygame.K_s:
                keytense_wsad[1] = 0
            elif event.key == pygame.K_a:
                keytense_wsad[2] = 0
            elif event.key == pygame.K_d:
                keytense_wsad[3] = 0
            elif event.key == pygame.K_LEFTBRACKET:
                keytense_arrow[0] = 0
            elif event.key == pygame.K_QUOTE:
                keytense_arrow[1] = 0
            elif event.key == pygame.K_SEMICOLON:
                keytense_arrow[2] = 0
            elif event.key == pygame.K_RETURN:
                keytense_arrow[3] = 0
            elif event.key == pygame.K_e:
                qpress = False


def i_got_shot():
    global jumin, jammin, badminton, wham, wham_start_t, JUMIN_HP, JAMMIN_HP

    badmintondamage = 10
    sharkdamage = 5

    if jammin.collision(badminton) and badminton_var[3] == True:#재민이가 배드민턴에 맞음
        oof.play()
        punch.play()
        pygame.event.post(badminton_var[0])
        badminton.show = False
        wham_start_t = pygame.time.get_ticks()
        wham.pos[0] = jammin.pos[0]
        wham.pos[1] = jammin.pos[1]
        wham.show = True
        JAMMIN_HP -= badmintondamage

    if jumin.collision(badminton) and badminton_var[4] == True:#주민이가 배드민턴에 맞음
        juminhurt.play()
        punch.play()
        pygame.event.post(badminton_var[0])
        badminton.show = False
        wham_start_t = pygame.time.get_ticks()
        wham.pos[0] = jumin.pos[0]
        wham.pos[1] = jumin.pos[1]
        wham.show = True

        JUMIN_HP -= badmintondamage

    if jammin.collision(shark) and shark_var[3] == True: #재민이가 상어에 맞음
        oof.play()
        punch.play()
        pygame.event.post(shark_var[0])
        shark.show = False
        wham_start_t = pygame.time.get_ticks()
        wham.pos[0] = jammin.pos[0]
        wham.pos[1] = jammin.pos[1]
        wham.show = True
        JAMMIN_HP -= sharkdamage

    if jumin.collision(shark) and shark_var[4] == True:#주민이가 상어에 맞음
        juminhurt.play()
        punch.play()
        pygame.event.post(shark_var[0])
        shark.show = False
        wham_start_t = pygame.time.get_ticks()
        wham.pos[0] = jumin.pos[0]
        wham.pos[1] = jumin.pos[1]
        wham.show = True

        JUMIN_HP -= sharkdamage

    global love, love_start_t
    if jumin.collision(jammin) and jamshoot_var["throwing"] == True and jamshoot_var["loving"] == False:  # 주민이와 부딫혔는데 아직 사랑중이 아니고 던지는 중이라면
        jamshoot_var["loving"] = True
        jammin.vel = [0, 0]
        pygame.event.post(jamshoot_var["finished"])
        love_start_t = pygame.time.get_ticks()
        love.pos[0] = (jumin.pos[0] + jammin.pos[0]) // 2
        love.pos[1] = (jumin.pos[1] + jammin.pos[1]) // 2
        love.show = True
        lovesounds.play()

    if pygame.time.get_ticks() - wham_start_t >= 1000:
        wham.show = False

    if pygame.time.get_ticks() - love_start_t >= 3000 and jamshoot_var['loving'] == True:
        oof.play()
        damage = (jamshoot_var['thrown_tick'] // 10)**2 / 2000 +5
        JUMIN_HP -= damage
        init_object.jamminrst()
        love.show = False
        lovesounds.stop()

    if pygame.time.get_ticks() - love_start_t < 3000 and jamshoot_var['loving'] == True:
        _img = pygame.image.load("./img/jammin_win/3.png")
        rect_size = (pygame.time.get_ticks() - love_start_t) // 2 + 100
        _img = resizeimg(_img, rect_size)
        imgrect = _img.get_rect()

        screen.blit(_img, [screen_size[0] // 2 - imgrect.centerx, screen_size[1] // 2 - imgrect.centery])


def HP_display():
    global JAMMIN_HP, JUMIN_HP

    # print(JAMMIN_HP, JUMIN_HP)

    for i in range(0, 11):
        HP_jammin_obj[i].show = False
        HP_jumin_obj[i].show = False

    for i in range(0, 11):
        if i * 10 <= JAMMIN_HP < (i + 1) * 10:
            HP_jammin_obj[i].show = True
            break
    for i in range(0, 11):
        if i * 5 <= JUMIN_HP < (i + 1) * 5:
            HP_jumin_obj[i].show = True
            break


def ultimate_screensiba():#등장 초기 장면 재생
    wham.show = False

    johncena.play()
    clock = pygame.time.Clock()

    text_scale = int(1 / 40 * screen_size[0] * obj_scale)
    for i in range(30):
        color = 225 //(i % 15+1) +30
        color2 = (color-30, color-30, color-30)
        color = (color, 0, 0)

        screen_center = (screen_size[0] / 2, screen_size[1] / 2)

        screen.fill((230, 230, 230))
        dropShadowText(screen, "ultimate_siba activated", int(1 * text_scale), screen_center[0], screen_center[1] + 3 * text_scale, color, color2)

        throw.play()
        jumin.spin([0, 0], 10000, 0)
        blit_all([jumin])
        pygame.time.wait(50)


        pygame.display.flip()
    siba1 = pygame.image.load("./img/siba1.png")
    siba1 = resizeimg(siba1, charactersize * 2)
    jumin.surface = siba1
    jumin.org_img = siba1
    for i in range(70):
        color = 225 //(i % 15+1) +30
        color2 = (color-30, color-30, color-30)
        color = (color,0 , 0)

        screen_center = (screen_size[0] / 2, screen_size[1] / 2)

        screen.fill((230, 230, 230))
        dropShadowText(screen, "ultimate_siba activated", int(1 * text_scale), screen_center[0], screen_center[1] + 3 * text_scale, color, color2)

        throw.play()
        jumin.spin([0, 0], 10000, 0)
        blit_all([jumin])
        pygame.time.wait(50)
        pygame.display.flip()
    jumin.pos = [width // 2, height // 10 * 2]
    johncena.fadeout(5000)



def main_play():
    global jumin, jammin, throwvel, event_tick, wham, sibaactivate, JUMIN_HP, qpress, JAMMIN_HP
    qpress = False
    sibastarttick = 0
    sibaactivated = 0  # 시바가 호출 되었는지 여부
    running = True
    heal_items = []
    while running:
        # 6 - 화면을 그리기에 앞서 화면을 흰색으로 지우기
        screen.fill((255, 255, 255))

        objects = []

        # 시바로 전환되는 부분
        if sibaactivate == False and JUMIN_HP <= 10 and sibaactivated == False:
            global jamfly
            jamfly = False
            # 각성효과음 + blinking text
            ultimate_screensiba()

            sibaactivate = True
            sibaactivated = True
            sibastarttick = pygame.time.get_ticks()

            # sibastarteffects
            siba1 = pygame.image.load("./img/siba1.png")
            siba1 = resizeimg(siba1, charactersize * 2)
            jumin.surface = siba1  #
            badminton.show = False
            shark.show = False
            wham.show = False

        # 시바 전환 해제, 원상복구
        if pygame.time.get_ticks() - sibastarttick >= 10000 and sibaactivate == True:
            sibaactivate = False
            # go back to jumin code
            jumin.surface = juminimg

            jammin.pos = [width // 2, height // 10 * 8]
            jumin.pos = [width // 2, height // 10 * 2]
            jammin.lock = True
            jumin.lock = True
            shark_var[4] = False
            badminton_var[3] = False

        # 나중에 삭제
        # 7 - 키보드/마우스 이벤트

        # 일반 모드, 재민, 주민
        if sibaactivate == False:
            get_key(pygame.event.get())
            if not jamshoot_var['loving']:
                jumin.applykey(keytense_wsad, juminvel)
            if not (jamshoot_var["throwing"] or shiftpressed or jamshoot_var['loving']):
                jammin.applykey(keytense_arrow, jamminvel)

            # badminton.throwed(35, 300, 0)
            jumin.lock = 1
            jammin.lock = True

            # 던지는 부분

            if badminton_var[3]:
                badminton.throwed(badminton.vel, 600, 0)
                if badminton.outofscreen():
                    pygame.event.post(badminton_var[0])
                # (self, vel, s_vel, dir):  # vel을 tuple(x, y)로 만듦)
            if badminton_var[4]:
                badminton.throwed(badminton.vel, 600, 0)
                if badminton.outofscreen():
                    pygame.event.post(badminton_var[0])

            if shark_var[3]:
                shark.throwed(shark.vel, 600, 0)
                if shark.outofscreen():
                    pygame.event.post(shark_var[0])
                # (self, vel, s_vel, dir):  # vel을 tuple(x, y)로 만듦)
            if shark_var[4]:
                shark.throwed(shark.vel, 600, 0)
                if shark.outofscreen():
                    pygame.event.post(shark_var[0])
            if jamshoot_var["throwing"]:
                jammin.lock = False
                jammin.vel = [0, -jamshoot_var["thrown_tick"] / 40]
                jammin.throwed(jammin.vel, 0, 0)
                if jammin.outofscreen():
                    pygame.event.post(jamshoot_var['finished'])

        # 시바견 모드일때
        if sibaactivate == True:
            get_key_siba(pygame.event.get())
            jammin.lock = False
            jumin.lock = False

            jumin.applykey(keytense_wsad, juminvel)
            if not jamfly :
                jammin.applykey(keytense_arrow, jamminvel * 1.8)

            if qpress:
                siba2 = pygame.image.load("./img/siba2.png")
                siba2 = resizeimg(siba2, charactersize * 3.6)
                jumin.surface = siba2
            else:
                jumin.surface = siba1

            if jammin.outofscreen() and jamfly:
                jammin.pos = [random.randint(100, int(width-100)), random.randint(int(height*0.1), int(height *0.9))]
                jamfly = False

            if jamfly :
                jammin.spin(jammin.vel, 800, 1)


            # heal item drop
            heal_hp = 5

            heal_item_num = 6

            if random.randint(1, 100) == 15:  # 힐템 추가

                heal_xpos = random.randint(width // 20, width - width // 20)
                # select randomimg
                heal_img = pygame.image.load("./img/heal_items/" + str(random.randint(1, heal_item_num)) + ".png")
                heal_img = resizeimg(heal_img, charactersize)
                # append
                item = py_object(heal_img, [heal_xpos, 10], True)
                item.vel = [0, 10]
                heal_items.append(item)

            for heal_item in heal_items:
                objects.append(heal_item)
                if heal_item.show:
                    heal_item.move()

                if jumin.collision(heal_item):
                    oof.stop()
                    oof.play()
                    heal_item.show = False
                    if JUMIN_HP + heal_hp <= JUMIN_HP_MAX:
                        JUMIN_HP += heal_hp
                elif jammin.collision(heal_item):
                    oof.stop()
                    oof.play()
                    heal_item.show = False
                    if JAMMIN_HP + heal_hp <= JAMMIN_HP_MAX:
                        JAMMIN_HP += heal_hp
                if heal_item.outofscreen():
                    heal_item.show = False

        # 던진거 맞았으면 처리
        i_got_shot()

        HP_display()

        objects.append(jumin)  # 나중에 objects 한꺼번에 다 셋팅
        objects.append(jammin)
        objects.append(badminton)
        objects.append(shark)
        objects.append(wham)
        objects.append(love)
        for i in range(0, 11):
            objects.append(HP_jumin_obj[i])
            objects.append(HP_jammin_obj[i])

        blit_all(objects)

        fpsClock.tick(FPS)
        # pygame.event.post()

        # 11 - 화면 전체 업데이트
        pygame.display.flip()

        if JAMMIN_HP <= 0:
            running = False
            return 'jumin'
        if JUMIN_HP <= 0:
            running = False
            return 'jammin'


def dyingeffect(winner):
    jumindeadimg = pygame.image.load('./img/jumindead.png')
    jammindeadimg = pygame.image.load('./img/jammindead.png')

    jumindeadimg = resizeimg(jumindeadimg, charactersize)
    jammindeadimg = resizeimg(jammindeadimg, charactersize)

    jumin.lock = 0
    jammin.lock = 0


    oooooof.play()

    if winner == 'jammin':
        jumin.surface = jumindeadimg
        jumin.org_img = jumindeadimg
    elif winner == 'jumin':
        jammin.surface = jammindeadimg
        jammin.org_img = jammindeadimg

    running = True
    while (running):
        # 6 - 화면을 그리기에 앞서 화면을 흰색으로 지우기
        screen.fill((213, 213, 213))

        # 7 - 키보드/마우스 이벤트
        get_key(pygame.event.get())

        HP_display()

        objects = []
        objects.append(jumin)  # 나중에 objects 한꺼번에 다 셋팅
        objects.append(jammin)
        objects.append(wham)
        for i in range(0, 11):
            objects.append(HP_jumin_obj[i])
            objects.append(HP_jammin_obj[i])

        if winner == 'jumin':  # def spin(self, vel, s_vel, dir)
            jammin.spin([0, 5], 300, 1)
        elif winner == 'jammin':
            jumin.spin([0, 5], 300, 1)

        blit_all(objects)

        fpsClock.tick(FPS)
        # pygame.event.post()

        # 11 - 화면 전체 업데이트
        pygame.display.flip()

        # 종료조건

        if jammin.outofscreen() or jumin.outofscreen():
            running = False
    oooooof.fadeout(fadeoutlength)


init_game()
start_screen()  # 시작화면 재생

while (1):
    winner = main_play()
    dyingeffect(winner)
    end_screen(winner)

    init_game()
