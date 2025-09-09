from odoo import models, fields, api


class EstatePropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "An estate property type model"
    _order = "sequence,name"

    name = fields.Char(required=True)
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order property types."
    )
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_ids = fields.One2many(
        related="property_ids.offer_ids", string="Offers", readonly=True
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count", string="Number of Offers"
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
