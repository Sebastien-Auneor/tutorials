from dateutil.relativedelta import relativedelta

from odoo import models, fields

class EstatePropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "An estate property type model"

    name = fields.Char(required=True)