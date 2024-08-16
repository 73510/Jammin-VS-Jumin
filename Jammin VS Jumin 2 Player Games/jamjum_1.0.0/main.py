# 1 - 모듈 임포트
import pygame
import random
import pyautogui
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#모든 전역 변수
width, height= pyautogui.size()
screen_size = (width*0.8, height*0.8)
width = screen_size[0]
height = screen_size[1]
obj_scale = 1.0
charactersize = 2*int(1/30 * width) #우선 가로만 맞추는걸로
FPS = 60

sexy_pink = (245, 69, 221)
toxic_green = (22, 241, 4)  # (0, 0, 0)#(140, 12, 80)#(1, 255, 251 )
sexy_blue = (1, 255, 251)
blue = (16, 34, 217)
yello = (255, 243, 0)


def inscreen(pos, rect):
    if pos[0] - rect.center[0] >= 0 and pos[0] + rect.center[0] <= screen_size[0] and 0 <= pos[1] - rect.center[1] and pos[1] + rect.center[1] <= screen_size[1]:
        return True
    return False

def outofscreen(pos, rect):
    if pos[0] + rect.center[0] <= 0 and pos[0] - rect.center[0] >= screen_size[0] and 0 >= pos[1] + rect.center[1] and \
            pos[1] - rect.center[1] >= screen_size[1]:
        return True
    else:
        return False

#obj를 위한 클래스 생성
class py_object: #surface(pygame surface), pos(list pair), show(bool)

    #생성자 함수, surf - surface, pos - position, show - 활성화 여부, lock - 이동시 x축 lock 여부
    def __init__(self, surf, pos, show = True, angle = 0, lock = False, org_img = False):
        self.surface = surf
        self.pos = pos #object의 pos는 center위치로 저장되어있음
        self.show = show
        self.angle = angle
        self.lock = lock  # #l
        self.vel = [0, 0] # 이건 생성자에 안넣어줬음
        if not org_img:
            self.org_img = surf
        else : self.org_img = org_img

    def collision(self, object):
        self_rect = self.surface.get_rect() # 이후 object 의 rect를 상대위치만큼 이동시켜 줌
        #(centerx, centery) 된거니까

        #(-self.pos[0] + self_rect.centerx, -self.pos[1] + self_rect.centery)만큼 이동시킨거니까

        object_rect = object.surface.get_rect()
        object_rect.centerx += object.pos[0] -self.pos[0] #+ self_rect.centerx
        object_rect.centery += object.pos[1] -self.pos[1] #+ self_rect.centery

        return self_rect.colliderect(object_rect) and (self.show and object.show)

    def wallcollision(self):
        self_rect = self.surface.get_rect()
        return not inscreen(self.pos, self_rect)

    def outofscreen(self):
        rect = self.surface.get_rect()
        pos = self.pos
        if pos[0] + rect.center[0] <= 0 or pos[0] - rect.center[0] >= screen_size[0] or 0 >= pos[1] + rect.center[1] or pos[1] - rect.center[1] >= screen_size[1]:
            return True
        else:
            return False

    def move(self, arg = lambda x,y : True): #move의 vel은 단위벡터 두개
        vel = self.vel
        rect = self.surface.get_rect()
        next = [self.pos[0], self.pos[1]]
        if self.lock :
            next[1] += vel[1]
        else :
            next[0] += vel[0]
            next[1] += vel[1]

        if arg(next, rect):
            self.pos[0] = next[0]
            self.pos[1] = next[1]

    def spin(self, vel, s_vel, dir):
        self.vel[0] = vel[0]
        self.vel[1] = vel[1]
        angle_ = (s_vel)/FPS
        self.angle += angle_

        self.surface = pygame.transform.rotate(self.org_img, (-1)**dir * self.angle%360)

        self.move(lambda x, y : not outofscreen(x, y))

    def throwed(self, vel, s_vel, dir): #vel을 tuple(x, y)로 만듦)
        self.vel[0] = vel[0]
        self.vel[1] = vel[1]

        if self.show : self.spin(vel, s_vel, dir)

        if self.outofscreen():
            self.show = False
            pygame.event.post(event_throwfinished)

    def applykey(self, keytense4, vel):
        arg = lambda x, y : inscreen(x, y)


        if keytense4[0]:
            self.vel[1] = -vel
        elif keytense4[1]:
            self.vel[1] = +vel
        else :
            self.vel[1] = 0
        if keytense4[2]:
            self.vel[0] = -vel
        elif keytense4[3]:
            self.vel[0] = vel
        else :
            self.vel[0] = 0

        self.move(lambda x, y : inscreen(x, y))

