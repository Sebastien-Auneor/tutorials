from odoo import models, fields, api


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        print("Creating the journal entry for the sale...")
        return super().action_sold()
