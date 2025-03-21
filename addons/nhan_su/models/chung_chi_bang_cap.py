from odoo import models, fields, api


class DChungChiBangCap(models.Model):
    _name = 'chung_chi_bang_cap'
    _description = 'Bảng chưa thông tin chứng chỉ bằng cấp'
    _rec_name = 'ten_chung_chi'
    ten_chung_chi = fields.Char("Tên chứng chỉ", required=True)
    loai_chung_chi = fields.Char("Loại chứng chỉ", required=True)
    muc_do = fields.Char("Mức độ chứng chỉ", required=True)
    noi_cap = fields.Char("Nơi cấp chứng chỉ", required=True)
    ma_chung_chi = fields.Char("Mã chứng chỉ", required=True)
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên")