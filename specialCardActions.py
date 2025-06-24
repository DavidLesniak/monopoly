def payCardAction(player=None):
	player.cash -= 400
	player.actionAnimation(f'-400$', 'red')