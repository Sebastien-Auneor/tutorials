from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Create a property type
        cls.property_type = cls.env['estate.property.type'].create({
            'name': 'House'
        })
        
        # Create a partner (buyer)
        cls.buyer = cls.env['res.partner'].create({
            'name': 'Test Buyer'
        })
        
        # Create a property
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100000,
            'property_type_id': cls.property_type.id,
        })

    def test_cannot_create_offer_for_sold_property(self):
        """Test that creating an offer for a sold property raises an error"""
        # First, create an offer and accept it
        offer = self.env['estate.property.offer'].create({
            'price': 90000,
            'partner_id': self.buyer.id,
            'property_id': self.property.id,
        })
        offer.action_accept()
        
        # Sell the property
        self.property.action_sold()
        
        # Verify the property is sold
        self.assertEqual(self.property.state, 'sold')
        
        # Try to create another offer - this should fail
        with self.assertRaises(UserError) as context:
            self.env['estate.property.offer'].create({
                'price': 95000,
                'partner_id': self.buyer.id,
                'property_id': self.property.id,
            })
        
        self.assertIn('Cannot create an offer for a sold property', str(context.exception))

    def test_cannot_sell_property_without_accepted_offers(self):
        """Test that selling a property without accepted offers raises an error"""
        # Create a new property for this test
        property_no_offers = self.env['estate.property'].create({
            'name': 'Property No Offers',
            'expected_price': 150000,
            'property_type_id': self.property_type.id,
        })
        
        # Try to sell without any offers - this should fail
        with self.assertRaises(UserError) as context:
            property_no_offers.action_sold()
        
        self.assertIn('Cannot sell a property with no accepted offers', str(context.exception))
        
        # Create an offer but don't accept it
        self.env['estate.property.offer'].create({
            'price': 140000,
            'partner_id': self.buyer.id,
            'property_id': property_no_offers.id,
        })
        
        # Try to sell with only pending offers - this should still fail
        with self.assertRaises(UserError) as context:
            property_no_offers.action_sold()
        
        self.assertIn('Cannot sell a property with no accepted offers', str(context.exception))

    def test_property_correctly_marked_as_sold(self):
        """Test that a property with accepted offers is correctly marked as sold"""
        # Create a new property for this test
        property_for_sale = self.env['estate.property'].create({
            'name': 'Property For Sale',
            'expected_price': 200000,
            'property_type_id': self.property_type.id,
        })
        
        # Create and accept an offer
        offer = self.env['estate.property.offer'].create({
            'price': 190000,
            'partner_id': self.buyer.id,
            'property_id': property_for_sale.id,
        })
        offer.action_accept()
        
        # Verify the property state is 'offer_accepted'
        self.assertEqual(property_for_sale.state, 'offer_accepted')
        
        # Sell the property
        property_for_sale.action_sold()
        
        # Verify the property is correctly marked as sold
        self.assertEqual(property_for_sale.state, 'sold')
        self.assertEqual(property_for_sale.selling_price, 190000)
        self.assertEqual(property_for_sale.buyer_id, self.buyer)

    def test_multiple_offers_scenario(self):
        """Test selling a property with multiple offers where one is accepted"""
        # Create a new property for this test
        property_multi_offers = self.env['estate.property'].create({
            'name': 'Property Multi Offers',
            'expected_price': 250000,
            'property_type_id': self.property_type.id,
        })
        
        # Create a second buyer
        buyer2 = self.env['res.partner'].create({
            'name': 'Test Buyer 2'
        })
        
        # Create multiple offers
        offer1 = self.env['estate.property.offer'].create({
            'price': 240000,
            'partner_id': self.buyer.id,
            'property_id': property_multi_offers.id,
        })
        
        offer2 = self.env['estate.property.offer'].create({
            'price': 260000,
            'partner_id': buyer2.id,
            'property_id': property_multi_offers.id,
        })
        
        # Accept the second offer
        offer2.action_accept()
        
        # Verify first offer is refused and second is accepted
        self.assertEqual(offer1.status, 'refused')
        self.assertEqual(offer2.status, 'accepted')
        
        # Sell the property
        property_multi_offers.action_sold()
        
        # Verify the property is sold correctly
        self.assertEqual(property_multi_offers.state, 'sold')
        self.assertEqual(property_multi_offers.selling_price, 260000)
        self.assertEqual(property_multi_offers.buyer_id, buyer2)

    def test_garden_onchange_behavior(self):
        """Test that the garden onchange sets garden_area and garden_orientation correctly"""
        from odoo.tests import Form
        
        # Create a new property using Form to trigger onchange
        with Form(self.env['estate.property']) as property_form:
            property_form.name = 'Property With Garden'
            property_form.expected_price = 300000
            property_form.property_type_id = self.property_type
            property_form.garden = True
            
            # Verify that garden_area and garden_orientation are set correctly
            self.assertEqual(property_form.garden_area, 10)
            self.assertEqual(property_form.garden_orientation, 'north')
            
            # Now set garden to False and check values are reset
            property_form.garden = False
            
            # Verify that garden_area and garden_orientation are reset
            self.assertEqual(property_form.garden_area, 0)
            self.assertFalse(property_form.garden_orientation)
    