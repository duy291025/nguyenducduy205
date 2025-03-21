from odoo import models, fields, api


class TaiNguyen(models.Model):
    _name = 'du_an_tai_nguyen'
    _description = 'Tài Nguyên Dự Án'
    
    name = fields.Char(string='Tên Tài Nguyên', required=True)
    project_id = fields.Many2one('du_an_quan_ly', string='Dự Án')
    type = fields.Selection([
        ('human', 'Nhân Lực'),
        ('equipment', 'Thiết Bị'),
        ('budget', 'Ngân Sách')
    ], string='Loại', required=True)
    quantity = fields.Integer(string='Số Lượng')
