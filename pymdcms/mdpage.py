from markdown import markdown
from page import Page

class MDPage(Page):
	def from_file(self, fn):
		try:
			with open(fn) as fp:
				rollback=0;

				while True:
					rollback=fp.tell()
					line=fp.readline().strip()

					if not line:
						break

					try:
						key, value=(x.strip() for x in line.split(':', 1))
						self[key.lower()]=value
					except ValueError:
						break

				fp.seek(rollback)

				self['content']=MDPage.decode(fp.read())
		except IOError as e:
			self['content'] = str(e)

		return self
	
	@staticmethod
	def decode(text):
		return markdown(text, extensions=['markdown.extensions.extra'])
