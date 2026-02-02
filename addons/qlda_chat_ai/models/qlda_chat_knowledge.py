from odoo import models, fields

class QLDAChatKnowledge(models.Model):
    _name = 'qlda.chat.knowledge'
    _description = 'AI Knowledge Base'

    name = fields.Char(string='Tiêu đề', required=True)
    content = fields.Text(string='Nội dung kiến thức', required=True)
