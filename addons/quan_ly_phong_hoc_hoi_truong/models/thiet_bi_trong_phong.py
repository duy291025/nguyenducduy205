from odoo import models, fields, api


class RoomEquipment(models.Model):
    _name = 'thiet_bi_trong_phong'
    _description = 'Thiết bị trong phòng'

    name = fields.Char(string='Tên thiết bị', required=True)
    room_id = fields.Many2one('phong_hoc', string='Phòng')
    status = fields.Selection([
        ('available', 'Hoạt động'),
        ('in_stock', 'Tồn kho'),
        ('broken', 'Hỏng')
    ], string='Tình trạng', default='available')
    maintenance_ids = fields.One2many('lich_su_sua_chua', 'equipment_id', string='Lịch sử sửa chữa')