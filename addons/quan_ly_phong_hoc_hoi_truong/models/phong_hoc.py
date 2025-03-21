from odoo import models, fields, api


class Room(models.Model):
    _name = 'phong_hoc'
    _description = 'Phòng học/Hội trường'

    name = fields.Char(string='Tên phòng', required=True)
    capacity = fields.Integer(string='Sức chứa')
    equipment_ids = fields.One2many('thiet_bi_trong_phong', 'room_id', string='Thiết bị')
    booking_ids = fields.One2many('dat_phong', 'room_id', string='Lịch đặt phòng')