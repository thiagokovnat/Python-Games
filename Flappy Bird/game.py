import pygame
import sys
import random


##### Variables globales

gravedad = 0.25
alturasPipe = [400, 500, 800]
activo = False


################################### PISO ######################################################################
class Piso():

	def __init__(self, pantalla):

		self.pantalla = pantalla
		self.posicionPisoX = 0
		self.imagen = pygame.image.load("assets/base.png")
		self.imagen = pygame.transform.scale2x(self.imagen)
		

	def dibujar(self):
		
		self.posicionPisoX -= 1
		self.pantalla.blit(self.imagen, (self.posicionPisoX, 900))
		self.pantalla.blit(self.imagen, (self.posicionPisoX + 576, 900))

		if self.posicionPisoX <= -576:
			self.posicionPisoX = 0

################################### BIRD ######################################################################
class Bird():

	def __init__(self, pantalla):

		self.pantalla = pantalla
		self.imagen = pygame.image.load("assets/bluebird-midflap.png")
		self.imagen = pygame.transform.scale2x(self.imagen)
		self.hitbox = self.imagen.get_rect(center = (100, 512))
		self.rotado = self.imagen.get_rect(center = (100, 512))
		self.movimiento = 0

	def dibujar(self):

		self.movimiento += gravedad
		self.rotar()
		
		self.hitbox.centery += self.movimiento
		self.pantalla.blit(self.rotado , self.hitbox)

	def rotar(self):
		self.rotado = pygame.transform.rotozoom(self.imagen , - (self.movimiento * 2), 1)

	def saltar(self):

		self.movimiento = 0
		self.movimiento -= 10 

	def colision(self, pipeList):

		for pipe in pipeList:

			if self.hitbox.top <= -100 or self.hitbox.bottom >= 900 or pipe.colisionaCon(self.hitbox):
				return True
			
		return False



################################### PIPE ######################################################################
class Pipe():

	def __init__(self, pantalla):

		self.pantalla = pantalla
		self.imagen = pygame.image.load("assets/pipe-green.png")
		self.imagen = pygame.transform.scale2x(self.imagen)
		self.imagenInvertida = pygame.transform.flip(self.imagen, False, True)

		randomAltura = random.choice(alturasPipe)
		self.hitboxInferior = self.imagen.get_rect(midtop = (700, randomAltura))
		self.hitboxSuperior = self.imagen.get_rect(midbottom = (700, randomAltura - 300))

	def mover(self):

		self.hitboxSuperior.centerx -= 5
		self.hitboxInferior.centerx -= 5

	def dibujar(self):


		self.pantalla.blit(self.imagen, self.hitboxInferior)
		self.pantalla.blit(self.imagenInvertida, self.hitboxSuperior)

	def colisionaCon(self, hitboxBird):

		return self.hitboxInferior.colliderect(hitboxBird) or self.hitboxSuperior.colliderect(hitboxBird)



################################### SCORE ######################################################################
class Score():

	def __init__(self, pantalla, highScore):

		self.score = 0
		self.highScore = highScore
		self.font = pygame.font.Font("04B_19.TTF", 30)
		self.pantalla = pantalla

	def dibujar(self, estado):

		if estado:
			surfaceScore = self.font.render(str(int(self.score)), True, (255, 255, 255))

		else:
			surfaceScore = self.font.render("High Score: " + str(int(self.highScore)), True, (255, 255, 255))
			
		rect = surfaceScore.get_rect(center = (288, 100))
		self.pantalla.blit(surfaceScore, rect)

	def update(self):

		self.score += 0.01
		if self.score > self.highScore:
			self.highScore = self.score

		return self.highScore


################################################################################################################

def main():

	pygame.init()
	pygame.display.set_caption("Flappy Bird")

	pantalla = pygame.display.set_mode((576, 1024))
	clock = pygame.time.Clock()
	
	highScore = 0
	score = Score(pantalla, highScore)

	fondo = pygame.image.load("assets/background-day.png").convert()
	fondo = pygame.transform.scale2x(fondo)

	gameOverFondo = pygame.image.load("assets/message.png")
	gameOverFondo = pygame.transform.scale2x(gameOverFondo)
	gameOverRect = gameOverFondo.get_rect(center = (288, 500))



	piso = Piso(pantalla)
	bird = Bird(pantalla)


	# Tubos
	listaPipes = []
	PipeSpawner = pygame.USEREVENT
	pygame.time.set_timer(PipeSpawner, 1200)

	while True:

		pantalla.blit(fondo, (0, 0))
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_SPACE and activo:
					bird.saltar()

				if event.key == pygame.K_SPACE and not activo:
					activo = True
					listaPipes.clear()
					bird = Bird(pantalla)
					score = Score(pantalla, highScore)

			if event.type == PipeSpawner:
				listaPipes.append(Pipe(pantalla))

			


		piso.dibujar()
		activo = not bird.colision(listaPipes)

		if activo:

			for pipe in listaPipes:
				pipe.mover()
				pipe.dibujar()

			bird.dibujar()
			highScore = score.update()

		else:
			pantalla.blit(gameOverFondo, gameOverRect)

		score.dibujar(activo)
		

		pygame.display.update()
		clock.tick(120)



main()