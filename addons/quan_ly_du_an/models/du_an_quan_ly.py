from odoo import models, fields


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
        comodel_name='du_an_cong_viec',
        inverse_name='project_id',
        string='Công Việc'
    )

    # =========================
    # THÀNH VIÊN DỰ ÁN
    # =========================
    thanh_vien_ids = fields.Many2many(
        comodel_name='nhan_vien',
        relation='nhan_vien_quan_ly_du_an_rel',
        column1='du_an_id',
        column2='nhan_vien_id',
        string='Nhân sự tham gia'
    )
