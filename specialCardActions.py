def startCardAction(player=None):
	print('ACTION START')
	player.cash += 400
	player.actionAnimation(f'+400$', 'darkgreen')
	print('Dodano 400$$')

def goToJailCardAction(player=None):
	pass

def payCardAction(player=None):
	player.cash -= 400
	player.actionAnimation(f'-400$', 'red')