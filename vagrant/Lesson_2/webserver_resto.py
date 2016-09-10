from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<a href='/restaurants/new'>Add new restaurant</a><br><br>"

				query = session.query(Restaurant).all()
				for q in query:
					output += "%s <br>" % q.name
					output += "<a href='/restaurants/%s/edit'>Edit</a><br>" % q.id
					output += "<a href='/restaurants/%s/delete'>Delete</a><br>" % q.id
					output += "<br><br>"

				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			elif self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Add new restaurant</h1>"

				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<input name='name' type='text'>"
				output += "<input type='submit' value='Create'></form>"
				
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			elif self.path.endswith("/edit"):
				id_num = self.path.split("/")[2]
				query = session.query(Restaurant.name).filter(Restaurant.id==id_num).one()
				print "edit restaurant name: ", query[0]
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>%s</h1>" % query[0]
				output += "<h3>Edit restaurant name</h3>"

				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % id_num
				output += "<input name='name' type='text' placeholder='%s'>" % query[0]
				output += "<input type='submit' value='Edit'></form>"
				
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			elif self.path.endswith("/delete"):
				id_num = self.path.split("/")[2]
				query = session.query(Restaurant.name).filter(Restaurant.id==id_num).one()
				print "delete restaurant name: ", query[0]
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>%s</h1>" % query[0]
				output += "<h3>Delete restaurant?</h3>"

				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % id_num
				output += "<input name='submitted' type='submit' value='cancel'>"
				output += "<input name='submitted' type='submit' value='OK'>"
				output += "</form>"
				
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

		except IOError:
			self.send_error(404, 'File Not Found %s' % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('name')
				
					myNewRestaurant = Restaurant(name = messagecontent[0])
					session.add(myNewRestaurant)
					session.commit()
					print "Created restaurant: ", messagecontent[0]

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location','/restaurants')
					self.end_headers()

			elif self.path.endswith("/edit"):
				id_num = self.path.split("/")[2]
				ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('name')
				
					myUpdatedRestaurant = session.query(Restaurant).filter_by(id=id_num).one()
					if myUpdatedRestaurant:

						myUpdatedRestaurant.name = messagecontent[0]
						session.add(myUpdatedRestaurant)
						session.commit()
						print "Edited restaurant: ", messagecontent[0]
						print "Restaurant id: ", id_num
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location','/restaurants')
					self.end_headers()

			elif self.path.endswith("/delete"):
				id_num = self.path.split("/")[2]
				ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('submitted')
					if messagecontent[0] == 'OK':
						myDeletedRestaurant = session.query(Restaurant).filter_by(id=id_num).one()
						if myDeletedRestaurant:
						
							session.delete(myDeletedRestaurant)
							session.commit()
							print "Deleted restaurant: ", messagecontent[0]
						
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location','/restaurants')
					self.end_headers()		
				
		except:
			pass

def main():

	try:
		port =8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()


if __name__ == '__main__':

	

	main()

