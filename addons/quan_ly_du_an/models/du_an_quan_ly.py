from odoo import models, fields

class DuAn(models.Model):
    _name = 'du_an_quan_ly'
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

    # ==============================
    # LIÊN KẾT MODULE KHÁC (THÊM MỚI)
    # ==============================

    task_ids = fields.One2many(
    'du_an_cong_viec',   
    'project_id',        
    string='Công việc'
    )


    nhan_su_ids = fields.Many2many(
        'nhan.su',
        string='Nhân sự tham gia'
    )
