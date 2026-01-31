from odoo import models, fields

class DuAn(models.Model):
    _name = 'quan_ly_du_an'
    _description = 'Quản Lý Dự Án'

    name = fields.Char(string='Tên Dự Án', required=True)
    description = fields.Text(string='Mô Tả')
    start_date = fields.Date(string='Ngày Bắt Đầu')
    end_date = fields.Date(string='Ngày Kết Thúc')

    status = fields.Selection([
        ('ongoing', 'Đang Thực Hiện'),
        ('completed', 'Hoàn Thành'),
        ('cancelled', 'Đã Hủy')
    ], string='Trạng Thái', default='ongoing')

    # 🔥 LIÊN KẾT ĐÚNG VỚI CÔNG VIỆC (KHÔNG DÙNG task)
    cong_viec_ids = fields.One2many(
        'du_an_cong_viec',   # _name bên module quản lý công việc
        'project_id',
        string='Công Việc'
    )

    # 🔥 LIÊN KẾT NHÂN SỰ (giả sử model là nhan_su)
    nhan_su_ids = fields.Many2many(
    'nhan_vien',
    'nhan_vien_quan_ly_du_an_rel',   # tên bảng quan hệ
    'du_an_id',                      # cột FK về dự án
    'nhan_vien_id',                  # cột FK về nhân viên
    string='Nhân sự tham gia'
)

