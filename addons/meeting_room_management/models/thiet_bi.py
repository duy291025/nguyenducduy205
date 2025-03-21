from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ThietBi(models.Model):
    _name = 'thiet_bi'
    _description = 'Thiết bị phòng họp'
    _inherit = ['mail.thread']

    name = fields.Char(string="Tên thiết bị", required=True, tracking=True)
    room_id = fields.Many2one('phong_hop', string="Phòng họp", required=True, tracking=True)
    status = fields.Selection([
        ('active', 'Hoạt động'),
        ('maintenance', 'Đang bảo trì'),
        ('inactive', 'Không sử dụng')
    ], string="Trạng thái", default='active', tracking=True)
    maintenance_count = fields.Integer(string="Số lần bảo trì", compute="_compute_maintenance_count")

    def _compute_maintenance_count(self):
        for record in self:
            record.maintenance_count = self.env['lich_su_bao_tri'].search_count([('device_id', '=', record.id)])

    def action_request_maintenance(self):
        """ Gửi yêu cầu bảo trì """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo yêu cầu bảo trì',
            'res_model': 'lich_su_bao_tri',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_device_id': self.id}
        }
