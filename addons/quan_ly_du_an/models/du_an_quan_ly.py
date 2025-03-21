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

    # Quan hệ One2many
    task_ids = fields.One2many('du_an_cong_viec', 'project_id', string='Công Việc')
    resource_ids = fields.One2many('du_an_tai_nguyen', 'project_id', string='Tài Nguyên')
    risk_ids = fields.One2many('du_an_rui_ro', 'project_id', string='Rủi Ro')
    nhan_su_du_an_ids = fields.One2many('du_an_quan_ly_nhan_su', 'project_id', string='Nhân sự thực hiện dự án')
    progress_ids = fields.One2many('du_an_tien_do', 'project_id', string= 'Tiến Độ' )
