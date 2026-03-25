from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CongViec(models.Model):
    _name = 'du_an_cong_viec'
    _description = 'Công Việc Dự Án'

    name = fields.Char('Tên Công Việc', required=True)

    project_id = fields.Many2one(
        'quan_ly_du_an',
        string='Dự Án',
        required=True,
        ondelete='cascade'
    )

    assigned_to = fields.Many2one(
        'nhan_vien',
        string='Nhân viên Được Giao'
    )

    deadline = fields.Date('Hạn Chót')

    priority = fields.Selection(
        [
            ('low', 'Thấp'),
            ('medium', 'Trung Bình'),
            ('high', 'Cao')
        ],
        default='medium'
    )

    status = fields.Selection(
        [
            ('to_do', 'Chưa Bắt Đầu'),
            ('in_progress', 'Đang Thực Hiện'),
            ('done', 'Hoàn Thành')
        ],
        default='to_do'
    )

    # =========================
    # DOMAIN NHÂN VIÊN
    # =========================
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

    # =========================
    # RÀNG BUỘC NHÂN VIÊN
    # =========================
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

    # =========================
    # ❌ CHẶN DỰ ÁN ĐÃ HỦY (ĐÚNG CÁCH)
    # =========================
    @api.model
    def create(self, vals):
        project = self.env['quan_ly_du_an'].browse(vals.get('project_id'))
        if project.status == 'cancelled':
            raise ValidationError(
                'Không thể tạo công việc khi dự án đã bị HỦY!'
            )

        rec = super().create(vals)
        rec.project_id._compute_progress()
        return rec

    def write(self, vals):
        for rec in self:
            if rec.project_id.status == 'cancelled':
                raise ValidationError(
                    'Không thể chỉnh sửa công việc khi dự án đã bị HỦY!'
                )

        res = super().write(vals)

        if 'status' in vals:
            self.mapped('project_id')._compute_progress()

        return res

    def unlink(self):
        projects = self.mapped('project_id')
        for p in projects:
            if p.status == 'cancelled':
                raise ValidationError(
                    'Không thể xóa công việc khi dự án đã bị HỦY!'
                )

        res = super().unlink()
        projects._compute_progress()
        return res