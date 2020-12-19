# Scratch application 
from odoo import models, fields, api 

class Scratch_product_template(models.Model): 
    """
    Extend Product Template Model to add diet information
    """
    _name = 'product.template'
    _inherit = 'product.template'

    calories = fields.Integer("Calories")
    serving_size = fields.Float("Serving Size")
    last_updated = fields.Date("Last Updated")
    nutrient_ids = fields.One2many("product.template.nutrient","product_id","Nutrients")
    nutrition_score = fields.Float("Nutrition Score", store=True, compute="_calc_score")

    @api.depends('nutrient_ids','nutrient_ids.value')
    def _calc_score(self):
            current_score = 0
            for nutrient in self.nutrient_ids:
                    if nutrient.nutrient_id.name == 'Protein':
                            current_score += nutrient.value * 2.5
                    elif nutrient.nutrient_id.name == 'Sodium':
                            current_score += nutrient.value * 1.5
            self.nutrition_score = current_score 
    
class Scratch_res_users_meal(models.Model):
    """
    Meal Model, which will contain a list of diet foods 
    """
    _name = 'res.users.meal'
    _description = 'Meal menu to calculate nutricions facts'
    
    name = fields.Char("Meal Name")
    meal_date = fields.Datetime("Meal Date")
    item_ids = fields.One2many("res.users.meal.item","meal_id")
    user_id = fields.Many2one("res.users","Meal User")
    large_meal = fields.Boolean("Large Meal")
    total_calories = fields.Integer(string="Total Meal Calories", store=True, compute="_sum_calories")
    notes = fields.Text("Meal Notes")

    @api.onchange('total_calories')
    def check_large_meal(self):
        if self.total_calories > 500:
            self.large_meal = True
        else:
            self.large_meal = False

    @api.depends('item_ids','item_ids.servings')
    def _sum_calories(self):
        current_calories = 0
        for meal_item in self.item_ids:
            current_calories += meal_item.calories * meal_item.servings
        self.total_calories = current_calories 

class Scratch_res_users_meal_item(models.Model):
    """
    Meal Item Model, which will represent every food 
    to be added on your meal
    """
    _name = 'res.users.meal.item'
    _description = 'Food Item to be added to the Meal menu'

    meal_id = fields.Many2one("res.users.meal")
    item_id = fields.Many2one("product.template","Meal Item")
    servings = fields.Float("Servings")
    calories = fields.Integer(related="item_id.calories", string="Calories Per Serving", store=True, readonly=True)
    notes = fields.Text("Meal item notes")
 
class Scratch_product_nutrient(models.Model):
    """
    Nutrient Model to add custom nutrients, such as:
    Cholesterol, Sodium, Protein and so on, that may differ based on the food.
    """
    _name = 'product.nutrient'
    _description = 'Nutrient types'
    
    name = fields.Char("Nutrient Name")
    uom_id = fields.Many2one("uom.uom", "Unit of Measure")
    description = fields.Text("Description")

class Scratch_product_template_nutrient(models.Model):
    """
    Ties together Nutrient Model with Products Model
    """
    _name = 'product.template.nutrient'
    _description = 'Nutrients information to every meal item'

    nutrient_id = fields.Many2one("product.nutrient", string="Product Nutrient")
    product_id = fields.Many2one("product.template")
    uom = fields.Char(related='nutrient_id.uom_id.name', string="UOM", readonly=True)
    value = fields.Float("Nutrient Value")
    daily_percent = fields.Float("Daily Recommended Value")

