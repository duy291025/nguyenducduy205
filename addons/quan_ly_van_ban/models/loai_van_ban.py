from odoo import models, fields, api


class VanBanDen(models.Model):
    _name = 'van_ban_den'
    _description = 'Bảng chứa thông tin văn bản'

    so_hieu_van_ban = fields.Char("Số hiệu", required=True)
    ten_van_ban = fields.Char("Tên văn bản")
    so_van_ban_den = fields.Char("Số văn bản đến")
    nam = fields.Integer("Năm")
    noi_gui_den = fields.Char("Nơi gửi đến")
    muc_do = fields.Selection([
        ('hoa_toc', 'Hoả tốc'),
        ('thuong_khan', 'Thượng khẩn'),
        ('khan', 'Khẩn'),
    ], string="Mức độ", default='thuong', required=True)