def get_center_coord(object):
    rect = object.surface.get_rect()
    return (object.pos[0] - rect.center[0], object.pos[1] - rect.center[1])

def blit_all(objects): #blit by center coordinate
    for obj in objects:
        blit_pos = get_center_coord(obj)
        if obj.show:
            screen.blit(obj.surface, blit_pos)

def resizeimg(surface, width):
    rect = surface.get_rect()
    a = width / rect.width
    return  pygame.transform.scale(surface, (width, rect.height * a))
# 2 - 게임 변수 초기화
# 2.1 - 게임 화면

def init_game():
    global screen, fpsClock, score, sharkimg_original, sharkimg_resized
    global black, white

    global whamimg, wham, jamminimg, sharkimg_original, sharkimg_resized, juminimg, badmintonimg,badmintonstartpos
    global juminvel, jamminvel, juminstartpos, jamminstartpos, jumin, jammin, badminton, throwvel, throwconst
    global keytense_wsad, keytense_arrow, width, height

    global event_throwfinished, event_juminthrowstart, event_jamminthrowstart, event_tick, wham_start_t

    global HP_img, HP_jumin_obj, HP_jammin_obj, JAMMIN_HP, JUMIN_HP

    JAMMIN_HP = 100
    JUMIN_HP = 50
    HP_img = []
    HP_jumin_obj = []
    HP_jammin_obj = []

    wham_start_t = 0


    event_throwfinished = pygame.event.Event(pygame.USEREVENT, attr1 = 'THROWFINISHED')
    event_juminthrowstart = pygame.event.Event(pygame.USEREVENT, attr1 = "JUMINTHROW")
    event_jamminthrowstart = pygame.event.Event(pygame.USEREVENT, attr1 = "JAMMINTHROW")
    event_tick = pygame.event.Event(pygame.USEREVENT, attr1 = "tick")
    throwvel = [0, 0]
    throwconst = 40
    global juminthrow, jamminthrow

    juminthrow = False
    jamminthrow = False

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
        sharkimg_original = pygame.image.load("./img/shark.png")
        jamminimg = pygame.image.load("./img/jamminface.png")
        juminimg = pygame.image.load("./img/juminface.png")
        badmintonimg = pygame.image.load("./img/badminton.png")
        whamimg = pygame.image.load("./img/wham.png")

        #HP import
        hp_size = 200
        for i in range (0, 11):
            hp_dir = "./img/HP_/HP_" + str(i) + ".png"
            HP_img.append(resizeimg(pygame.image.load(hp_dir), hp_size))


        #open sounds
        global oooooof, oof, gta_ending, punch, fadeoutlength, throw
        fadeoutlength = 500

        oooooof = pygame.mixer.Sound("./audio/oooooof.mp3")
        oof = pygame.mixer.Sound("./audio/oof.mp3")
        gta_ending = pygame.mixer.Sound('./audio/gta_ending.mp3')
        punch = pygame.mixer.Sound('./audio/punch.mp3')
        throw = pygame.mixer.Sound('./audio/throw.mp3')

        #rescaling images
        juminimg = resizeimg(juminimg, charactersize)
        jamminimg = resizeimg(jamminimg, charactersize)
        badmintonimg = resizeimg(badmintonimg, int(charactersize*0.5))
        whamimg = resizeimg(whamimg, int(charactersize*2))
        sharkimg_resized = pygame.transform.scale(sharkimg_original, (120, 50))
        # 3.2 - 효과음 삽입

        # 3.3 - 폰트 삽입

    except Exception as err:
        print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
        pygame.quit()
        exit(0)

    juminvel = 10
    jamminvel = 10
    juminstartpos = [0 + width // 10 * 2, height // 2]
    jamminstartpos = [width // 10 * 8, height // 2]  # list로 만들어야 됨
    badmintonstartpos = [width//2, height//2]

    jumin = py_object(juminimg, juminstartpos, 1)
    jammin = py_object(jamminimg, jamminstartpos, 1) #마지막꺼 show
    badminton = py_object(badmintonimg, badmintonstartpos, 0)
    wham = py_object(whamimg, [100, 100], 0)

    HP_jumin_pos = [width * 0.1, height * 0.1]
    HP_jammin_pos = [width - width*0.1, height *0.1]

    for img in HP_img:
        HP_jumin_obj.append(py_object(img, HP_jumin_pos, 0))
        HP_jammin_obj.append(py_object(img, HP_jammin_pos, 0))

class init_object:
    global badminton, jumin, jammin, throwvel, throwconst
    def juminbadmintoninit():

        badminton.show = True
        badminton.pos[0] = jumin.pos[0]
        badminton.pos[1] = jumin.pos[1]

        badminton.vel = [jumin.vel[0] + throwconst, jumin.vel[1]]

    def jamminbadmintoninit():
        badminton.show = True
        badminton.pos[0] = jammin.pos[0]
        badminton.pos[1] = jammin.pos[1]

        badminton.vel = [jammin.vel[0] - throwconst, jammin.vel[1]]

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
    text_scale = int(1/60 *screen_size[0]* obj_scale)
    screen.fill(white)
    screen_center = (screen_size[0]/2, screen_size[1]/2)
    #screen, text, size, x, y,
    dropShadowText(screen, "Jammin likes Jumin", int(2 * text_scale),screen_center[0], screen_center[1],sexy_pink, yello)

    dropShadowText(screen, "Press any key to start", int(1 * text_scale), screen_center[0], screen_center[1] + 3* text_scale, sexy_pink, yello)

    juminface_spinned = resizeimg(pygame.image.load("./img/juminface.png"), charactersize)
    juminface_spinned = pygame.transform.rotate(juminface_spinned, 45)

    jamminface_spinned = resizeimg(pygame.image.load("./img/jamminface.png"), charactersize)
    jamminface_spinned = pygame.transform.rotate(jamminface_spinned, 0)

    love = pygame.image.load("./img/heart.png")
    love_rect = love.get_rect()
    screen.blit(juminface_spinned, (screen_center[0]*0.5, 300))
    screen.blit(jamminface_spinned,  (screen_center[0]*1.5, 350))
    screen.blit(love, (screen_center[0]-love_rect.centerx, screen_center[1]-love_rect.centery-300))

    pygame.display.flip()
    proceed = False
    while not (proceed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                proceed = True

def dropShadowText(screen, text, size, x, y, colour=(255,255,255), drop_colour=(128,128,128), font='./public-pixel-font/arcadelit.ttf'):
    # how much 'shadow distance' is best?
    dropshadow_offset = 1 + (size // 15)
    text_font = pygame.font.Font(font, size)
    # make the drop-shadow
    text_bitmap = text_font.render(text, True, drop_colour)
    r1 = text_bitmap.get_rect()
    r1.center = (x+dropshadow_offset, y+dropshadow_offset)
    screen.blit(text_bitmap, r1)
    # make the overlay text
    text_bitmap = text_font.render(text, True, colour)
    r2 = text_bitmap.get_rect()
    r2.center =(x , y)
    screen.blit(text_bitmap, r2)

def end_screen(winner):

    black = (0, 0, 0)
    global gta_ending

    juminwin_count = 2
    jamminwin_count = 4

    juminwin = []
    jamminwin = []

    #import winning images
    size = charactersize*3
    pos_ = [screen_size[0] / 2, screen_size[1] *0.2]
    for i in range(1, juminwin_count+1):
        img = pygame.image.load('./img/jumin_win/'+str(i) + '.png')
        juminwin.append(py_object(resizeimg(img, size), pos_, 1))
    for i in range(1, jamminwin_count +1):
        img = pygame.image.load('./img/jammin_win/' + str(i)+'.png')
        jamminwin.append(py_object(resizeimg(img, size), pos_, 1))
    gta_backgroundimg = pygame.image.load('./img/gta_background.jpg')
#screen, text, size, x, y, colour=(255,255,255), drop_colour=(128,128,128), font=None
    screen.blit(resizeimg(gta_backgroundimg, width), (0, 0))
    gta_ending.play()
    text_scale = int(1 / 60 * screen_size[0] * obj_scale)
    screen_center = (screen_size[0] / 2, screen_size[1] / 2)
    objects= []
    if winner == "jumin":
        dropShadowText(screen, "Jumin succeeded to run away!", int(2 * text_scale), screen_center[0], screen_center[1], colour = black, drop_colour= yello)
        #text("Jumin succeeded to run away!", screen_center, int(2 * text_scale), sexy_pink)
        juminpic = random.choice(juminwin)
        objects.append(juminpic)
        dropShadowText(screen, "Press space to restart", int(1 * text_scale), screen_center[0],screen_center[1] + 3 * text_scale, colour=black, drop_colour=yello)

    if winner == "jammin":
        dropShadowText(screen, "Jammin found his love!", int(2 * text_scale), screen_center[0], screen_center[1], colour = black, drop_colour= toxic_green)
        objects.append(random.choice(jamminwin))
        dropShadowText(screen, "Press space to restart", int(1 * text_scale), screen_center[0],screen_center[1] + 3 * text_scale, colour=black, drop_colour=toxic_green)

    blit_all(objects)
    '''
    juminface_spinned = resizeimg(pygame.image.load("./img/juminface.png"), charactersize)
    juminface_spinned = pygame.transform.rotate(juminface_spinned, 45)

    jamminface_spinned = resizeimg(pygame.image.load("./img/jamminface.png"), charactersize)
    jamminface_spinned = pygame.transform.rotate(jamminface_spinned, 0)
    
    love = pygame.image.load("./img/heart.png")
    love_rect = love.get_rect()
    screen.blit(juminface_spinned, (screen_center[0] * 0.5, 300))
    screen.blit(jamminface_spinned, (screen_center[0] * 1.5, 350))
    screen.blit(love, (screen_center[0] - love_rect.centerx, screen_center[1] - love_rect.centery - 300))
    '''
    pygame.display.flip()
    proceed = False
    while not (proceed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_SPACE:
                    proceed = True
    gta_ending.fadeout(fadeoutlength)
    main_play()

def get_key(events):
    global keytense_wsad, keytense_arrow
    global juminthrow, jamminthrow
    global juminbadmintonposinit

    for event in events:  #나중에 키보드 입력 함수 따로 만들기
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: keytense_wsad[0] = 1
            elif event.key == pygame.K_s: keytense_wsad[1] = 1
            elif event.key == pygame.K_a : keytense_wsad[2] = 1
            elif event.key == pygame.K_d: keytense_wsad[3] = 1
            elif event.key == pygame.K_UP: keytense_arrow[0] = 1
            elif event.key == pygame.K_DOWN : keytense_arrow[1] = 1
            elif event.key == pygame.K_LEFT: keytense_arrow[2] = 1
            elif event.key == pygame.K_RIGHT: keytense_arrow[3] = 1

            elif event.key == pygame.K_e : pygame.event.post(event_juminthrowstart)
            elif event.key == pygame.K_PERIOD : pygame.event.post(event_jamminthrowstart)

            elif event.key == pygame.K_ESCAPE:
                exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:keytense_wsad[0] = 0
            elif event.key == pygame.K_s:keytense_wsad[1] = 0
            elif event.key == pygame.K_a:keytense_wsad[2] = 0
            elif event.key == pygame.K_d:keytense_wsad[3] = 0
            elif event.key == pygame.K_UP: keytense_arrow[0] = 0
            elif event.key == pygame.K_DOWN : keytense_arrow[1] = 0
            elif event.key == pygame.K_LEFT: keytense_arrow[2] = 0
            elif event.key == pygame.K_RIGHT: keytense_arrow[3] = 0
        elif event == event_throwfinished:
            juminthrow = False
            jamminthrow = False

        elif event == event_juminthrowstart and (juminthrow == False) and (jamminthrow == False):
            init_object.juminbadmintoninit()
            juminthrow = True
            throw.stop()
            throw.play()

        elif event == event_jamminthrowstart and (juminthrow == False) and (jamminthrow == False):
            init_object.jamminbadmintoninit()
            jamminthrow = True
            throw.stop()
            throw.play()

def i_got_shot():
    global jumin, jammin, badminton, wham, wham_start_t, JUMIN_HP, JAMMIN_HP

    badmintondamage = 10

    if jammin.collision(badminton) and juminthrow == True:
        oof.play()
        punch.play()
        pygame.event.post(event_throwfinished)
        badminton.show = False
        wham_start_t = pygame.time.get_ticks()
        wham.pos[0] = jammin.pos[0]
        wham.pos[1] = jammin.pos[1]
        wham.show = True
        JAMMIN_HP -= badmintondamage

    if jumin.collision(badminton) and jamminthrow == True:
        oof.play()
        punch.play()
        pygame.event.post(event_throwfinished)
        badminton.show = False
        wham_start_t = pygame.time.get_ticks()
        wham.pos[0] = jumin.pos[0]
        wham.pos[1] = jumin.pos[1]
        wham.show = True

        JUMIN_HP -= badmintondamage

    if pygame.time.get_ticks() - wham_start_t >= 1000:
        wham.show = False

def HP_display ():
    global JAMMIN_HP, JUMIN_HP

    #print(JAMMIN_HP, JUMIN_HP)

    for i in range(0, 11):
        HP_jammin_obj[i].show = False
        HP_jumin_obj[i].show = False

    for i in range(0, 11):
        if i * 10 <= JAMMIN_HP < (i + 1) * 10 :
            HP_jammin_obj[i].show = True
            break
    for i in range(0, 11):
        if i * 5 <= JUMIN_HP < (i+1) * 5 :
            HP_jumin_obj[i].show = True
            break

def main_play():
    global jumin, jammin, throwvel, event_throwfinished, event_tick, wham

    running = True

    while running:
        # 6 - 화면을 그리기에 앞서 화면을 흰색으로 지우기
        screen.fill((255, 255, 255))

        # 7 - 키보드/마우스 이벤트
        get_key(pygame.event.get())

        jumin.applykey(keytense_wsad, juminvel)
        jammin.applykey(keytense_arrow, jamminvel)

        #badminton.throwed(35, 300, 0)
        jumin.lock = 1
        jammin.lock = 1

        #던지는 부분
        if juminthrow :
            badminton.throwed(badminton.vel, 600, 0)
            #(self, vel, s_vel, dir):  # vel을 tuple(x, y)로 만듦)
        if jamminthrow :
            badminton.throwed(badminton.vel, 600, 0)

        #던진거 맞았으면 처리
        i_got_shot()

        HP_display()


        objects = []
        objects.append(jumin)  # 나중에 objects 한꺼번에 다 셋팅
        objects.append(jammin)
        objects.append(badminton)
        objects.append(wham)
        for i in range(0, 11):
            objects.append(HP_jumin_obj[i])
            objects.append(HP_jammin_obj[i])

        blit_all(objects)

        fpsClock.tick(FPS)
        #pygame.event.post()

        # 11 - 화면 전체 업데이트
        pygame.display.flip()

        if JAMMIN_HP<= 0:
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
    oooooof.play()

    if winner == 'jammin':
        jumin.surface = jumindeadimg
        jumin.org_img = jumindeadimg
    elif winner == 'jumin':
        jammin.surface = jammindeadimg
        jammin.org_img = jammindeadimg


    running = True
    while(running):
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

        if winner == 'jumin' : #def spin(self, vel, s_vel, dir)
            jammin.spin([0, 5], 300, 1)
        elif winner == 'jammin':
            jumin.spin([0, 5], 300, 1)

        blit_all(objects)

        fpsClock.tick(FPS)
        # pygame.event.post()

        # 11 - 화면 전체 업데이트
        pygame.display.flip()

        #종료조건

        if jammin.outofscreen() or jumin.outofscreen():
            running = False
    oooooof.fadeout(fadeoutlength)

init_game()
start_screen() #시작화면 재생

while(1):
    winner = main_play()
    dyingeffect(winner)
    end_screen(winner)
    init_game()