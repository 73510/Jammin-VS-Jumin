# 1 - 모듈 임포트
import pygame
import random
import pyautogui


#모든 전역 변수
width, height= pyautogui.size()
screen_size = (width, height)
FPS = 60
velocitylvl = 3


#obj를 위한 클래스 생성
class py_object:

    def __init__(self, surf, pos, velocity, dir):
        self.surface = surf
        self.pos = pos
        self.vel = velocity
        self.dir = dir # 0 for x, 1 for y

    def inscreen(self, other):
        pos = other[0]
        screensize = other[1]
        rect = pygame.Rect(self.get_rect())
        print(rect)
        if pos[0] >= 0 and pos[0] <= screensize[0] and 0 <= pos[1] and pos[1] <= screensize[1]:
            return True
        return False

    def move_tick(self, screensize):
        next = (0, 0)
        if self.dir == 0:
            next = (self.pos[0] + self.vel, self.pos[1])
        if self.dir == 1:
            next = (self.pos[0], self.pos[1] + self.vel)

        print(next, screensize)
        if inscreen(self, (next, screensize)):
            self.pos = next

def move_obj(obj):

    if obj.dir == 0:
        obj.pos = (obj.pos[0] + obj.vel, obj.pos[1])
    if obj.dir == 0:
        obj.pos = (obj.pos[0] + obj.vel, obj.pos[1])



# 2 - 게임 변수 초기화
# 2.1 - 게임 화면

def init_game():
    global screen, fpsClock, score, spaceshipimg, gameover, sharkimg_original, takeoffsound, landingsound, sharkimg_resized
    global black, white

    global jamminimg
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

    try:
        # 3 - 그림과 효과음 삽입
        # 3.1 - 그림 삽입
        spaceshipimg = pygame.image.load("./img/spaceship.png")
        gameover = pygame.image.load("./img/gameover.jpg")
        sharkimg_original = pygame.image.load("./img/shark.jpg")

        jamminimg = pygame.image.load("./img/jamminface.jpg")

        # 3.2 - 효과음 삽입

        # 3.3 - 폰트 삽입

    except Exception as err:
        print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
        pygame.quit()
        exit(0)
    sharkimg_resized = pygame.transform.scale(sharkimg_original, (120, 50))

# 4 - 점수 출력
def text(arg, coord, fontsize, fontcolor):
    x = coord[0]
    y = coord[1]
    font = pygame.font.Font('./public-pixel-font/arcadelit.ttf', fontsize)
    text = font.render(str(arg), False, fontcolor)
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    screen.blit(text, textRect)

def move_(pos, speed, dir):
    if dir == 1:
        return (pos[0], pos[1] + speed)
    elif dir == 0:
        return (pos[0]+speed, pos[1])

def start_screen():
    screen.fill(white)
    screen_center = (screen_size[0]/2, screen_size[1]/2)
    text("Jammin likes Jumin", screen_center, 30, black)

    text("Press any key to start", (screen_center[0], screen_center[1] + 60), 20, black)

    pygame.display.flip()

def move_sprite(pos, keytype):
    pos = list(pos)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pos[1] -= 10
            elif event.key == pygame.K_s :
                pos[1] += 10
            elif event.key == pygame.K_a :
                pos[0] -= 10
            elif event.key == pygame.K_s:
                pos[0] +=10
    print(pos)
    return tuple(pos)

def inscreen(surface):
    rect = surface.get_rect()
    if rect.left >= 0 and rect.right <= screen_size[0] and 0 <= rect.top and rect.bottom <= screen_size[1]:
        return True
    return False

init_game()
start_screen() #시작화면 재생

proceed = False
while  not (proceed):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            proceed = True

# 5 - 게임 루프
running = True

sharkpos = (140, 200)
spaceshippos = [150, 50]

spaceship_v = (0, 0)
while running:
    # 6 - 화면을 그리기에 앞서 화면을 흰색으로 지우기
    screen.fill((255, 255, 255))

    # 7 - 키보드/마우스 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                spaceship_v = (0, -velocitylvl)
            elif event.key == pygame.K_s :
                spaceship_v = (0, +velocitylvl)
            elif event.key == pygame.K_a :
                spaceship_v = (-velocitylvl, 0)
            elif event.key == pygame.K_d:
                spaceship_v = (+velocitylvl, 0)
            if event.key == pygame.K_ESCAPE:
                exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s :
                spaceship_v = (spaceship_v[0], 0)
            if event.key == pygame.K_a or event.key == pygame.K_d :
                spaceship_v = (0, spaceship_v[1])

    # 9 - 게임 요소 상태 변경
    # 9.1 - spaceship 이동/그리기
    nextspaceshippos = (spaceshippos[0] + spaceship_v[0], spaceshippos[1] + spaceship_v[1])
    #if inscreen(spaceship):
    #    spaceshippos = nextspaceshippos

    spaceship_ = py_object(spaceshipimg, spaceshippos, 1, 10)


    screen.blit(sharkimg_resized, sharkpos)
    screen.blit(jamminimg, spaceshippos)
    # spaceship 사각형
    spaceshiprect = pygame.Rect(spaceshipimg.get_rect())
    spaceshiprect.left = spaceshippos[0]
    spaceshiprect.top = spaceshippos[1]

    #spaceship_.move_tick(screen_size)


    sharkpos = move_(sharkpos, 10, 1)


    # 10 - 게임 속도
    fpsClock.tick(FPS)

    # 11 - 화면 전체 업데이트
    pygame.display.flip()


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

