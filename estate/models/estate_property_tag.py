from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Char(string="Color Index")

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "The tag name must be unique."),
    ]
