from odoo import fields, models

class EstatePropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string='Name', required=True)
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', "The tag name must be unique."),
    ]
