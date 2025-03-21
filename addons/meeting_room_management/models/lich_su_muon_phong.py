from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class LichSuMuonPhong(models.Model):
    _name = 'lich_su_muon_phong'
    _description = 'Lịch sử mượn phòng'
    _order = 'start_time desc'

    room_id = fields.Many2one('phong_hop', string='Phòng họp', required=True, ondelete='cascade')
    requester = fields.Many2one('res.users', string='Người mượn', required=True, ondelete='restrict')
    phone = fields.Char(string='Số điện thoại')
    email = fields.Char(string='Email')
    start_time = fields.Datetime(string='Bắt đầu', required=True)
    end_time = fields.Datetime(string='Kết thúc', required=True)
    status = fields.Selection([
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy')
    ], string='Trạng thái', default='completed', required=True)

    @api.constrains('start_time', 'end_time')
    def _check_time_validity(self):
        """ Đảm bảo thời gian bắt đầu phải nhỏ hơn thời gian kết thúc """
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError(_('Thời gian bắt đầu phải nhỏ hơn thời gian kết thúc.'))

    @api.model
    def create_history(self, booking):
        """ Tạo bản ghi lịch sử từ một lần đăng ký mượn phòng """
        if not booking or not booking.room_id or not booking.requester:
            _logger.warning("⚠️ Không thể tạo lịch sử: Thiếu thông tin quan trọng!")
            return False  

        status = 'completed' if booking.status == 'approved' else 'cancelled'

        _logger.info(f"📌 Tạo lịch sử: Phòng {booking.room_id.name}, Người mượn {booking.requester.name}, Trạng thái: {status}")

        return self.create({
            'room_id': booking.room_id.id,
            'requester': booking.requester.id,
            'phone': booking.requester.phone,
            'email': booking.requester.email,
            'start_time': booking.start_time,
            'end_time': booking.end_time,
            'status': status
        })

    @api.model
    def create(self, vals):
        """ Kiểm tra dữ liệu trước khi tạo bản ghi """
        _logger.info(f"🔹 Đang tạo lịch sử mượn phòng với dữ liệu: {vals}")

        if 'room_id' not in vals or not vals.get('room_id'):
            raise ValidationError(_('Không thể tạo lịch sử: Thiếu thông tin phòng họp.'))
        if 'requester' not in vals or not vals.get('requester'):
            raise ValidationError(_('Không thể tạo lịch sử: Thiếu thông tin người mượn.'))
        
        return super(LichSuMuonPhong, self).create(vals)

    def write(self, vals):
        """ Cập nhật trạng thái và gửi thông báo """
        result = super(LichSuMuonPhong, self).write(vals)
        if 'status' in vals:
            for rec in self:
                message = "Yêu cầu đặt phòng của bạn đã hoàn thành." if rec.status == 'completed' else "Yêu cầu đặt phòng của bạn đã bị hủy."
                rec.send_notification(message)
        return result

    def send_notification(self, message):
        """ Gửi thông báo đến người đặt phòng """
        for rec in self:
            if not rec.requester or not rec.requester.partner_id:
                _logger.warning(f"⚠️ Không thể gửi thông báo: Người mượn phòng {rec.requester.name} không có partner_id!")
                continue

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thông báo',
                    'message': message,
                    'type': 'info',
                    'sticky': False,
                }
            }
