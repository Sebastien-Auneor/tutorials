from dateutil.relativedelta import relativedelta

from odoo import models, fields

class EstatePropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "An estate property type model"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")