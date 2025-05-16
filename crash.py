import sys

if len(sys.argv) == 1:
	input('未捕获到异常，输入任意内容结束异常处理程序。。。')
	sys.exit()
else:
	print('你遇到了一个BUG！')
	message = sys.argv[1]
	print(f'...[ {message.split('\n')[-2]} ]...')
	if input('输入y确认发送报错信息，输入其他任意内容退出：') == 'y':
		try:
			import os
			import deta
			import time
			os.environ['DETA_PROJECT_KEY'] = 'c0s5rmynt5a_S8QgPj2cgftLoy63dp79k2rW7x3ngsFm'
			d = deta.Deta()
			drive = d.Drive('Data')
			print('发送中...')
			drive.put(name=f'crash_report/{time.asctime()}.txt', data=message.encode('utf-8'))
		except:
			import traceback
			with open('_internal/hsarc.txt', 'a+') as f:
				print('==========', time.asctime(), '==========\n', message, '\n', traceback.format_exc(), file=f)
			print('发送失败！请手动联系作者！(QQ:2364209908)')
		else:
			print('发送成功！感谢你对本游戏的支持！')
	else:
		print('为了游戏BUG修复，你应该尽快告知作者！')
	input('输入任意内容结束异常处理程序。。。')
