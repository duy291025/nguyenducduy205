from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    ten = fields.Char("Điền họ tên", required=True)
    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ngay_sinh = fields.Date("Ngày sinh", required=True)
    que_quan = fields.Char("Quê quán", required=True)
    can_cuoc_cd = fields.Char("Căn cước công dân", required=True )
    email = fields.Char("Email", required=True)
    so_dien_thoai = fields.Char("Số điện thoại", required=True)
    tinh_trang_hon_nhan = fields.Char("Tình trạng hôn nhân", required=True)
    lich_su_cong_tac_ids = fields.One2many(
        "lich_su_cong_tac",  
        "nhan_vien_id",      
        string="Danh sách lịch sử công tác"
    )
    chung_chi_bang_cap_ids = fields.One2many(
        "chung_chi_bang_cap",  
        "nhan_vien_id",      
        string="Danh sách chứng chỉ bằng cấp"
    )
    tuoi = fields.Integer("Tuổi", compute="_compute_tinh_tuoi", store=True)
    anh = fields.Binary("Hình ảnh")

    # Trường giới tính
    gioi_tinh = fields.Selection(
        [
            ('nam', 'Nam'),
            ('nu', 'Nữ'),
            ('khac', 'Khác'),
        ],
        string="Giới tính",
        required=True,
        default='nam',  # Giá trị mặc định là 'Nam'
    )

    @api.depends("ngay_sinh")
    def _compute_tinh_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                today = date.today()
                record.tuoi = today.year - record.ngay_sinh.year - (
                    (today.month, today.day) < (record.ngay_sinh.month, record.ngay_sinh.day)
                )
            else:
                record.tuoi = 0

    @api.constrains("tuoi")
    def _check_tuoi(self):
        for record in self:
            if record.tuoi < 18:
                raise ValidationError("Đéo đủ tuổi")