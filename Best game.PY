import pygame, random, sys

pygame.init()

# Initial windowed mode
screen = pygame.display.set_mode((800,600))
fullscreen = False
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Ultimate Money Clicker")

# Colors and fonts
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
RED = (255,0,0)
GRAY = (200,200,200)
BLUE = (0,0,255)
font = pygame.font.SysFont(None, 28)

# Player stats
money = 0
click_income = 1
player_items = []

# Shop scroll
shop_scroll = 0
shop_item_height = 30
search_text = ""
category_filter = ""

# Categories and items
categories = {
    "Cars": ["Rusty Smart Car", "Bugatti", "Ferrari", "Lamborghini", "Universe Cruiser"],
    "Houses": ["Broken House", "Cabin", "Mansion", "Skyscraper"],
    "Luxury Items": ["Yacht", "Private Jet", "Diamond Ring"],
    "Basic Items": ["Pencil", "Chair", "Phone", "Book"],
    "Universe": ["Planet", "Star", "Galaxy", "Universe"]
}

items = [{"id":0,"name":"Rusty Coin","price":1,"income":1,"category":"Basic Items"}]

# Generate 1000 more items
id_counter = 1
while len(items) < 1001:
    category = random.choice(list(categories.keys()))
    base_name = random.choice(categories[category])
    name = f"{base_name} #{random.randint(1,10000)}"
    price = random.randint(5,1000000)
    income = max(price // 10,1)
    items.append({"id":id_counter,"name":name,"price":price,"income":income,"category":category})
    id_counter += 1

items.sort(key=lambda x: x["price"])

# Clock
clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    dt = clock.tick(FPS) / 1.0
    mx,my = pygame.mouse.get_pos()

    # Passive income
    total_income_per_sec = sum(item["income"] for item in player_items)
    money += total_income_per_sec * (1/FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                search_text = search_text[:-1]
            elif event.key == pygame.K_DOWN:
                shop_scroll += shop_item_height
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                # Toggle fullscreen/windowed
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((800,600))
                WIDTH, HEIGHT = screen.get_size()
            else:
                search_text += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if 10 < mx < 210 and 50 < my < 90:
                    money += click_income
                shop_y = 100 - shop_scroll
                search_lower = search_text.lower()
                filtered_items = [i for i in items if (category_filter=="" or i["category"]==category_filter) and search_lower in i["name"].lower()]
                for item in filtered_items:
                    if 10 < mx < WIDTH-10 and shop_y < my < shop_y + shop_item_height:
                        if money >= item["price"]:
                            money -= item["price"]
                            player_items.append(item)
                    shop_y += shop_item_height

    # Draw UI
    pygame.draw.rect(screen,YELLOW,(10,50,200,40))
    screen.blit(font.render(f"Money: ${int(money)}",True,BLACK),(15,55))
    screen.blit(font.render("Click to Earn Money",True,BLACK),(15,70))

    # Search box
    pygame.draw.rect(screen,WHITE,(10,10,200,30))
    screen.blit(font.render(search_text,True,BLACK),(15,15))

    # Categories
    x_offset = 220
    for cat in categories.keys():
        color = BLUE if cat==category_filter else WHITE
        pygame.draw.rect(screen,color,(x_offset,10,100,30))
        screen.blit(font.render(cat,True,BLACK),(x_offset+5,15))
        x_offset += 110
        if pygame.mouse.get_pressed()[0]:
            if x_offset-110 < mx < x_offset-10 and 10 < my < 40:
                category_filter = cat

    # Render shop
    shop_y = 100 - shop_scroll
    search_lower = search_text.lower()
    filtered_items = [i for i in items if (category_filter=="" or i["category"]==category_filter) and search_lower in i["name"].lower()]
    for item in filtered_items:
        color = GREEN if money >= item["price"] else RED
        pygame.draw.rect(screen,color,(10,shop_y,WIDTH-20,shop_item_height-2))
        screen.blit(font.render(f"{item['name']} - ${item['price']} (Income:{item['income']}/s)",True,BLACK),(15,shop_y+5))
        shop_y += shop_item_height

    pygame.display.flip()
