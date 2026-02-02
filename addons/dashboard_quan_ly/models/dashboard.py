from odoo import models, fields, api


class DashboardQuanLy(models.Model):
    _name = 'dashboard.quan.ly'
    _description = 'Dashboard Quản Lý Tổng Hợp'
    _rec_name = 'id'

    # =====================
    # FIELDS (CARD)
    # =====================
    tong_nhan_su = fields.Integer(string='Nhân sự', compute='_compute_dashboard', store=False)
    tong_du_an = fields.Integer(string='Dự án', compute='_compute_dashboard', store=False)
    tong_cong_viec = fields.Integer(string='Công việc', compute='_compute_dashboard', store=False)
    du_an_dang_lam = fields.Integer(string='Dự án đang làm', compute='_compute_dashboard', store=False)
    cong_viec_hoan_thanh = fields.Integer(string='Công việc hoàn thành', compute='_compute_dashboard', store=False)

    # =====================
    # FIELDS (BIỂU ĐỒ)
    # =====================
    cong_viec_dang_lam = fields.Integer(string='Công việc đang làm', compute='_compute_dashboard', store=False)
    cong_viec_chua_xong = fields.Integer(string='Công việc chưa xong', compute='_compute_dashboard', store=False)

    # =====================
    # TẠO 1 RECORD DASHBOARD (BẮT BUỘC)
    # =====================
    @api.model
    def init(self):
        if not self.search([], limit=1):
            self.create({})

    # =====================
    # COMPUTE DATA
    # =====================
    def _compute_dashboard(self):
        for rec in self:
            # Nhân sự
            rec.tong_nhan_su = self.env['nhan_vien'].search_count([])

            # Dự án
            rec.tong_du_an = self.env['quan_ly_du_an'].search_count([])
            rec.du_an_dang_lam = self.env['quan_ly_du_an'].search_count([
                ('status', '=', 'ongoing')
            ])

            # Công việc
            rec.tong_cong_viec = self.env['du_an_cong_viec'].search_count([])

            rec.cong_viec_hoan_thanh = self.env['du_an_cong_viec'].search_count([
                ('status', '=', 'done')
            ])

            rec.cong_viec_dang_lam = self.env['du_an_cong_viec'].search_count([
                ('status', '=', 'doing')
            ])

            rec.cong_viec_chua_xong = rec.tong_cong_viec - rec.cong_viec_hoan_thanh

    # =====================
    # ACTION CLICK CARD
    # =====================
    def action_open_nhan_su(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nhân sự',
            'res_model': 'nhan_vien',
            'view_mode': 'tree,form',
        }

    def action_open_du_an(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Dự án',
            'res_model': 'quan_ly_du_an',
            'view_mode': 'tree,form',
        }

    def action_open_cong_viec(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Công việc',
            'res_model': 'du_an_cong_viec',
            'view_mode': 'tree,form',
        }

    def action_open_cong_viec_hoan_thanh(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Công việc hoàn thành',
            'res_model': 'du_an_cong_viec',
            'view_mode': 'tree,form',
            'domain': [('status', '=', 'done')],
        }

    def action_open_cong_viec_dang_lam(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Công việc đang làm',
            'res_model': 'du_an_cong_viec',
            'view_mode': 'tree,form',
            'domain': [('status', '=', 'doing')],
        }
