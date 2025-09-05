from dateutil.relativedelta import relativedelta

from odoo import models, fields

class EstatePropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "An estate property type model"
    _order = "sequence,name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")