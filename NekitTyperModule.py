from telethon.tl.functions.messages import EditMessageRequest
from .. import loader, utils 
from time import sleep
@loader.tds
class NekitMod(loader.Module):
	"""Модуль со стилями тайпинга"""
	strings = {'name': 'NekitTyperMod'}          
	async def client_ready(self, client, db):
		self.db = db
		self.client = client     
	async def tickercmd(self, message):
		"""Текст с бегущей строкой""" 
		args = utils.get_args_raw(message) 
		a = args
		text = args
		fsm = 0
		lsm = 28
		while(a!=""):
			a = text[fsm:lsm]
			await message.edit("—————————————————\n"+a+"\n—————————————————")
			lsm+=1
			fsm+=1
			sleep(0.2)
        
