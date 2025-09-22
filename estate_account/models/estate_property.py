from odoo import models, fields, api, Command


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # Create an empty account.move for the invoice
        # Check access rights before creating the invoice
        self.env["account.move"].check_access('create')  # Check invoice creation access
        self.env["account.move"].create(
            {
                "partner_id": self.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "6% of selling price",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        },
                    ),
                    Command.create(
                        {
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100.00,
                        },
                    ),
                ],
            }
        )
        return super().action_sold()
