from odoo import models, fields, api

class EquipmentMaintenance(models.Model):
    _name = 'lich_su_sua_chua'
    _description = 'Lịch sử sửa chữa thiết bị'

    equipment_id = fields.Many2one('lich_su_sua_chua', string='Thiết bị', required=True)
    repair_date = fields.Date(string='Ngày sửa chữa', required=True)
    repaired_by = fields.Many2one('res.users', string='Người thực hiện')