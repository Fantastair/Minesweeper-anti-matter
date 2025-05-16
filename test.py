# import pygame

# pygame.init()
# screen = pygame.display.set_mode((1,1))

# c1 = pygame.Color((160, 160, 160, 160))
# test_surface1 = pygame.Surface((1,1))
# test_surface1.set_at((0,0), c1)
# test_surface1.set_alpha(160)
# c2 = pygame.Color((45, 45, 45, 45))
# test_surface2 = pygame.Surface((1,1))
# test_surface2.set_at((0,0), c2)
# test_surface2.set_alpha(45)
# '''
# BLEND_RGB_ADD 1
# BLEND_RGB_SUB 2
# BLEND_RGB_MULT 3
# BLEND_RGB_MIN 4
# BLEND_RGB_MAX 5
# BLEND_RGBA_ADD 6
# BLEND_RGBA_SUB 7
# BLEND_RGBA_MULT 8
# BLEND_RGBA_MIN 9
# BLEND_RGBA_MAX 16
# BLEND_PREMULTIPLIED 17
# BLEND_ALPHA_SDL2 18
# '''

# print(test_surface1.get_at((0,0)))
# print(test_surface2.get_at((0,0)))
# # test_surface1.blit(test_surface2, (0,0))# , special_flags=pygame.BLEND_ADD)
# test_surface1.blit(test_surface2, (0,0), special_flags=pygame.BLEND_RGB_ADD)
# # print(pygame.BLEND_ADD)
# print(test_surface1.get_at((0,0)))
# # from pygame.locals import *
# # g = dict(globals())

# # for i in g:
# # 	if 'BLEND' in i:
# # 		print(i, g[i])
	# if Num < area / 2:
	#     y = [0] * (area - Num) + [-1] * Num
	#     random.shuffle(y)
	# else:
	#     y = [-1] * Num + [0] * (area - Num)
	#     random.shuffle(y)

# import fantas
# '''
# data = pickle.load('userdata')
# data = pickle.load('userdata - safety')
'''
data = {
	'map_size': (16, 16),
	'difficulty': 'medium',
	'music_volume': 80,
	'sound_volume': 80,
	'show_hovermessage': False,
	'skip_startani': False,
}
# '''
# data['version'] = '1.0'
# print(data)
# pickle.dump(data, 'userdata')
# pickle.dump(data, 'userdata - safety')
# data[((16, 16), 'easy')] = 500
# data[((30,16),'easy')] = 128
# data[((30,16),'medium')] = 365

# from tempfile import TemporaryFile

# 	f.write(data)
# import fantas
# data = fantas.load('userdata')

# del data[((16,16),'easy')]
# del data[((16,16),'medium')]
# del data[((16,16),'difficult')]
# del data[((30,16),'easy')]
# del data[((30,16),'medium')]
# del data[((30,16),'difficult')]
# del data['version']
# data['map_size'] = (16, 16)

# data['use_cheat'] = True
# print(data)

# fantas.dump(data, 'userdata')

from pathlib import Path

path = 'C:/Python/12.扫雷（反物质版） - 副本/fantas'

for i in Path(path+'/__pycache__').iterdir():
	i_ = i.name.split('.')
	name = '.'.join((i_[0], i_[-1]))
	with i.open('rb') as f1:
		with Path(f'{path}/{name}').open('wb') as f2:
			f2.write(f1.read())

