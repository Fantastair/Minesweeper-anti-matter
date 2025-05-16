import fantas
from fantas import uimanager as u
import style

import main_page
import element.music_play as music_play

bg = fantas.Root(u.color['BGDARKGRAY'])
icon = fantas.Ui(u.image['icon'], center=(640, 440))
icon.join(bg)
icon.size = (260,260)
icon.apply_size()
icon.alpha = 0
icon.size = (130, 130)

gamename_text1 = fantas.Text('扫', u.font['shuhei'], style.gamename_text, center=(640, 480))
gamename_text1.join(bg)
gamename_text1.alpha = 0
gamename_text2 = fantas.Text('雷', u.font['shuhei'], style.gamename_text, center=(640, 540))
gamename_text2.join(bg)
gamename_text2.alpha = 0
gameversion_text = fantas.Text('反物质版', u.font['shuhei'], style.gameversion_text, center=(640, 510))
gameversion_text.join(bg)
gameversion_text.alpha = 0
author_text = fantas.Text('BY    FANTASTAIR', u.font['deltha'], style.author_text, center=(680, 540))
author_text.join(bg)
author_text.alpha = 0

black_cover = fantas.Label(u.size, bg=u.color['BGBLACK'])
black_cover.join(bg)
black_cover.alpha = 0
if not u.userdata['skip_startani']:
	fantas.Text('都什么年代了！  还在玩传统扫雷？', u.font['douyu'], style.gamename_text, center=black_cover.rect.center).join(black_cover)
	style.gamename_text['size'] = 30
	fantas.Text('内含音乐与音效，请确保周围环境适合播放！', u.font['shuhei'], style.gamename_text, midtop=black_cover.kidgroup[0].rect.midbottom).join(black_cover)

start_game_curve = fantas.FormulaCurve('34/9*x**3-77/9*x**2+52/9*x')
icon_alpha_in = fantas.UiKeyFrame(icon, 'alpha', 255, 60, u.curve)
icon_move_up = fantas.RectKeyFrame(icon, 'centery', 280, 60, start_game_curve)
icon_big = fantas.UiKeyFrame(icon, 'size', (260,260), 60, u.harmonic_curve)
sao_alpha_in = fantas.UiKeyFrame(gamename_text1, 'alpha', 255, 25, u.curve)
sao_move_left = fantas.RectKeyFrame(gamename_text1, 'centerx', 460, 25, u.harmonic_curve)
lei_alpha_in = fantas.UiKeyFrame(gamename_text2, 'alpha', 255, 25, u.curve)
lei_move_left = fantas.RectKeyFrame(gamename_text2, 'centerx', 460, 25, u.harmonic_curve)
gv_alpha_in = fantas.UiKeyFrame(gameversion_text, 'alpha', 255, 40, u.curve)
lei_alpha_in.bind_endupwith(gv_alpha_in.launch)
gv_move_right = fantas.RectKeyFrame(gameversion_text, 'centerx', 680, 40, u.harmonic_curve)
lei_move_left.bind_endupwith(gv_move_right.launch)
gv_move_up = fantas.RectKeyFrame(gameversion_text, 'top', 435, 40, u.harmonic_curve)
at_alpha_in = fantas.UiKeyFrame(author_text, 'alpha', 255, 40, u.curve)
at_move_down = fantas.RectKeyFrame(author_text, 'bottom', 570, 40, u.harmonic_curve)
bc_alpha_in = fantas.UiKeyFrame(black_cover, 'alpha', 255, 90, u.curve)
bc_alpha_out = fantas.UiKeyFrame(black_cover, 'alpha', 0, 30, u.curve)
bc_alpha_out.bind_endupwith(black_cover.leave)

def show_text():
	sao_alpha_in.launch()
	sao_move_left.launch()
	lei_alpha_in.launch()
	lei_move_left.launch()
icon_move_up.bind_endupwith(show_text)

def show_author():
	gv_move_up.launch()
	at_alpha_in.launch()
	at_move_down.launch()
	delay.bind_endupwith(bc_alpha_in.launch)
gv_move_right.bind_endupwith(show_author)

def icon_act():
	icon_alpha_in.launch()
	icon_move_up.launch()
	icon_big.launch()

def start_game():
	u.root = main_page.bg
	u.set_cursor_back()
	main_page.black_cover = black_cover
	black_cover.leave()
	black_cover.join(main_page.bg)
	bao_delay = fantas.Trigger()
	bao_delay.bind_endupwith(bc_alpha_out.launch)
	bao_delay.launch(time=60)
	main_page.wb_wander.launch()
	music_play.play_music('background')

delay = fantas.Trigger()
delay.bind_endupwith(icon_act)
at_move_down.bind_endupwith(delay.launch, time=60)
bc_alpha_in.bind_endupwith(start_game)

def main():
	u.root = bg
	u.set_cursor('o')
	delay.launch(time=30)

def fast_main():
	u.root = main_page.bg
	main_page.black_cover = black_cover
	u.set_cursor_back()
	black_cover.alpha = 255
	black_cover.leave()
	black_cover.join(main_page.bg)
	bc_alpha_out.launch()
	main_page.wb_wander.launch()
	music_play.play_music('background')
	# main_page.settings.pull_button.展开or收起()
	# main_page.start_game()

