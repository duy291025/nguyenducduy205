from odoo import models, fields


class QLDAChatMemory(models.Model):
    _name = 'qlda.chat.memory'
    _description = 'Chat AI Memory'

    user_id = fields.Many2one('res.users', required=True)
    last_tool = fields.Char()
    last_project = fields.Char()
