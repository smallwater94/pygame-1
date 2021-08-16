import pygame
import random

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
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 97, 0)
Green = (255, 0, 255)
# 字體載入
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_recy = pygame.Rect(x, y, BAR_LENGTH, BAR_HIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HIGHT)
    pygame.draw.rect(surf, Green, fill_rect)
    pygame.draw.rect(surf, Green, outline_recy, 2)

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
        self.helf = 100

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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add((bullet))
        bullets.add(bullet)


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
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HIGH:
            self.rect.x = random.randrange(0, WIDTH - self.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-2, 2)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.n = 0
        self.width = 10
        self.high = 30
        self.image = pygame.Surface((self.width, self.high))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# 物件群組，所有物件聽命於此
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
players = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
players.add(player)
for i in range(20):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# 遊戲狀態
running = True
# 遊戲迴圈

score = 0

while running:
    clock.tick(FPS)  # 遊戲FPS
    # 取得輸入
    for event in pygame.event.get():  # 如果點擊右上角的叉叉則結束遊戲
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # 更新遊戲
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        score += 100
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)

    hits = pygame.sprite.groupcollide(players, rocks, False, True)
    for hit in hits:
        player.helf -= 10
        if player.helf <= 0:
            running = False

    # 畫面顯示
    screen.fill(WHITE)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health(screen, player.helf, 5, 10)
    pygame.display.update()

# 遊戲結束
pygame.quit()
