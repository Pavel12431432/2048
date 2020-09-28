import random
import pygame

# size for each tile
tile_size = 128

# pygame initialization
pygame.init()
WIDTH, HEIGHT = tile_size * 4, tile_size * 4
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('2048')
pygame.display.set_icon(pygame.transform.scale(pygame.image.load('sprites/icon.png'), (32, 32)))
font = pygame.font.SysFont('consolas', 50)
clock = pygame.time.Clock()

# load tile sprites
tiles = {
	0: pygame.transform.scale(pygame.image.load('sprites/0.png').convert_alpha(), (tile_size, tile_size)),
	2: pygame.transform.scale(pygame.image.load('sprites/2.png').convert_alpha(), (tile_size, tile_size)),
	4: pygame.transform.scale(pygame.image.load('sprites/4.png').convert_alpha(), (tile_size, tile_size)),
	8: pygame.transform.scale(pygame.image.load('sprites/8.png').convert_alpha(), (tile_size, tile_size)),
	16: pygame.transform.scale(pygame.image.load('sprites/16.png').convert_alpha(), (tile_size, tile_size)),
	32: pygame.transform.scale(pygame.image.load('sprites/32.png').convert_alpha(), (tile_size, tile_size)),
	64: pygame.transform.scale(pygame.image.load('sprites/64.png').convert_alpha(), (tile_size, tile_size)),
	128: pygame.transform.scale(pygame.image.load('sprites/128.png').convert_alpha(), (tile_size, tile_size)),
	256: pygame.transform.scale(pygame.image.load('sprites/256.png').convert_alpha(), (tile_size, tile_size)),
	512: pygame.transform.scale(pygame.image.load('sprites/512.png').convert_alpha(), (tile_size, tile_size)),
	1024: pygame.transform.scale(pygame.image.load('sprites/1024.png').convert_alpha(), (tile_size, tile_size)),
	2048: pygame.transform.scale(pygame.image.load('sprites/2048.png').convert_alpha(), (tile_size, tile_size)),
	4096: pygame.transform.scale(pygame.image.load('sprites/4096.png').convert_alpha(), (tile_size, tile_size)),
	8192: pygame.transform.scale(pygame.image.load('sprites/8192.png').convert_alpha(), (tile_size, tile_size))
}


# function to slide array right
# [0, 2, 0, 4] -> [0, 0, 2, 4]
def slide(a):
	return [0] * a.count(0) + list(filter(lambda x: x, a))


# function to combine elements in array to the right
# [4, 4, 2, 2] -> [0, 8, 0, 4]
def combine(a):
	for i in range(3):
		if a[2 - i] == a[3 - i]:
			a[2 - i], a[3 - i] = 0, a[2 - i] + a[3 - i]
	return a


# add a tile to the board (2 or 4)
def add_tile():
	global grid
	valid = []
	for i in range(4):
		for j in range(4):
			if not grid[i][j]:
				valid.append((i, j))
	pos = random.choice(valid)
	grid[pos[0]][pos[1]] = random.randint(1, 2) * 2


# draw grid to screen
def draw():
	screen.fill((160, 150, 140))
	for i in range(4):
		for j in range(4):
			screen.blit(tiles[grid[i][j]], (j * tile_size, i * tile_size))
			if grid[i][j]:
				screen.blit(font.render(str(grid[i][j]), True, (95, 85, 75)),
							(j * tile_size + 64 - len(str(grid[i][j])) * 14, i * tile_size + 40))

	pygame.display.update()


# rotate 2d array by 90 degrees
# [0, 0, 2]		  	[2, 2, 0]
# [4, 0, 2]		->	[0, 0, 16]
# [8, 16, 0]	  	[0, 4, 8]
def rotate90(m):
	return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]) - 1, -1, -1)]


# rotate 2d array by -90 degrees
# [0, 0, 2]		  	[8, 4, 0]
# [4, 0, 2]		->	[16, 0, 0]
# [8, 16, 0]	  	[0, 2, 2]
def rotate270(m):
	return [list(x)[::-1] for x in zip(*m)]


# handle input
def inp():
	global grid
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == pygame.KEYDOWN:
			# make copy of current grid
			prev = grid
			if event.key == pygame.K_RIGHT:
				# if right arrow is pressed then slide the combine then slide the grid
				grid = [slide(combine(slide(grid[i]))) for i in range(4)]
			elif event.key == pygame.K_DOWN:
				# if down arrow is pressed then rotate grid by 90, slide, combine, slide and rotate 270
				grid = rotate270([slide(combine(slide(rotate90(grid)[i]))) for i in range(4)])
			elif event.key == pygame.K_UP:
				# if up arrow is pressed then rotate grid by 270, slide, combine, slide and rotate 90
				grid = rotate90([slide(combine(slide(rotate270(grid)[i]))) for i in range(4)])
			elif event.key == pygame.K_LEFT:
				# if left arrow is pressed then rotate grid by 90 twice, slide, combine, slide and rotate 90 twice
				grid = rotate90(rotate90([slide(combine(slide(rotate90(rotate90(grid))[i]))) for i in range(4)]))
			# if grid has changed then add a tile
			if not grid == prev:
				add_tile()


# initialize grid
grid = [[0] * 4 for i in range(4)]

# add 2 initial tiles
add_tile()
add_tile()

# main loop
while True:
	inp()
	draw()