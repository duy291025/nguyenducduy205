from odoo import models, fields, api


class DuAn(models.Model):
    _name = 'quan_ly_du_an'
    _description = 'Quản Lý Dự Án'
    _rec_name = 'name'

    name = fields.Char(string='Tên Dự Án', required=True)
    description = fields.Text(string='Mô Tả')
    start_date = fields.Date(string='Ngày Bắt Đầu')
    end_date = fields.Date(string='Ngày Kết Thúc')

    status = fields.Selection(
        [
            ('ongoing', 'Đang Thực Hiện'),
            ('completed', 'Hoàn Thành'),
            ('cancelled', 'Đã Hủy')
        ],
        string='Trạng Thái',
        default='ongoing'
        
    )

    cong_viec_ids = fields.One2many(
        'du_an_cong_viec',
        'project_id',
        string='Công Việc'
    )

    thanh_vien_ids = fields.Many2many(
        'nhan_vien',
        'nhan_vien_quan_ly_du_an_rel',
        'du_an_id',
        'nhan_vien_id',
        string='Nhân sự tham gia'
    )

    progress = fields.Float(
        string='Tiến độ (%)',
        compute='_compute_progress'
    )

    # =========================
    # COMPUTE PROGRESS (CHUẨN NGHIỆP VỤ)
    # =========================
    @api.depends('cong_viec_ids.status', 'status')
    def _compute_progress(self):
        for rec in self:

            # ❌ Dự án đã hủy → luôn 0%
            if rec.status == 'cancelled':
                rec.progress = 0.0
                continue

            tasks = rec.cong_viec_ids

            # ❌ Không có công việc
            if not tasks:
                rec.progress = 0.0
                rec.status = 'ongoing'
                continue

            # ✅ Đếm công việc hoàn thành
            done_tasks = tasks.filtered(lambda t: t.status == 'done')

            percent = (len(done_tasks) / len(tasks)) * 100
            rec.progress = round(percent, 2)

            # 🔁 TỰ ĐỘNG ĐỒNG BỘ TRẠNG THÁI
            if percent == 100:
                rec.status = 'completed'
            else:
                rec.status = 'ongoing'