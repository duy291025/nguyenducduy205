from odoo import models, fields

class ChatMessage(models.Model):
    _name = 'qlda.chat.message'
    _description = 'Chat AI Message'
    _order = 'create_date asc'

    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user
    )

    role = fields.Selection([
        ('user', 'User'),
        ('ai', 'AI')
    ], required=True)

    content = fields.Text(string='Nội dung', required=True)
