from odoo import models, fields

class DuAnNhanSu(models.Model):
    _name = 'du_an_quan_ly_nhan_su'
    _description = 'Nhân Sự Thực Hiện Dự Án'

    project_id = fields.Many2one('du_an_quan_ly', string='Dự án', required=True, ondelete='cascade')
    ten_nhan_su = fields.Many2one('res.users', string='Tên nhân sự')
    role = fields.Selection([
        ('manager', 'Quản Lý'),
        ('member', 'Thành Viên'),
    ], string='Vai Trò', default='member')
