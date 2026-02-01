from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CongViec(models.Model):
    _name = 'du_an_cong_viec'
    _description = 'Công Việc Dự Án'

    name = fields.Char(string='Tên Công Việc', required=True)

    project_id = fields.Many2one(
        'quan_ly_du_an',
        string='Dự Án',
        required=True,
        ondelete='cascade'
    )

    # ✅ BỎ domain ở đây (NGUYÊN NHÂN GÂY LỖI)
    assigned_to = fields.Many2one(
        'nhan_vien',
        string='Nhân viên Được Giao'
    )

    # 👉 field kỹ thuật (GIỮ NGUYÊN)
    thanh_vien_domain = fields.Many2many(
        'nhan_vien',
        compute='_compute_thanh_vien_domain',
        store=False
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

    # ==================================================
    # 1️⃣ COMPUTE DOMAIN – GIỮ NGUYÊN
    # ==================================================
    @api.depends('project_id')
    def _compute_thanh_vien_domain(self):
        for rec in self:
            rec.thanh_vien_domain = rec.project_id.thanh_vien_ids

    # ==================================================
    # 1️⃣.1 DOMAIN ĐỘNG – ĐÚNG CHUẨN ODOO
    # ==================================================
    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            return {
                'domain': {
                    'assigned_to': [
                        ('id', 'in', self.project_id.thanh_vien_ids.ids)
                    ]
                }
            }
        return {
            'domain': {
                'assigned_to': []
            }
        }

    # ==================================================
    # 2️⃣ CONSTRAINS – GIỮ NGUYÊN (CHẶN DB)
    # ==================================================
    @api.constrains('assigned_to', 'project_id')
    def _check_assigned_to(self):
        for rec in self:
            if (
                rec.assigned_to
                and rec.project_id
                and rec.assigned_to not in rec.project_id.thanh_vien_ids
            ):
                raise ValidationError(
                    'Nhân viên được giao KHÔNG thuộc dự án này!'
                )
