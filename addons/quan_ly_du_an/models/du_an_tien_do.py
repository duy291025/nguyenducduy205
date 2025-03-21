from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DuAnMocTienDo(models.Model):
    _name = 'du_an_tien_do'
    _description = 'Mốc Tiến Độ Dự Án'

    name = fields.Char(string="Tên Mốc Tiến Độ", required=True)
    project_id = fields.Many2one('du_an_quan_ly', string="Dự Án")
    ngay_du_kien = fields.Date(string="Ngày Dự Kiến")
    phan_tram_hoan_thanh = fields.Float(string="Phần Trăm Hoàn Thành", default=0.0)

    @api.constrains('phan_tram_hoan_thanh')
    def _check_phan_tram(self):
        for record in self:
            if record.phan_tram_hoan_thanh < 0 or record.phan_tram_hoan_thanh > 100:
                raise ValidationError("Phần trăm hoàn thành phải từ 0 đến 100!")
