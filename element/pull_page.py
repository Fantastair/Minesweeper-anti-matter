import fantas
from fantas import uimanager
u = uimanager
import style

import element.music_play as music_play

class PullButton(fantas.SmoothColorButton):
	__slots__ = ['fold', 'arrow', 'arrow_jump', 'arrow_color', 'arrow_rotate', 'move', 'page', 'move_page', 'park', 'fold_tip', 'unfold_tip']

	def __init__(self, park, page_size, *args, **kwargs):
		super().__init__(*args, mousewidget=PullButtonWidget, **kwargs)
		self.fold = True
		self.park = (-1) ** (park == 'right')
		s = dict(style.arrow_icontext)
		if park == 'right':
			s['rotation'] = 180
			self.page = fantas.Label(page_size, bd=5, bg=u.color['TIPGRAY'], sc=style.pull_button['hover_sc'], radius={'border_top_left_radius': 32,'border_bottom_left_radius': 32}, midleft=self.rect.midright)
		else:
			s['rotation'] = 0
			self.page = fantas.Label(page_size, bd=5, bg=u.color['TIPGRAY'], sc=style.pull_button['hover_sc'], radius={'border_top_right_radius': 32,'border_bottom_right_radius': 32}, midright=self.rect.midleft)
		self.arrow = fantas.Text(chr(0xe905), u.font['iconfont'], s, center=(self.rect.width/2, self.rect.height/2))
		self.arrow.join(self)
		self.bind(self.展开or收起)
		self.arrow_jump = fantas.RectKeyFrame(self.arrow, 'centerx', 5*self.park, 15, u.parabola1, absolute=False)
		self.arrow_color = fantas.TextKeyFrame(self.arrow, 'fgcolor', u.color['BUTTONBDBLUE'], 8, u.curve)
		self.arrow_rotate = fantas.TextKeyFrame(self.arrow, 'rotation', 0 if self.park == -1 else 180, 15, u.harmonic_curve)
		self.move = fantas.RectKeyFrame(self, 'centerx', (self.page.rect.width-self.page.bd)*self.park, 40, u.harmonic_curve, absolute=False)
		self.move_page = fantas.RectKeyFrame(self.page, 'centerx', self.page.rect.width*self.park, 20, u.harmonic_curve, absolute=False)

	def 展开or收起(self):
		if not self.move.is_launched():
			music_play.play_sound('pull_page')
			self.fold = not self.fold
			self.arrow_rotate.launch('continue')
			self.move_page.launch()
			self.move.launch()
			if self.fold:
				self.move_page.bind_endupwith(self.page.leave)
				self.arrow_jump.value = 5 * self.park
				self.arrow_rotate.value = 0 if self.park == -1 else 180
				self.move.value = self.move_page.value = self.page.rect.width * self.park
				self.move.value -= self.page.bd * self.park
				if u.show_messages:
					self.fold_tip.cancel_event()
					self.unfold_tip.apply_event()
				self.mousewidget.mouseon = False
				self.mousewidget.mouseout()
			else:
				self.page.join(self.father)
				self.move_page.bind_endupwith(None)
				self.arrow_jump.value = -5 * self.park
				self.arrow_rotate.value = 180 if self.park == -1 else 0
				self.move.value = self.move_page.value = -self.page.rect.width * self.park
				self.move.value += self.page.bd * self.park
				if u.show_messages:
					self.unfold_tip.cancel_event()
					self.fold_tip.apply_event()

class PullButtonWidget(fantas.ColorButtonMouseWidget):
	def mousein(self):
		if self.ui.fold:
			self.ui.arrow_color.value = u.color['BUTTONBDBLUE']
			self.ui.arrow_color.launch('continue')
		super().mousein()
		self.ui.arrow_jump.launch('nothing')

	def mouseout(self):
		if self.ui.fold:
			super().mouseout()
			self.ui.arrow_color.value = u.color['TEXTWHITE']
			self.ui.arrow_color.launch('continue')
		else:
			u.set_cursor_back()
			self.ui.set_state('hover')


