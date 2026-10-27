import pygame
import asyncio

def main():
    pygame.init()
    W, H = 600, 400
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pong - W/S, Up/Down, or Touch")
    font = pygame.font.Font(None, 48)
    sfont = pygame.font.Font(None, 20)
    
    PAD_W, PAD_H = 12, 80
    BALL_SIZE = 10
    
    p1_y = H//2 - PAD_H//2
    p2_y = H//2 - PAD_H//2
    bx, by = W//2, H//2
    bdx, bdy = 4, 3
    score1, score2 = 0, 0
    speed = 5
    
    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type in (pygame.FINGERDOWN, pygame.FINGERMOTION):
                fx = int(event.x * W)
                fy = int(event.y * H)
                if fx < W // 2:
                    p1_y = max(0, min(H - PAD_H, fy - PAD_H // 2))
                else:
                    p2_y = max(0, min(H - PAD_H, fy - PAD_H // 2))
    
        # Keyboard controls
        if keys[pygame.K_w] and p1_y > 0:
            p1_y -= speed
        if keys[pygame.K_s] and p1_y < H - PAD_H:
            p1_y += speed
        if keys[pygame.K_UP] and p2_y > 0:
            p2_y -= speed
        if keys[pygame.K_DOWN] and p2_y < H - PAD_H:
            p2_y += speed
    
        # Touch/mouse: left half controls P1, right half controls P2
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if mx < W // 2:
                p1_y = max(0, min(H - PAD_H, my - PAD_H // 2))
            else:
                p2_y = max(0, min(H - PAD_H, my - PAD_H // 2))
    
        bx += bdx
        by += bdy
    
        if by <= 0 or by >= H - BALL_SIZE:
            bdy = -bdy
    
        # Paddle collision
        if bx <= 30 and p1_y <= by <= p1_y + PAD_H:
            bdx = abs(bdx)
        if bx >= W - 30 - BALL_SIZE and p2_y <= by <= p2_y + PAD_H:
            bdx = -abs(bdx)
    
        # Scoring
        if bx < 0:
            score2 += 1
            bx, by, bdx = W//2, H//2, 4
        if bx > W:
            score1 += 1
            bx, by, bdx = W//2, H//2, -4
    
        screen.fill((15, 15, 35))
        pygame.draw.rect(screen, (66, 133, 244), (15, p1_y, PAD_W, PAD_H), border_radius=4)
        pygame.draw.rect(screen, (239, 68, 68), (W-15-PAD_W, p2_y, PAD_W, PAD_H), border_radius=4)
        pygame.draw.rect(screen, (255,255,255), (bx, by, BALL_SIZE, BALL_SIZE))
        pygame.draw.aaline(screen, (50,50,70), (W//2, 0), (W//2, H))
    
        t = font.render(f"{score1}  {score2}", True, (200,200,200))
        screen.blit(t, (W//2 - t.get_width()//2, 15))
        hint = sfont.render("W/S + Up/Down or touch left/right side", True, (60,60,80))
        screen.blit(hint, (W//2 - hint.get_width()//2, H - 20))
    
        pygame.display.flip()
        await asyncio.sleep(1/60)
    
    pygame.quit()

if __name__ == '__main__':
    main()
