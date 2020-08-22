import pygame
import sys
import random


##### Variables globales

gravedad = 0.25
alturasPipe = [400, 500, 800]
activo = True

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
		self.movimiento -= 12 

	def colision(self, pipeList):

		for pipe in pipeList:

			if self.hitbox.top <= -100 or self.hitbox.bottom >= 900 or pipe.colisionaCon(self.hitbox):
				return True
			
		return False





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



def main():

	pygame.init()
	pantalla = pygame.display.set_mode((576, 1024))
	clock = pygame.time.Clock()

	fondo = pygame.image.load("assets/background-day.png").convert()
	fondo = pygame.transform.scale2x(fondo)



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

			if event.type == PipeSpawner:
				listaPipes.append(Pipe(pantalla))

			


		piso.dibujar()
		activo = not bird.colision(listaPipes)

		if activo:

			for pipe in listaPipes:
				pipe.mover()
				pipe.dibujar()

			bird.dibujar()


		

		pygame.display.update()
		clock.tick(120)



main()