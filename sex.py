from dotenv import load_dotenv
load_dotenv()

import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread, Lock
import time
import emojis
import grapheme

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

	updater = Updater(os.getenv("TELEGRAM_TOKEN"), use_context=True)
	dispatcher = updater.dispatcher
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
	def sse_broadcast(event, data):
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
