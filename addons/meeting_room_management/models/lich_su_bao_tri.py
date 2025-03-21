from odoo import models, fields, api

class LichSuBaoTri(models.Model):
    _name = 'lich_su_bao_tri'
    _description = 'Lịch sử bảo trì thiết bị'
    _inherit = ['mail.thread']

    device_id = fields.Many2one('thiet_bi', string="Thiết bị", required=True, tracking=True)
    room_id = fields.Many2one('phong_hop', string="Phòng họp", related='device_id.room_id', store=True, readonly=True)
    maintenance_date = fields.Datetime(string="Ngày bảo trì", default=fields.Datetime.now, required=True, tracking=True)
    technician = fields.Many2one('res.users', string="Kỹ thuật viên", required=True, tracking=True)
    notes = fields.Text(string="Ghi chú")
    status = fields.Selection([
        ('pending', 'Chờ xử lý'),
        ('in_progress', 'Đang sửa chữa'),
        ('completed', 'Hoàn thành')
    ], string="Trạng thái", default='pending', tracking=True)
    
    maintenance_type = fields.Selection([
        ('preventive', 'Bảo trì định kỳ'),
        ('corrective', 'Bảo trì sửa chữa'),
        ('emergency', 'Bảo trì khẩn cấp')
    ], string="Loại bảo trì", required=True, tracking=True)

    @api.model
    def create(self, vals):
        """ Cập nhật trạng thái thiết bị khi tạo yêu cầu bảo trì """
        record = super(LichSuBaoTri, self).create(vals)
        if record.device_id:
            record.device_id.status = 'maintenance'
        return record

    def action_mark_completed(self):
        """ Đánh dấu bảo trì đã hoàn thành """
        for record in self:
            record.status = 'completed'
            record.device_id.status = 'active'
