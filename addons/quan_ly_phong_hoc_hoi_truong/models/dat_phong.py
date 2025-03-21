from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RoomBooking(models.Model):
    _name = 'dat_phong'
    _description = 'Đặt phòng'

    room_id = fields.Many2one('phong_hoc', string='Phòng', required=True)
    start_time = fields.Datetime(string='Bắt đầu', required=True)
    end_time = fields.Datetime(string='Kết thúc', required=True)
    user_id = fields.Many2one('res.users', string='Người đặt', default=lambda self: self.env.user)
    recurring = fields.Boolean(string='Đặt định kỳ')
    recurrence_rule = fields.Selection([
        ('daily', 'Hằng ngày'),
        ('weekly', 'Hằng tuần'),
        ('monthly', 'Hằng tháng')
    ], string='Loại định kỳ')

    @api.constrains('start_time', 'end_time', 'room_id')
    def _check_booking_conflict(self):
        for record in self:
            conflicts = self.env['dat_phong'].search([
                ('room_id', '=', record.room_id.id),
                ('id', '!=', record.id),
                ('start_time', '<', record.end_time),
                ('end_time', '>', record.start_time),
            ])
            if conflicts:
                raise ValidationError('Phòng đã được đặt trong khoảng thời gian này!')