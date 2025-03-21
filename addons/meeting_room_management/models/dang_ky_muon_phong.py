from odoo import models, fields, api

class DangKyMuonPhong(models.Model):
    _name = 'dang_ky_muon_phong'
    _description = 'Đăng ký mượn phòng'
    _inherit = ['mail.thread']

    room_id = fields.Many2one('phong_hop', string='Phòng họp', required=True)
    requester = fields.Many2one('res.users', string='Người mượn', default=lambda self: self.env.user, required=True)
    phone = fields.Char(string='Số điện thoại', compute='_compute_contact_info', store=True)
    email = fields.Char(string='Email', compute='_compute_contact_info', store=True)
    start_time = fields.Datetime(string='Thời gian bắt đầu', required=True)
    end_time = fields.Datetime(string='Thời gian kết thúc', required=True)
    status = fields.Selection([
        ('pending', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối')
    ], string='Trạng thái', default='pending', tracking=True)

    @api.depends('requester')
    def _compute_contact_info(self):
        """ Tự động điền số điện thoại và email dựa trên người mượn """
        for record in self:
            record.phone = record.requester.partner_id.phone if record.requester.partner_id else ''
            record.email = record.requester.partner_id.email if record.requester.partner_id else ''

    def action_confirm(self):
        """ Xác nhận đăng ký và gửi thông báo """
        for record in self:
            record.status = 'approved'

            # Gửi thông báo trên Chatter (mail.thread)
            if record.requester.partner_id:
                record.message_post(
                    body=f'Bạn đã đăng ký mượn phòng "{record.room_id.name}" thành công!',
                    partner_ids=[record.requester.partner_id.id],
                    subtype_xmlid='mail.mt_comment'
                )

        # Sử dụng `ir.actions.client` để hiển thị thông báo trên giao diện
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công!',
                'message': 'Đăng ký mượn phòng đã được duyệt!',
                'type': 'success',
                'sticky': False,  # Thông báo biến mất sau vài giây
            }
        }
