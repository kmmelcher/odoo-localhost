from xmlrpc import client 
import csv


#Network information
server = "http://localhost:8069"
database = "dietfacts-app"
user = "kilian.melcher@gmail.com"
password = "123"

#Connect to the server
common = client.ServerProxy(f'{server}/xmlrpc/2/common')

#Authenticate connection to the server
uid = common.authenticate(database, user, password, {})

#Get Odoo API
odoo_api = client.ServerProxy(f'{server}/xmlrpc/2/object')

#Filter the search to get only scratch items
scratch_filter = [[['large_meal','=',True]]]

#Count how many records with there is based on a Model with a Filter
product_count = odoo_api.execute_kw(
        database,
        uid,
        password,
        'res.users.meal',
        'search_count',
        scratch_filter,
)

filename = "products.csv"
reader = csv.reader(open(filename,'r')) 

category_filter = [[['name', '=', 'Scratch Items']]]
categ_id = odoo_api.execute_kw(database,uid,password,'product.category','search',category_filter)

for row in reader:
    #Get csv columns
    product_name = row[0]
    calories = row[1]

    #Search if the product exists
    field_filter = [[['name','=',product_name]]]
    product_id = odoo_api.execute_kw(database,uid,password,'product.template','search',field_filter) 
    if not product_id:
        #Create a new product
        print ("Creating " + product_name + "...")
        record = [{'name': product_name, 'calories': calories, 'categ_id': categ_id[0]}]
        product_count = odoo_api.execute_kw(
            database,
            uid,
            password,
            'product.template',
            'create',
            record,
        )
    else:
        #Update product
        print ("Updating " + product_name + "...")
        record = {'calories': calories, 'categ_id': categ_id[0]}
        product_count = odoo_api.execute_kw(
            database,
            uid,
            password,
            'product.template',
            'write',
            [product_id,record],
        )
           
