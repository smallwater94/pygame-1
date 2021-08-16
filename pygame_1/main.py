import pygame
import  random

# 初始化
pygame.init()

# 創建視窗
WIDTH = 1000
HIGH = 1000
screen = pygame.display.set_mode((WIDTH, HIGH))

# 標題
pygame.display.set_caption('First Game By York')

# 時間管理
clock = pygame.time.Clock()

# 遊戲幀數
FPS = 60

# 各類顏色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)



# 物件
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HIGH - 10
        self.speed = 10

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speed

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HIGH:
            self.rect.bottom = HIGH

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.n = 0
        self.width = 30
        self.high = 30
        self.image = pygame.Surface((self.width, self.high))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(10, 40)
        self.speedx = random.randrange(-10, 10)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HIGH:
            self.rect.x = random.randrange(0, WIDTH - self.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(10, 40)
            self.speedx = random.randrange(-10, 10)

# 物件群組，所有物件聽命於此
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(20):
    rock = Rock()
    all_sprites.add(rock)

# 遊戲狀態
running = True
# 遊戲迴圈
while running:
    clock.tick(FPS)  # 遊戲FPS
    # 取得輸入
    for event in pygame.event.get():  # 如果點擊右上角的叉叉則結束遊戲
        if event.type == pygame.QUIT:
            running = False
    # 更新遊戲
    all_sprites.update()

    # 畫面顯示
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.update()

# 遊戲結束
pygame.quit()
