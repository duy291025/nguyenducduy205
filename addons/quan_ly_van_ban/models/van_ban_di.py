from odoo import models, fields, api


class VanBanDen(models.Model):
    _name = 'van_ban_di'
    _description = 'Bảng chứa thông tin văn bản'

    so_hieu_van_ban = fields.Char("Số hiệu", required=True)
    ten_van_ban = fields.Char("Tên văn bản")
    so_van_ban_di = fields.Char("Số văn bản đi")
    nam = fields.Integer("Năm")
    noi_den = fields.Char("Nơi đến")
