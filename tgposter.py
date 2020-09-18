from os import listdir, chdir, remove, getcwd
from datetime import datetime
from subprocess import Popen
import argparse
import telebot

def autoposter(token, chat_id, dir):

	try:
		print("%s Checking token." % (datetime.now().strftime("[%H:%M:%S]")))
		bot = telebot.TeleBot(token)
		bot.get_me()
		chdir(dir)
	except telebot.apihelper.ApiTelegramException as error:
		print("%s Fatal error: '%s'" % (datetime.now().strftime("[%H:%M:%S]"), error))
		return 0
	try:
		print("%s Scanning directory..." % (datetime.now().strftime("[%H:%M:%S]")))
		while 1:
			if listdir():
				for file in listdir():
					if file[-4:] == ".png" or file[-4:] == ".jpg":
						try:
							photo = open(file, "rb")
							bot.send_photo(chat_id, photo)
							photo.close()
							remove(file)
							print("%s '%s' successfully uploaded." % (datetime.now().strftime("[%H:%M:%S]"), file))
						except FileNotFoundError:
							pass
						except telebot.apihelper.ApiTelegramException as error:
							if "PHOTO_INVALID_DIMENSIONS" in str(error):
								print("%s '%s' photo too large, uploading as document." % (datetime.now().strftime("[%H:%M:%S]"), file))
								doc = open(file, "rb")
								bot.send_document(chat_id, doc)
								photo.close()
								doc.close()
								remove(file)
								print("%s '%s' successfully uploaded." % (datetime.now().strftime("[%H:%M:%S]"), file))
						except Exception as e:
							print("%s Error while uploading '%s' - '%s'" % (datetime.now().strftime("[%H:%M:%S]"), file, e))	
					elif file[-4:] == ".gif":						
						try:						
							doc = open(file, "rb")
							bot.send_document(chat_id, doc)
							doc.close()
							remove(file)
							print("%s '%s' successfully uploaded." % (datetime.now().strftime("[%H:%M:%S]"), file))						
						except FileNotFoundError:
							pass
						except Exception as e:						
							print("%s Error while uploading '%s' - '%s'" % (datetime.now().strftime("[%H:%M:%S]"), file, e))
					elif file[-4:] == ".mp4":
						try:
							video = open(file, "rb")
							print("%s Uploading '%s'..." % (datetime.now().strftime("[%H:%M:%S]"), file))
							bot.send_video(chat_id, video)
							video.close()
							remove(file)
							print("%s Successfully uploaded." % (datetime.now().strftime("[%H:%M:%S]")))					
						except FileNotFoundError:
							pass
						except Exception as e:
							print("%s Error while uploading - '%s'" % (datetime.now().strftime("[%H:%M:%S]"), e))
					elif file[-5:] == ".webm":
						try:
							print("%s Converting '%s' to mp4..." % (datetime.now().strftime("[%H:%M:%S]"), file))
							ffmpeg = Popen(["ffmpeg.exe", "-i", file, file[0:-5]+".mp4", "-loglevel", "quiet"])
							ffmpeg.wait()
							remove(file)
							print("%s Uploading '%s'..." % (datetime.now().strftime("[%H:%M:%S]"), file[0:-5]+".mp4"))
							video = open(file[0:-5]+".mp4", "rb")
							bot.send_video(chat_id, video)
							video.close()
							remove(file[0:-5]+".mp4")
							print("%s Successfully uploaded." % (datetime.now().strftime("[%H:%M:%S]")))										
						except FileNotFoundError:
							pass						
						except Exception as e:
							print("%s Error while uploading - '%s'" % (datetime.now().strftime("[%H:%M:%S]"), e))
	except KeyboardInterrupt:
		return 0

def main():

	print("%s Starting..." % (datetime.now().strftime("[%H:%M:%S]")))
	parser = argparse.ArgumentParser(description='Telegram Autoposter Bot.')
	parser.add_argument('-D', '--dir', type=str, default=getcwd(), help = "Directory.")
	parser.add_argument('-T', '--token', type=str, required=True, help = "Token.")
	parser.add_argument('-C', '--chat', type=str, required=True, help = "Chat ID.")
	args = parser.parse_args()
	autoposter(args.token, args.chat, args.dir)

main()