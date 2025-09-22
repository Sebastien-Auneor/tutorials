# -*- coding: utf-8 -*-
{
    "name": "Estate",
    "depends": ["base"],
    "category": "Tutorials/estate",
    "installable": True,
    "application": True,
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        
        "views/estate_property_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_res_user.xml",
        "views/estate_property_type_views.xml",
        "views/estate_menu.xml",
        "demo/estate.property.type.csv",
        "demo/demo_data.xml",
        
        "security/security.xml",
        "demo/demo_data.xml"
    ],
    "demo": [
        "demo/estate.property.type.csv",
    ],
}
