import random

import fantas
from fantas import uimanager
u = uimanager
import style
import element.music_play as music_play
import element.game_time as game_time
import element.ensure as ensure


class GameMapMouseWidget(fantas.MouseBase):
	__slots__ = ('last_pos')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.last_pos = None

	def mouserelease(self, pos, button):
		if button == 1:
			self.ui.press(pos)
		elif button == 3:
			self.ui.set_flag(pos)

	def mousemove(self, pos):
		pos = self.ui.transform_to_xy((pos[0] - self.ui.rect.left, pos[1] - self.ui.rect.top))
		if pos != self.last_pos:
			if self.last_pos is not None:
				self.ui.highlight_block(self.last_pos, False)
			if pos is not None and not self.ui.get_block(*pos).is_root():
				self.ui.highlight_block(pos, True)
				music_play.play_sound('click')
			self.last_pos = pos


class GameMap(fantas.Label):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.started = False
		self.map_side = (16, 16)
		self.change_side = fantas.LabelKeyFrame(self, 'size', None, 40, u.harmonic_curve)
		self.block_group = [fantas.Label((0,0), bg=u.color['BLOCKBG'], radius={'border_radius': 4}) for i in range(480)]
		self.circle_choose = CircleChooseKeyFrame(self)
		self.line_choose = LineChooseKeyFrame(self)
		self.cheat = Cheat(self)
		self.delay = fantas.Trigger()
		self.mousewidget = GameMapMouseWidget(self, 2)
		self.labelkeyframe_group = []
		self.block_label_link = {}
		self.block_rect_link = {}

	def start_game(self):
		self.flag = {}
		self.to_remove = []
		if u.userdata['map_size'] != self.map_side:
			self.map_side = u.userdata['map_size']
			self.change_side.value = (10+whole*self.map_side[0]+block_size[1], 10+whole*self.map_side[1]+block_size[1])
			self.change_side.launch('continue')
		else:
			self.change_side.value = (10+whole*self.map_side[0]+block_size[1], 10+whole*self.map_side[1]+block_size[1])
		for i in range(len(self.block_group[:self.map_side[0]*self.map_side[1]])):
			self.block_group[i].rect.center = (self.bd+block_size[1]+whole*(i%self.map_side[0])+block_size[0]/2, self.bd+block_size[1]+whole*(i//self.map_side[0])+block_size[0]/2)
			self.block_group[i].join(self)
		if self.map_side[0] == 16:
			self.curve = bounce_curve1
			self.circle_choose.st = 60
		else:
			self.curve = bounce_curve2
			self.circle_choose.st = 80
		self.delay.bind_endupwith(self.circle_choose.launch)
		self.delay.launch(150)
		self.create_data()
		self.checked_pos = []
		self.unchecked_blank = self.map_side[0]*self.map_side[1] - self.mine_num
		self.unchecked_mine = '+-'
		self.checked_mine = []
		self.rotate_point = (
			self.get_block(self.map_side[0]-1, 0).rect.center,
			self.get_block(0, 0).rect.center,
			self.get_block(0, self.map_side[1]-1).rect.center,
			self.get_block(self.map_side[0]-1, self.map_side[1]-1).rect.center,
			(self.change_side.value[0]/2,self.change_side.value[1]/2)
			)

	def end_game(self, winned):
		self.started = False
		self.mousewidget.cancel_event()
		game_time.time_ticker.stop()
		music_play.fadeout(500)
		if winned:
			music_play.play_sound('winned')
			used_time = game_time.clock_time.get_time()
			if used_time < u.userdata.get((self.map_side, u.userdata['difficulty']),float('+inf')):
				u.userdata[(self.map_side, u.userdata['difficulty'])] = used_time
				show_modeinfo(True)
			self.line_choose.init()
			self.line_choose.launch()
		else:
			music_play.play_sound('lost')
			c = fantas.CircleLabel(0, bg=u.color['TEXTGRAY' if self.get_data(*self.checked_mine[-1][0])=='+' else 'TEXTWHITE'], center=(self.rect.w/2,self.rect.h/2))
			c.join(self)
			self.to_remove.append(c)
			c.alpha = 200
			fantas.LabelKeyFrame(c, 'radius', (self.rect.w**2+self.rect.h**2)**0.5, 128, u.harmonic_curve).launch()
		for i in self.checked_mine:
			y = i[0][1] < self.map_side[1]/2
			xx = 3 - 3*y + (i[0][0]<self.map_side[0]/2) * (2*y-1)
			i[1].style = dict(i[1].style)
			i[1].style['rotation'] = 0
			i[1].style['fgcolor'] = u.color['TEXTWHITE' if self.get_data(*i[0])=='+' else 'TEXTGRAY']
			i[1].move_top()
			b = fantas.BezierRectKeyFrame(i[1], 'center', 80, fantas.BezierCurve((i[1].rect.center, self.rotate_point[(xx+1)%4], self.rotate_point[(xx+2)%4], self.rotate_point[4])))
			b.launch()
			b.bind_endupwith(i[1].leave)
			fantas.TextKeyFrame(i[1], 'rotation', 360, 80, u.curve).launch()
			fantas.TextKeyFrame(i[1], 'size', 100, 80, u.curve).launch()
		if self.checked_mine:
			b.bind_endupwith(end_game, winned, i[1], self.get_data(*i[0])=='+')
		elif winned:
			fantas.Trigger().launch(80).bind_endupwith(end_game, winned, None, True)

	def reset_game(self):
		for i in self.block_group:
			i.set_size((0,0))
			if i.father is not None:
				i.leave()
		for i in self.to_remove:
			if not i.is_root():
				i.leave()

	def get_block(self, x, y):
		return self.block_group[x+y*self.map_side[0]]

	def get_data(self, x, y):
		return self.data[x+y*self.map_side[0]]

	def set_data(self, x, y, data):
		self.data[x+y*self.map_side[0]] = data

	def get_xy(self, block):
		p = self.block_group.index(block)
		return p % self.map_side[0], p // self.map_side[0]

	def transform_to_xy(self, pos):
		if (pos[0] - self.bd) % whole < block_size[1] or (pos[1] - self.bd) % whole < block_size[1]:
			return None
		else:
			x, y = (pos[0] - self.bd) // whole, (pos[1] - self.bd) // whole
			if 0 <= x < self.map_side[0] and 0 <= y < self.map_side[1]:
				return x, y
			else:
				return None

	def create_data(self):
		#      easy: 7.5%
		#    mediun: 12.5%
		# difficult: 20%
		total_num = self.map_side[0] * self.map_side[1]
		if u.userdata['difficulty'] == 'easy':
			num = round(total_num * 0.075 / 2)
		elif u.userdata['difficulty'] == 'medium':
			num = round(total_num * 0.125 / 2)
		elif u.userdata['difficulty'] == 'difficult':
			num = round(total_num * 0.2 / 2)
		self.data = ['+']*num + ['-']*num + [None]*(total_num-2*num)
		random.shuffle(self.data)
		self.mine_num = num * 2

	def get_free_keyframe(self, keyframe, *args, **kwargs):
		for k in self.labelkeyframe_group:
			if not k.is_launched() and isinstance(k, keyframe):
				k.__init__(*args, **kwargs)
				return k
		self.labelkeyframe_group.append(keyframe(*args, **kwargs))
		return self.labelkeyframe_group[-1]

	def highlight_block(self, block_pos, flag):
		k = self.block_label_link.get(block_pos)
		if k is not None:
			k.__init__(self.get_block(*block_pos), 'bg', u.color['BLOCKBG']+style.bf2 if flag else u.color['BLOCKBG'], 8, u.curve)
		else:
			k = self.get_free_keyframe(fantas.LabelKeyFrame, self.get_block(*block_pos), 'bg', u.color['BLOCKBG']+style.bf2 if flag else u.color['BLOCKBG'], 8, u.curve)
			self.bind_bk(self.block_label_link, block_pos, k)
		k.bind_endupwith(self.unbind_bk, self.block_label_link, block_pos)
		k.launch('continue')

	def bind_bk(self, link, block_pos, keyframe):
		link[block_pos] = keyframe

	def unbind_bk(self, link, block_pos, other_operation=None, **kwargs):
		del link[block_pos]
		if other_operation:
			other_operation(**kwargs)

	def set_flag(self, pos):
		pos = self.transform_to_xy((pos[0] - self.rect.left, pos[1] - self.rect.top))
		if pos is None or pos in self.checked_pos:
			return
		music_play.play_sound('set_flag')
		if self.checked_pos:
			self.highlight_block(pos, False)
			flag = self.flag.get(pos)
			o = self.get_block(*pos)
			if flag is None:
				style.map_data['fgcolor'] = u.color['TEXTWHITE']
				flag = fantas.IconText(chr(0xe906), u.font['iconfont'], style.map_data, center=(o.rect.w/2,o.rect.h/2))
				self.flag[pos] = (flag, '+')
				flag.join(o)
				self.to_remove.append(flag)
			else:
				if flag[1] == '-':
					flag[0].leave()
					self.flag[pos] = None
				else:
					style.map_data['fgcolor'] = u.color['TEXTGRAY']
					flag[0].update_img()
					self.flag[pos] = (flag[0], '-')


	def press(self, pos):
		pos = self.transform_to_xy((pos[0] - self.rect.left, pos[1] - self.rect.top))
		if pos is None or pos in self.checked_pos:
			return
		self.highlight_block(pos, False)
		if not self.checked_pos:
			music_play.play_music(u.userdata['difficulty'])
			self.started = True
			game_time.time_ticker.launch()
			while len(u.cursor_stack) > 1:
				u.set_cursor_back()
			while self.get_data(*pos) is not None or not self.around_is_None(pos):
				random.shuffle(self.data)
			for x in range(self.map_side[0]):
				for y in range(self.map_side[1]):
					d = self.get_data(x, y)
					if isinstance(d, str):
						if d == '+':
							d = 1
						elif d == '-':
							d = -1
						for x_,y_ in around:
							x_ = x+x_
							y_ = y+y_
							if self.inside(x_, y_):
								d_ = self.get_data(x_, y_)
								if d_ is None:
									self.set_data(x_, y_, d)
								elif isinstance(d_, int):
									self.set_data(x_, y_, d_+d)
		self.reveal(pos)

	def reveal(self, pos):
		if self.started:
			sound = 'reveal'
			d = self.get_data(*pos)
			self.checked_pos.append(pos)
			o = self.get_block(*pos)
			if d is not None:
				if isinstance(d, int):
					if d < 0:
						style.map_data['fgcolor'] = u.color['BGBLACK']
					elif d > 0:
						style.map_data['fgcolor'] = u.color['TEXTWHITE']
					else:
						style.map_data['fgcolor'] = random.choice((u.color['TEXTWHITE'],u.color['BGBLACK']))
					self.to_remove.append(fantas.Text(str(d), u.font['shuhei'], style.map_data, center=o.rect.center))
					self.to_remove[-1].join(self)
					self.unchecked_blank -= 1
				else:
					if d == '+':
						style.map_data['fgcolor'] = u.color['TEXTWHITE']
						if self.unchecked_mine == '+-':
							self.unchecked_mine = '-'
						elif self.unchecked_mine == '+':
							self.unchecked_mine = ''
					else:
						if self.unchecked_mine == '+-':
							self.unchecked_mine = '+'
						elif self.unchecked_mine == '-':
							self.unchecked_mine = ''
						style.map_data['fgcolor'] = u.color['BGBLACK']
					m = fantas.IconText(chr(0xe900), u.font['iconfont'], style.map_data, center=o.rect.center)
					m.join(self)
					self.checked_mine.append((pos, m))
					sound = 'error'
			else:
				self.unchecked_blank -= 1
			if self.unchecked_blank == 0:
				self.end_game(True)
			elif self.unchecked_mine == '':
				self.end_game(False)
			else:
				music_play.play_sound(sound)
			random.shuffle(near)
			for t in near:
				t = (pos[0]+t[0], pos[1]+t[1])
				if t not in self.checked_pos and self.inside(*t):
					break
			else:
				if d is None:
					self.reveal_around(pos=pos, block=o)
				else:
					o.leave()
				return
			k = self.block_rect_link.get(pos)
			if k is not None:
				k.__init__(o.rect, 'center', self.get_block(*t).rect.center, 10, u.harmonic_curve)
			else:
				k = self.get_free_keyframe(fantas.RectKeyFrame, o, 'center', self.get_block(*t).rect.center, 10, u.harmonic_curve)
				self.bind_bk(self.block_rect_link, pos, k)
			if d is None:
				k.bind_endupwith(self.unbind_bk, self.block_rect_link, pos, other_operation=self.reveal_around, pos=pos, block=o)
			else:
				k.bind_endupwith(self.unbind_bk, self.block_rect_link, pos, other_operation=o.leave)
			k.launch('continue')

	def reveal_around(self, pos, block):
		block.leave()
		for x, y in around:
			x, y = pos[0]+x, pos[1]+y
			if self.inside(x, y) and (x, y) not in self.checked_pos:
				self.reveal((x, y))

	def inside(self, x, y):
		return 0 <= x < self.map_side[0] and 0 <= y < self.map_side[1]

	def around_is_None(self, pos):
		for x, y in around:
			if self.get_data(pos[0]+x, pos[1]+y) is not None:
				return False
		return True


class CircleChooseKeyFrame(fantas.KeyFrame):
	__slots__ = ('map_box', 'frame', 'max_r', 'r', 'st')
	gap = 2

	def __init__(self, map_box):
		self.map_box = map_box

	def tick(self):
		self.frame += 1
		r = self.frame // self.gap
		if r > self.r:
			self.r = r
			r_ = (r - 1) ** 2
			if r_ >= self.max_r:
				self.stop()
				self.map_box.mousewidget.apply_event()
				f = fantas.load('userdata')
				if f['use_cheat']:
					self.map_box.cheat.gap = f['cheat_gap']
					self.map_box.cheat.init()
					fantas.Trigger().launch(60).bind_endupwith(self.map_box.cheat.launch)
				return
			r = r ** 2
			temp = []
			for x in range(self.map_box.map_side[0]):
				dx = (x - self.map_box.map_side[0]//2 + 0.5) ** 2
				for y in range(self.map_box.map_side[1]):
					dy = (y - self.map_box.map_side[1]//2 + 0.5) ** 2
					if r_ < dx + dy <= r:
						temp.append(self.map_box.get_block(x, y))
			if temp:
				fantas.MutiLabelKeyFrame(temp, 'size', (block_size[0],block_size[0]), self.st, self.map_box.curve).launch()

	def launch(self):
		music_play.play_sound('open_map')
		super().launch()
		self.frame = self.gap
		self.r = 0
		self.max_r = (self.map_box.map_side[0]**2 + self.map_box.map_side[1]**2) / 4

class LineChooseKeyFrame(fantas.KeyFrame):
	gap = 12

	def __init__(self, map_box):
		self.map_box = map_box

	def tick(self):
		line = self.frame // self.gap
		if (self.frame-1) // self.gap != line:
			temp = []
			line_ = self.map_box.map_side[1] - line
			for x in range(self.map_box.map_side[0]):
				b = self.map_box.get_block(x, line_)
				if b.is_root():
					b.join(self.map_box)
				elif self.map_box.get_data(x, line_) is not None:
					y = line_ < self.map_box.map_side[1]/2
					xx = 3 - 3*y + (x<self.map_box.map_side[0]/2) * (2*y-1)
					i = fantas.IconText(chr(0xe900), u.font['iconfont'], style.map_data, center=b.rect.center)
					i.style = dict(i.style)
					i.style['rotation'] = 0
					i.style['fgcolor'] = u.color['TEXTWHITE' if self.map_box.get_data(x, line_)=='+' else 'TEXTGRAY']
					i.join(self.map_box)
					b_ = fantas.BezierRectKeyFrame(i, 'center', 80, fantas.BezierCurve((i.rect.center, self.map_box.rotate_point[(xx+1)%4], self.map_box.rotate_point[(xx+2)%4], self.map_box.rotate_point[4])))
					b_.launch()
					b_.bind_endupwith(i.leave)
					fantas.TextKeyFrame(i, 'rotation', 360, 80, u.curve).launch().bind_endupwith(music_play.play_sound, 'score')
					fantas.TextKeyFrame(i, 'size', 100, 80, u.curve).launch().bind_endupwith(add_size)
				if not b.is_leaf():
					b.kidgroup[0].leave()
				b.set_bg(u.color['TEXTWHITE'])
				b.rect.center = (self.map_box.bd+block_size[1]+whole*x+block_size[0]/2, self.map_box.bd+block_size[1]+whole*(self.map_box.map_side[1]-line)+block_size[0]/2)
				temp.append(b)
			fantas.MutiLabelKeyFrame(temp, 'size', (0,0), 90, u.harmonic_curve).launch()
			fantas.MutiLabelKeyFrame(temp, 'bg', u.color['BLOCKBG'], 60, u.harmonic_curve).launch()
			for x in self.map_box.to_remove[(line-1)*self.extent:line*self.extent]:
				if not isinstance(x, fantas.IconText) and isinstance(x, fantas.Text):
					self.to_remove.append(x)
					fantas.UiKeyFrame(x, 'alpha', 0, 20, u.curve).launch().bind_endupwith(x.leave)
			if line >= self.map_box.map_side[1]:
				self.stop()
				for x in self.to_remove:
					self.map_box.to_remove.remove(x)
				return
		self.frame += 1

	def init(self):
		self.frame = self.gap
		self.extent = len(self.map_box.to_remove) // self.map_box.map_side[1] + 2
		self.to_remove = []

class Cheat(fantas.KeyFrame):
	__slots__ = ('map_box', 'frame', 'gap')

	def __init__(self, map_box):
		self.map_box = map_box

	def init(self):
		self.frame = self.gap

	def tick(self):
		if (self.frame-1) // self.gap != self.frame // self.gap:
			for x in range(self.map_box.map_side[0]):
				for y in range(self.map_box.map_side[1]):
					if (x, y) not in self.map_box.checked_pos and not isinstance(self.map_box.get_data(x, y), str):
						pos = self.map_box.get_block(x, y).rect.center
						self.map_box.press((pos[0]+self.map_box.rect.left,pos[1]+self.map_box.rect.top))
						if not self.map_box.started:
							# print('end')
							self.stop()
						return
		if self.frame > 60 and not self.map_box.started:
			# print('end')
			self.stop()
		self.frame += 1


around = ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1))
near = [(0,-1),(-1,0),(1,0),(0,1)]
bounce_curve1 = fantas.FormulaCurve('(math.e/2-math.e/2*math.cos(3*math.pi*x))/math.e**x')
bounce_curve2 = fantas.FormulaCurve('(math.e/2-math.e/2*math.cos(5*math.pi*x))/math.e**x')
block_size = (24, 6)
whole = block_size[0] + block_size[1]
ensure.map_box = map_box = GameMap((10+whole*16+block_size[1], 10+whole*16+block_size[1]), bd=5, sc=u.color['TEXTWHITE'], radius={'border_radius': 12}, center=(640,400))
ensure.time_ticker = game_time.time_ticker

def place_element(father):
	map_box.join(father)
