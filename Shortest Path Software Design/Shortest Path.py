import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

def pause():
	paused = True
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()


class Pathfinder:
	def __init__(self, matrix):

		# setup
		self.matrix = matrix
		self.grid = Grid(matrix = matrix)
		self.select_surf = pygame.image.load('Yo.png').convert_alpha()
		

		# pathfinding
		self.path = []

		# player
		self.irene = pygame.sprite.GroupSingle(Gesta(self.empty_path))

	def empty_path(self):
		self.path = []

	def draw_active_cell(self):
		mouse_pos = pygame.mouse.get_pos()
		row =  mouse_pos[1] // 32
		col =  mouse_pos[0] // 32
		current_cell_value = self.matrix[row][col]
		if current_cell_value == 1:
			rect = pygame.Rect((col * 32, row * 32),(32, 32))
			screen.blit(self.select_surf, rect)

	def create_path(self):

		# start
		start_x, start_y = self.irene.sprite.get_coord()
		start = self.grid.node(start_x,start_y)

		# end
		mouse_pos = pygame.mouse.get_pos()
		end_x, end_y =  mouse_pos[0] // 32, mouse_pos[1] // 32  
		end = self.grid.node(end_x,end_y) 

		# path
		finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
		self.path,_ = finder.find_path(start,end,self.grid)
		self.grid.cleanup()
		self.irene.sprite.set_path(self.path)

	def draw_path(self):
		if self.path:
			points = []
			for point in self.path:
				x = (point.x * 32) + 16
				y = (point.y * 32) + 16
				points.append((x,y))
				pygame.draw.circle(screen, 'red', (x, y), 10)
			pygame.draw.lines(screen,'yellow', False, points, 5)

	def update(self):
		self.draw_active_cell()
		self.draw_path()

		# player updating and drawing
		self.irene.update()
		self.irene.draw(screen)


class Gesta(pygame.sprite.Sprite):
	def __init__(self,empty_path):

		# basic
		super().__init__()
		self.image = pygame.image.load('Irene.png').convert_alpha()
		self.rect = self.image.get_rect(center = (40,370))

		# movement 
		
		self.pos = self.rect.center
		self.speed = 2
		self.direction = pygame.math.Vector2(0,0)

		# path
		self.path = []
		self.collision_rects = []
		self.empty_path = empty_path

	def get_coord(self):
		col = self.rect.centerx // 32
		row = self.rect.centery // 32
		return (col,row)

	def set_path(self,path):
		self.path = path
		self.create_collision_rects()
		self.get_direction()

	def create_collision_rects(self):
		if self.path:
			self.collision_rects = []
			for point in self.path:
				x = (point.x * 32) + 16
				y = (point.y * 32) + 16
				rect = pygame.Rect((x - 2,y - 2),(4,4))
				self.collision_rects.append(rect)

	def get_direction(self):
		if self.collision_rects:
			start = pygame.math.Vector2(self.pos)
			end = pygame.math.Vector2(self.collision_rects[0].center)
			self.direction = (end - start).normalize()
		else:
			self.direction = pygame.math.Vector2(0,0)
			self.path = []

	def check_collisions(self):
		if self.collision_rects:
			for rect in self.collision_rects:
				if rect.collidepoint(self.pos):
					del self.collision_rects[0]
					self.get_direction()
		else:
			self.empty_path()

	def update(self):
		self.pos += self.direction * self.speed
		self.check_collisions()
		self.rect.center = self.pos

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280,736))
clock = pygame.time.Clock()

# game setup
bg_surf = pygame.image.load('Bored.jpg').convert()
matrix = [
	[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0],
	[1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,1,1,1,1,1,1],
	[1,0,0,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1,0,0,0,0,0,1,1,1,1,1,0],
	[1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0],
	[1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0],
	[1,0,0,1,0,0,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[1,0,0,1,1,1,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0],
	[1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0],
	[1,1,0,1,0,0,1,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0],
	[1,1,1,1,0,0,1,0,0,1,0,1,1,1,1,1,1,1,1,0,0,1,1,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0],
	[1,0,0,1,1,1,1,0,0,1,0,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
	[1,0,0,1,0,0,1,0,0,1,0,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,1,1,0,1,1,1,1,1,1,1,1,0],
	[1,0,0,1,0,0,1,0,0,1,0,1,1,1,1,1,1,1,1,0,0,1,1,0,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0],
	[1,0,0,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,1,0,0,0],
	[1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,0,1,1,1,0,1,1,0,0,0,0,0,0,1,0,0,0],
	[1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1],
	[1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
pathfinder = Pathfinder(matrix)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			pathfinder.create_path()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p:
				pause()

	screen.blit(bg_surf,(0,0))
	pathfinder.update()

	pygame.display.update()
	clock.tick(300)