from dotenv import load_dotenv
load_dotenv()

import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread, Lock
import time
import emojis
import grapheme
import random

# Idk what this does precisely, but the telegram bot recommended it /shrug
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def telegram_bot():
	"""
	Telegram bot thread. Does the telegram bot business and uses
	SSEFuckery.sse_broadcast to send the taunts to the web clients.
	"""

	def error(update, context):
		update.message.reply_text('an error occured')

	def text(update, context):
		text_received = update.message.text

		# Hack to check if all graphemes are emojis
		if emojis.count(text_received) == len(list(grapheme.graphemes(text_received))):
			print("emojis:", text_received)
			update.message.reply_text(f'uwu {text_received}')
			SSEFuckery.sse_broadcast("emojis", text_received)
			return

		print("scrolly-text:", text_received)
		update.message.reply_text(f'auzi cica >{text_received}')
		SSEFuckery.sse_broadcast("scrolly-text", text_received)

	def doaflip(update, context):
		print("doaflip")
		SSEFuckery.sse_broadcast("doaflip")
		update.message.reply_animation(random.choice([
			"https://i.imgur.com/DHMMKyf.mp4",
			"https://i.imgur.com/pjpN4Gr.mp4",
			"https://i.imgur.com/x9CL5z7.mp4",
			"https://i.imgur.com/k7IRDVF.mp4",
			"https://i.imgur.com/h9DVD3G.mp4",
			"https://i.imgur.com/0O1hyWx.mp4",
			"https://media.giphy.com/media/3o85xnYxeojLcZ7GNy/giphy.gif",
			"https://media.giphy.com/media/l3fQwP0Fv7ek6uPWU/giphy.gif",
			"https://media.giphy.com/media/mKMGLhoD8L4yc/giphy.gif",
			"https://media.giphy.com/media/M3gmDwPbAWkbS/giphy.gif",
			"https://media.giphy.com/media/xTcnSMYx90VnYZti0g/giphy.gif",
			"https://media.giphy.com/media/10uzUfr4cGYxIk/giphy.gif",
			"https://media.giphy.com/media/2QixVlIqaFtVC/giphy.gif",
			"https://media.giphy.com/media/3o7Zez01HKXvaLXiHS/giphy.gif",
			"https://media.giphy.com/media/LOhwoZFUQwfMhww0rx/giphy.gif",
			"https://media.giphy.com/media/wwfCmkKuKzAAM/giphy.gif",
			"https://media.giphy.com/media/jOQ91yKFFdSgu7HZqh/giphy.gif",
			"https://media.giphy.com/media/ihjeVd9YRjoTGFXtN9/giphy.gif",
			"https://media.giphy.com/media/o2oe2HMZKZUpW/giphy.gif",
			"https://media.giphy.com/media/Z9J8SJgYrFR8JQrl8S/giphy.gif",
			"https://media.giphy.com/media/12S8pukaOwZApa/giphy.gif"
		]))

	updater = Updater(os.getenv("TELEGRAM_TOKEN"), use_context=True)
	dispatcher = updater.dispatcher
	dispatcher.add_handler(CommandHandler("doaflip", doaflip))
	dispatcher.add_handler(MessageHandler(Filters.text, text))
	dispatcher.add_error_handler(error)
	updater.start_polling()


class SSEFuckery(SimpleHTTPRequestHandler):
	"""
	This class describes a sse fuckery.
	"""
	all_wfiles = set()
	all_wfiles_lock = Lock()

	@staticmethod
	def sse_broadcast(event, data=""):
		"""
		Broadcasts an SSE event to all current connections.
		
		:param      event:  Event type
		:param      data:   Associated event data
		"""
		payload = f"event: {event}\ndata: {data}\n\n".encode()
		with SSEFuckery.all_wfiles_lock:
			for wfile in SSEFuckery.all_wfiles:
				try:
					wfile.write(payload)
				except BrokenPipeError:
					pass

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs, directory="static")

	def do_GET(self):
		"""
		Handles the /sse path specially, or just hands off control to the normal
		static websever.
		"""
		if self.path == "/sse":
			self.send_response(200)
			self.send_header("Content-Type", "text/event-stream")
			self.end_headers()

			with SSEFuckery.all_wfiles_lock:
				SSEFuckery.all_wfiles.add(self.wfile)

			try:
				while True:
					self.wfile.write(b"event: ping\ndata: ping\n\n")
					time.sleep(1)
			except BrokenPipeError:
				pass

			with SSEFuckery.all_wfiles_lock:
				SSEFuckery.all_wfiles.remove(self.wfile)
		else:
			return super().do_GET()

if __name__ == '__main__':
	print("Starting telegram thread")
	Thread(target = telegram_bot).start()
	PORT = 45149
	print(f"Starting web thread. Connect to http://localhost:{PORT}/")
	ThreadingHTTPServer(("", PORT), SSEFuckery).serve_forever()
