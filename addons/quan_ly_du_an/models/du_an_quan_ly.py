from odoo import models, fields, api


class DuAn(models.Model):
    _name = 'quan_ly_du_an'
    _description = 'Quản Lý Dự Án'
    _rec_name = 'name'

    # =========================
    # THÔNG TIN DỰ ÁN
    # =========================
    name = fields.Char(
        string='Tên Dự Án',
        required=True
    )

    description = fields.Text(
        string='Mô Tả'
    )

    start_date = fields.Date(
        string='Ngày Bắt Đầu'
    )

    end_date = fields.Date(
        string='Ngày Kết Thúc'
    )

    status = fields.Selection(
        [
            ('ongoing', 'Đang Thực Hiện'),
            ('completed', 'Hoàn Thành'),
            ('cancelled', 'Đã Hủy')
        ],
        string='Trạng Thái',
        default='ongoing'
    )

    # =========================
    # LIÊN KẾT CÔNG VIỆC
    # =========================
    cong_viec_ids = fields.One2many(
        'du_an_cong_viec',
        'project_id',
        string='Công Việc'
    )

    # =========================
    # THÀNH VIÊN DỰ ÁN
    # =========================
    thanh_vien_ids = fields.Many2many(
        'nhan_vien',
        'nhan_vien_quan_ly_du_an_rel',
        'du_an_id',
        'nhan_vien_id',
        string='Nhân sự tham gia'
    )

    # =========================
    # TIẾN ĐỘ (%)
    # =========================
    progress = fields.Float(
        string='Tiến độ (%)',
        compute='_compute_progress'
    )

    # =========================
    # COMPUTE PROGRESS (AN TOÀN 100%)
    # =========================
    def _compute_progress(self):
        Task = self.env['du_an_cong_viec']

        for rec in self:
            tasks = Task.search([
                ('project_id', '=', rec.id)
            ])

            if not tasks:
                rec.progress = 0.0
                continue

            done_tasks = tasks.filtered(
                lambda t: t.status == 'done'
            )

            rec.progress = (len(done_tasks) / len(tasks)) * 100
