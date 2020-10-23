# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import Warning

class Book(models.Model):
	_name = 'li.book'
	_description = 'Book'
	_order = 'name, date_published desc'
	
	name = fields.Char('Title', required=True)
	isbn = fields.Char('ISBN')

	#nuevo codigo de texto del capitulo 6 
	book_type = fields.Selection(
		[('paper','Paperback'),
		('hard','Hardcover'),
		('electronic','Electronic'),
		('other', 'Other')],
		'Type')

	notes = fields.Text('Internal Notes')
	descr = fields.Html('Description')


	# Numeric fields:
	copies = fields.Integer(default=1)
	avg_rating = fields.Float('Average Rating', (3, 2))
	price = fields.Monetary('Price', 'currency_id')
	currency_id = fields.Many2one('res.currency') 
	#fin de variables numericas del capitulo 6

	# price helper
	active = fields.Boolean('Active?', default=True)
	date_published = fields.Date()
	image = fields.Binary('Cover')
	publisher_id = fields.Many2one('res.partner', string='Publisher')
	author_ids = fields.Many2many('res.partner', string='Authors')

	def _check_isbn(self):

		self.ensure_one()
		digits = [int(x) for x in self.isbn if x.isdigit()] # esto verifica si son numeros 
		print(digits)
		if len(digits) == 13: # calcula el rango de el isbm
			ponderations = [1, 3] * 6 # crea una tupla de 12 digitos
			terms = [a *  b for a, b in zip(digits[:12], ponderations)] # une las tablas de el codigo las de [1,3]
			remain = sum(terms) % 10
			check = 10 - remain if remain != 0 else 0
			return digits[-1] == check

	@api.multi		
	def button_check_isbn(self):
		for book in self:
			if not book.isbn:
				raise Warning('Please provide an ISBN for %s' % book.name)
			if book.isbn and not book._check_isbn():
				raise Warning('%s is an invalid ISBN' % book.isbn)
		return True


		