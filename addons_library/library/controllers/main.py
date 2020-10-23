from odoo import http

class Books(http.Controller):
	
	@http.route('/library/book', auth='user')
	
	def list(self, **kwargs):
		Book = http.request.env['li.book']
		books = Book.search([])
		return http.request.render(
			'library.book_list_template', {'books': books})