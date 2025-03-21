from odoo import models, fields

class PhongHop(models.Model):
    _name = 'phong_hop'
    _description = 'Phòng họp/Hội trường'

    name = fields.Char(string='Tên phòng', required=True)
    capacity = fields.Integer(string='Sức chứa')
    equipment = fields.Text(string='Thiết bị có sẵn')
    booking_ids = fields.One2many('dang_ky_muon_phong', 'room_id', string='Lịch mượn phòng')
    history_ids = fields.One2many('lich_su_muon_phong', 'room_id', string='Lịch sử mượn phòng')
