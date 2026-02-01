from odoo import models, fields
from datetime import date


class CongViec(models.Model):
    _name = 'du_an_cong_viec'
    _description = 'Công Việc Dự Án'

    name = fields.Char(string='Tên Công Việc', required=True)

    project_id = fields.Many2one(
    'quan_ly_du_an',   # ✅ ĐÚNG MODEL
    string='Dự Án',
    ondelete='cascade'
)


    assigned_to = fields.Many2one(
        'nhan_vien',
        string='Nhân viên Được Giao'
    )

    deadline = fields.Date(string='Hạn Chót')

    priority = fields.Selection([
        ('low', 'Thấp'),
        ('medium', 'Trung Bình'),
        ('high', 'Cao')
    ], string='Mức Độ Ưu Tiên', default='medium')

    status = fields.Selection([
        ('to_do', 'Chưa Bắt Đầu'),
        ('in_progress', 'Đang Thực Hiện'),
        ('done', 'Hoàn Thành')
    ], string='Trạng Thái', default='to_do')

    tag_ids = fields.Many2many(
        'du_an_cong_viec_tag',
        string='Thẻ'
    )

    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Tệp đính kèm'
    )
