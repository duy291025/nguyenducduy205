from odoo import models, fields, api


class RuiRo(models.Model):
    _name = 'du_an_rui_ro'
    _description = 'Rủi Ro Dự Án'
    
    name = fields.Char(string='Tên Rủi Ro', required=True)
    project_id = fields.Many2one('du_an_quan_ly', string='Dự Án')
    impact = fields.Selection([
        ('low', 'Thấp'),
        ('medium', 'Trung Bình'),
        ('high', 'Cao')
    ], string='Mức Độ Ảnh Hưởng', required=True)
    mitigation_plan = fields.Text(string='Kế Hoạch Giảm Thiểu')