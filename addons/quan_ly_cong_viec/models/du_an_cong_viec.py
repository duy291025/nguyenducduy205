from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class CongViec(models.Model):
    _name = 'du_an_cong_viec'
    _description = 'Công Việc Dự Án'
    
    name = fields.Char(string='Tên Công Việc', required=True)
    project_id = fields.Many2one('du_an_quan_ly', string='Dự Án')
    assigned_to = fields.Many2one('res.users', string='Người Được Giao')
    deadline = fields.Date(string='Hạn Chót')
    priority = fields.Selection([
        ('low', 'Thấp'),
        ('medium', 'Trung Bình'),
        ('high', 'Cao')
    ], string='Mức Độ Ưu Tiên', default='medium')
    status = fields.Selection([
        ('to_do', 'Chưa Bắt Đầu'),
        ('in_progress', 'Đang Thực Hiện'),
        ('done', 'Hoàn Thành')
    ], string='Trạng Thái', default='to_do')
    tag_ids = fields.Many2many('du_an_cong_viec.tag', string='Thẻ')
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'du_an_cong_viec')], string='Tệp Đính Kèm')
