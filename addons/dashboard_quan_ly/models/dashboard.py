from odoo import models, fields


class DashboardQuanLy(models.Model):
    _name = 'dashboard.quan.ly'
    _description = 'Dashboard Quản Lý Tổng Hợp'

    tong_nhan_su = fields.Integer(compute='_compute_dashboard')
    tong_du_an = fields.Integer(compute='_compute_dashboard')
    tong_cong_viec = fields.Integer(compute='_compute_dashboard')
    du_an_dang_lam = fields.Integer(compute='_compute_dashboard')
    cong_viec_hoan_thanh = fields.Integer(compute='_compute_dashboard')

    def _compute_dashboard(self):
        for rec in self:
            # Nhân sự
            rec.tong_nhan_su = self.env['nhan_vien'].search_count([])

            # Dự án
            rec.tong_du_an = self.env['quan_ly_du_an'].search_count([])

            # Công việc
            rec.tong_cong_viec = self.env['du_an_cong_viec'].search_count([])

            # Dự án đang làm
            rec.du_an_dang_lam = self.env['quan_ly_du_an'].search_count([
                ('status', '=', 'ongoing')
            ])

            # Công việc hoàn thành
            rec.cong_viec_hoan_thanh = self.env['du_an_cong_viec'].search_count([
                ('status', '=', 'done')
            ])
