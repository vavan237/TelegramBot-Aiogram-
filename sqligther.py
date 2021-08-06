import sqlite3

class Sqligther():

	def __init__(self, database_file):
		#подключаем базу
		self.connection = sqlite3.connect('db.db')
		self.cursor = self.connection.cursor()


	def get_subscriptions(self, status = True):
		#получаем всех активных подписчиков
		with self.connection:
			#print (self.cursor.execute("SELECT * FROM subscribers WHERE status = ? ",(status,)).fetchall())
			return self.cursor.execute("SELECT * FROM subscribers WHERE status = ?",(status,)).fetchall()

	def subscriber_exists(self, user_id):
		#проверяем есть ли уже юзер в базе
		with self.connection:
			result = self.cursor.execute("SELECT * FROM subscribers WHERE user_id = ?",(user_id,)).fetchall()
			#print (bool(len(result)))
			return bool(len(result))
			
				

	def add_subscriber(self, user_id, status = True):
		with self.connection:
			return self.cursor.execute("INSERT INTO subscribers (user_id, status) VALUES (?,?)",(user_id, status,))

	#обновляем status		
	def update_subscriptions (self, user_id, status):
		with self.connection:
			return self.cursor.execute(" UPDATE subscribers SET status = ? WHERE user_id = ?",(status, user_id,))
			

	def close (self):
		#закрываем соединение
		self.connection.close()

	