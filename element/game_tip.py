import fantas
from fantas import uimanager
u = uimanager
import style

from element.pull_page import PullButton


pull_button = PullButton('right', (310,360), (40,120), style.pull_button, bd=2, radius={'border_top_left_radius': 16,'border_bottom_left_radius': 16}, midright=(1280,380))
fantas.Text('游戏介绍', u.font['shuhei'], style.introduce_title, center=(155,40)).join(pull_button.page)
fantas.Label((240,6), bg=u.color['TEXTWHITE'], radius={'border_radius': 2}, center=(155, 80)).join(pull_button.page)
fantas.Text('与传统扫雷最大的区别', u.font['shuhei'], style.introduce_text, midtop=(155,100)).join(pull_button.page)
fantas.Text('是同时存在正物质雷和', u.font['shuhei'], style.introduce_text, midtop=(155,128)).join(pull_button.page)
fantas.Text('反物质雷，分别使周围', u.font['shuhei'], style.introduce_text, midtop=(155,156)).join(pull_button.page)
fantas.Text('的数字+1或-1，也就是', u.font['shuhei'], style.introduce_text, midtop=(155,184)).join(pull_button.page)
fantas.Text('说，你会遇见0和负数，', u.font['shuhei'], style.introduce_text, midtop=(155,212)).join(pull_button.page)
fantas.Text('数字 1 周围也不一定只', u.font['shuhei'], style.introduce_text, midtop=(155,240)).join(pull_button.page)
fantas.Text('有 1颗雷。请小心探索！', u.font['shuhei'], style.introduce_text, midtop=(155,266)).join(pull_button.page)
style.introduce_text['fgcolor'] = u.color['TEXTGRAY']
fantas.Text('正物质雷', u.font['shuhei'], style.introduce_text, center=(203,142)).join(pull_button.page)
fantas.Text('+1', u.font['shuhei'], style.introduce_text, center=(119,198)).join(pull_button.page)
style.introduce_text['fgcolor'] = u.color['QUITRED']
fantas.Text('反物质雷', u.font['shuhei'], style.introduce_text, center=(83,170)).join(pull_button.page)
fantas.Text('-1', u.font['shuhei'], style.introduce_text, center=(166,198)).join(pull_button.page)
style.introduce_text['fgcolor'] = u.color['TEXTWHITE']

author_web = fantas.WebURL('瞧瞧我的其他作品呗！  (密码：fan)', 'https://fantastair.lanzout.com/b03qx3uyf', u.font['douyu'], style.recommand_text, center=(155,340))
author_web.join(pull_button.page)
if u.show_messages:
	fantas.HoverMessage(author_web, '蓝奏云网盘链接，密码：fan', u.hovermessagebox).apply_event()
	pull_button.unfold_tip = fantas.HoverMessage(pull_button, '展开游戏介绍', u.hovermessagebox)
	pull_button.unfold_tip.apply_event()
	pull_button.fold_tip = fantas.HoverMessage(pull_button, '收起游戏介绍', u.hovermessagebox)

def place_element(father):
	pull_button.join(father)
