__author__ = 'GN3'
import pandas as pd
import re
import numpy as np
import math
import pickle
from collections import Counter
import operator
pd.options.mode.chained_assignment = None  # default='warn'


basic_ing_meat_fish = ['sole fish','smoked fish','gurnard','mullet','fish','chops','steak', 'steaks', 'ribs','meat and meat products','tilapia','sausages','mussels','calamari','monkfish','pig','lobsters','anchovy','oyster','crabmeat','meat', 'beef', 'pork', 'veal', 'lamb', 'mutton', 'beef steak', 'roast beef', 'ground beef', 'hamburgers', 'cutlets', 'spare ribs', 'pork chops', 'lamb chops', 'veal cutlets', 'ham', 'bacon', 'pastrami', 'corned beef', 'sausage', 'salami', 'smoked sausage', 'bologna', 'hot dogs', 'link sausages', 'frankfurters', 'wieners', 'poultry', 'chicken', 'turkey', 'goose', 'duck', 'whole chicken', 'chicken quarters', 'chicken leg', 'drumstick', 'chicken breast', 'turkey breast', 'fish', 'salmon', 'trout', 'sturgeon', 'cod', 'sole', 'flatfish', 'pike', 'halibut', 'tuna', 'perch', 'sea bass', 'herring', 'eel', 'mackerel', 'fish steak', 'salmon steak', 'fish fillet', 'fillet of sole', 'smoked fish', 'salted fish', 'marinated herring', 'caviar', 'seafood', 'shrimp', 'prawns', 'crab', 'lobster', 'oysters', 'clams', 'shellfish', 'squid']
basic_ing_murder = ['mayo','eggs', 'egg', 'honey']
basic_ing_dairy = ['pasteurized milk','butermilk','milk', 'whole milk', 'skim milk', 'low-fat milk', 'nonfat milk', 'pasteursized milk', 'dry milk', 'condensed milk', 'yogurt', 'kefir', 'sour milk', 'buttermilk', 'cream', 'sour cream', 'butter', 'cottage cheese', "farmers' cheese", 'home-made cheese', 'cream cheese', 'cheese', 'swiss cheese', 'parmesan', 'cheddar', 'mozzarella', 'roquefort', 'blue cheese', 'hard cheese', 'soft cheese', 'sharp cheese', 'mild cheese', 'smoked cheese', 'grated cheese', 'cheese spread', 'ice cream', 'sundae', 'vanilla ice cream', 'chocolate ice cream', 'ice cream cone']
basic_ing_grains = ['breadcrumbs','beans','macadamia nuts','chickpeas','tapioca','cornstarch','bucatini','quinoa','cornflour','bulgur','yeast','wheat', 'rye', 'oats', 'corn (maize)', 'barley', 'buckwheat', 'rice', 'baked goods', 'bakery goods', 'rolls', 'buns', 'cakes', 'cookies', 'pies', 'cereal', 'corn flakes', 'oat flakes', 'wheat flakes', 'rice flakes', 'muesli', 'popcorn', 'pasta', 'macaroni', 'noodles', 'spaghetti', 'vermicelli', 'angel-hair pasta', 'ravioli', 'dumplings', 'flour', 'dough', 'batter', 'cake mix']
basic_ing_sweet = ['gum', 'molasses', 'nutella','crème','maple','mascarpone','ladyfingers','syrup','cacao','pistachios','candies', 'sweets', 'caramels', 'mint drops', 'jelly beans', 'lollipop', 'bonbons', 'chocolates', 'chocolate candies', 'chocolate', 'chocolate bar', 'candy bar', 'taffy', 'toffee', 'fudge', 'marshmallow', 'sugar']
basic_ing_pastry = ['baguette','bread', 'white bread', 'whole wheat bread', 'rye bread', 'raisin bread', 'garlic bread', 'sourdough bread', 'french bread', 'french loaf', 'pita bread', 'tortilla', 'roll', 'bread roll', 'sesame roll', 'poppy seed roll', 'cinnamon roll', 'hamburger bun', 'hot dog bun', 'crescent roll', 'croissant', 'bagel', 'cracker', 'biscuit', 'cookie', 'toast', 'breadstick', 'pretzel', 'hardtack', 'ship biscuit', 'wafer', 'waffle', 'crouton', 'cake', 'shortcake', 'fruitcake', 'strawberry shortcake', 'coffee cake', 'chocolate chip cake', 'blueberry muffin', 'raisin muffin', 'cupcake', 'brownie', 'oatmeal cookie', 'chocolate cookie', 'gingerbread', 'cake', 'birthday cake', 'wedding cake', 'christmas cake', 'chocolate cake', 'honey cake', 'cheesecake', 'layer cake', 'napoleon', 'sponge cake', 'torte', 'pastry', 'home-made pie', 'apple pie', 'blueberry pie', 'tart', 'mince pie', 'meat pie', 'knish', 'pizza', 'doughnut', 'english muffin', 'fritters', 'pancakes', 'waffles']
basic_ing_fruit = ['pomegranate melon', 'ackee','plantains','clementines','fresh fruit', 'apple', 'apples','lychees', 'pear', 'pears', 'apricot', 'apricots', 'peach', 'peaches', 'nectarine', 'nectarines', 'plum', 'plums', 'grapes', 'cherry', 'cherries', 'sweet cherry', 'lemon', 'lemons', 'lime', 'limes', 'orange', 'oranges', 'tangerine', 'tangerines', 'grapefruit', 'grapefruits', 'banana', 'bananas', 'kiwi', 'kiwis', 'olive', 'olives', 'pineapple', 'pineapples', 'papaya', 'papayas', 'mango', 'mangoes', 'avocado', 'avocados', 'coconut', 'coconuts', 'persimmon', 'persimmons', 'pomegranate', 'melon', 'melons', 'watermelon', 'watermelons', 'berries', 'strawberry', 'strawberries', 'blueberry', 'blueberries', 'cranberry', 'cranberries', 'raspberry', 'raspberries', 'black currants', 'red currants', 'potatoes', 'gooseberry', 'blackberry', 'blackberries', 'whortleberry', 'dried fruit', 'dried apricots', 'raisins', 'figs', 'prunes', 'dates', 'candied fruit', 'nuts', 'hazelnuts', 'walnuts', 'almonds', 'chestnuts', 'peanuts', 'pistachio nuts', 'cashew nuts', 'pecans', 'macadamia nuts', 'apricot pits', 'pumpkin seeds', 'sunflower seeds', 'raspberry jam', 'cranberry jam', 'grape jelly', 'maple syrup', 'peanut butter']
basic_ing_vegetable = ['tamari','ginger','aubergines', 'lettuces', 'peas','apricot pits','cherry lemon','arugula','shallots', 'shallot','tofu','Fennel','carrots', 'portobellos','portobello','artichokes','tomatillos','jalapeños','bean','cilantro','fennel', 'onions', 'sage','tomatoes','árbol','scallions','anise','mirepoix','celeriac','horseradish','parsnip','turmeric','chives','bok choy','beetroot','lemongrass','leeks','chillies','chilli','scallion','peppers','jalapeño','broth','fresh vegetables', 'salad vegetables', 'canned vegetables', 'leaf vegetables', 'greens', 'tomato', 'cucumber', 'onion', 'garlic', 'carrot', 'beets', 'potato', 'sweet pepper', 'paprika', 'hot pepper', 'chili pepper', 'green onions', 'spring onions', 'leek', 'mushrooms', 'cabbage', 'cauliflower', 'broccoli', 'brussels sprouts', 'collards', 'artichoke', 'lettuce', 'spinach', 'celery', 'asparagus', 'cress', 'watercress', 'eggplant', 'aubergine', 'squash', 'gourd', 'zucchini', 'pumpkin', 'turnip', 'radish', 'horse radish', 'pickled cucumbers', 'pickles', 'marinated cucumbers', 'sauerkraut', 'canned olives', 'green peas', 'sweet peas', 'string beans', 'lima beans', 'kidney beans', 'black beans', 'soybeans', 'corn', 'sweet corn', 'dill', 'parsley', 'basil', 'coriander', 'mint']
basic_ing_beverage = ['champagne vodka','water', 'soda','fruit juice','port','sherry','juice','vermouth','limoncello','pastis','scotch', 'bourbon','apple juice', 'orange juice', 'grapefruit juice', 'lemon juice', 'tomato juice', 'fresh fruit juice', 'frozen fruit juice', 'tea', 'green tea', 'black tea', 'tea with milk', 'iced tea', 'herbal tea', 'mint tea', 'indian tea', 'coffee', 'instant coffee', 'espresso', 'cappuccino', 'decaffeinated coffee', 'decaf', 'coffee with milk', 'coffee with cream', 'half-and-half', 'black coffee', 'cocoa', 'hot chocolate', 'milkshake', 'mineral water', 'spring water', 'soft drinks', 'soda water', 'lemonade', 'cider', 'ginger ale', 'beer', 'wine', 'red wine', 'white wine', 'champagne', 'vodka', 'cognac', 'brandy', 'whisky', 'liqueur', 'cocktail', 'punch', 'rum']
basic_ing_sauce = ['soy','vinegar','vanilla','worcestershire','tomato sauce', 'ketchup', 'mushroom sauce', 'meat sauce', 'steak sauce', 'gravy', 'spaghetti sauce', 'hot sauce', 'chili sauce', 'barbecue sauce', 'sweet-and-sour sauce', 'soy sauce', 'garlic sauce', 'white sauce', 'dip sauce', 'apple sauce', 'cranberry sauce', 'salad dressing', 'russian dressing', 'italian dressing', 'french dressing', 'blue-cheese dressing', 'mayonnaise', 'vegetable oil', 'olive oil', 'corn oil', 'sunflower seed oil', 'sesame oil', 'margarine', 'grease', 'lard', 'animal fat', 'vegetable fat']
basic_ing_seasoning = ['cumin','tabasco','peppercorns','seasoning', 'spices', 'flavoring', 'condiment', 'relish', 'pepper', 'ground pepper', 'whole pepper', 'red pepper', 'hot pepper', 'chili pepper', 'salt', 'mustard', 'herbs', 'bay leaf', 'basil', 'cinnamon', 'cloves', 'coriander', 'dill', 'parsley', 'nutmeg', 'mint', 'caraway', 'thyme', 'cardamom', 'tarragon', 'lemon peel', 'oregano', 'marjoram', 'rosemary', 'viniger', 'balsamic']

basic_ing = {}
basic_ing['meat_fish'] = {x:0 for x in ['sole fish','smoked fish','gurnard','mullet','fish','chops','steak', 'steaks', 'ribs','meat and meat products','tilapia','sausages','mussels','calamari','monkfish','pig','lobsters','anchovy','oyster','crabmeat','meat', 'beef', 'pork', 'veal', 'lamb', 'mutton', 'beef steak', 'roast beef', 'ground beef', 'hamburgers', 'cutlets', 'spare ribs', 'pork chops', 'lamb chops', 'veal cutlets', 'ham', 'bacon', 'pastrami', 'corned beef', 'sausage', 'salami', 'smoked sausage', 'bologna', 'hot dogs', 'link sausages', 'frankfurters', 'wieners', 'poultry', 'chicken', 'turkey', 'goose', 'duck', 'whole chicken', 'chicken quarters', 'chicken leg', 'drumstick', 'chicken breast', 'turkey breast', 'fish', 'salmon', 'trout', 'sturgeon', 'cod', 'sole', 'flatfish', 'pike', 'halibut', 'tuna', 'perch', 'sea bass', 'herring', 'eel', 'mackerel', 'fish steak', 'salmon steak', 'fish fillet', 'fillet of sole', 'smoked fish', 'salted fish', 'marinated herring', 'caviar', 'seafood', 'shrimp', 'prawns', 'crab', 'lobster', 'oysters', 'clams', 'shellfish', 'squid']}
basic_ing['murder'] = {x:0 for x in ['turkey breast eggs','mayo','eggs', 'egg', 'honey']}
basic_ing['dairy'] = {x:0 for x in ['pasteurized milk','butermilk','milk', 'whole milk', 'skim milk', 'low-fat milk', 'nonfat milk', 'pasteursized milk', 'dry milk', 'condensed milk', 'yogurt', 'kefir', 'sour milk', 'buttermilk', 'cream', 'sour cream', 'butter', 'cottage cheese', "farmers' cheese", 'home-made cheese', 'cream cheese', 'cheese', 'swiss cheese', 'parmesan', 'cheddar', 'mozzarella', 'roquefort', 'blue cheese', 'hard cheese', 'soft cheese', 'sharp cheese', 'mild cheese', 'smoked cheese', 'grated cheese', 'cheese spread', 'ice cream', 'sundae', 'vanilla ice cream', 'chocolate ice cream', 'ice cream cone']}
basic_ing['grains'] = {x:0 for x in ['chickpeas','tapioca','cornstarch','bucatini','quinoa','cornflour','bulgur','yeast','wheat', 'rye', 'oats', 'corn (maize)', 'barley', 'buckwheat', 'rice', 'baked goods', 'bakery goods', 'rolls', 'buns', 'cakes', 'cookies', 'pies', 'cereal', 'corn flakes', 'oat flakes', 'wheat flakes', 'rice flakes', 'muesli', 'popcorn', 'pasta', 'macaroni', 'noodles', 'spaghetti', 'vermicelli', 'angel-hair pasta', 'ravioli', 'dumplings', 'flour', 'dough', 'batter', 'cake mix']}
basic_ing['sweet'] = {x:0 for x in ['nuts and seeds','gum', 'molasses', 'nutella','crème','maple','mascarpone','ladyfingers','syrup','cacao','pistachios','candies', 'sweets', 'caramels', 'mint drops', 'jelly beans', 'lollipop', 'bonbons', 'chocolates', 'chocolate candies', 'chocolate', 'chocolate bar', 'candy bar', 'taffy', 'toffee', 'fudge', 'marshmallow', 'sugar']}
basic_ing['pastry']  = {x:0 for x in ['baguette','bread', 'white bread', 'whole wheat bread', 'rye bread', 'raisin bread', 'garlic bread', 'sourdough bread', 'french bread', 'french loaf', 'pita bread', 'tortilla', 'roll', 'bread roll', 'sesame roll', 'poppy seed roll', 'cinnamon roll', 'hamburger bun', 'hot dog bun', 'crescent roll', 'croissant', 'bagel', 'cracker', 'biscuit', 'cookie', 'toast', 'breadstick', 'pretzel', 'hardtack', 'ship biscuit', 'wafer', 'waffle', 'crouton', 'cake', 'shortcake', 'fruitcake', 'strawberry shortcake', 'coffee cake', 'chocolate chip cake', 'blueberry muffin', 'raisin muffin', 'cupcake', 'brownie', 'oatmeal cookie', 'chocolate cookie', 'gingerbread', 'cake', 'birthday cake', 'wedding cake', 'christmas cake', 'chocolate cake', 'honey cake', 'cheesecake', 'layer cake', 'napoleon', 'sponge cake', 'torte', 'pastry', 'home-made pie', 'apple pie', 'blueberry pie', 'tart', 'mince pie', 'meat pie', 'knish', 'pizza', 'doughnut', 'english muffin', 'fritters', 'pancakes', 'waffles']}
basic_ing['fruit']  = {x:0 for x in ['pomegranate melon', 'ackee','plantains','clementines','fresh fruit', 'apple', 'apples','lychees', 'pear', 'pears', 'apricot', 'apricots', 'peach', 'peaches', 'nectarine', 'nectarines', 'plum', 'plums', 'grapes', 'cherry', 'cherries', 'sweet cherry', 'lemon', 'lemons', 'lime', 'limes', 'orange', 'oranges', 'tangerine', 'tangerines', 'grapefruit', 'grapefruits', 'banana', 'bananas', 'kiwi', 'kiwis', 'olive', 'olives', 'pineapple', 'pineapples', 'papaya', 'papayas', 'mango', 'mangoes', 'avocado', 'avocados', 'coconut', 'coconuts', 'persimmon', 'persimmons', 'pomegranate', 'melon', 'melons', 'watermelon', 'watermelons', 'berries', 'strawberry', 'strawberries', 'blueberry', 'blueberries', 'cranberry', 'cranberries', 'raspberry', 'raspberries', 'black currants', 'red currants', 'potatoes', 'gooseberry', 'blackberry', 'blackberries', 'whortleberry', 'dried fruit', 'dried apricots', 'raisins', 'figs', 'prunes', 'dates', 'candied fruit', 'nuts', 'hazelnuts', 'walnuts', 'almonds', 'chestnuts', 'peanuts', 'pistachio nuts', 'cashew nuts', 'pecans', 'macadamia nuts', 'apricot pits', 'pumpkin seeds', 'sunflower seeds', 'raspberry jam', 'cranberry jam', 'grape jelly', 'maple syrup', 'peanut butter']}
basic_ing['vegetable']  = {x:0 for x in ['cherry lemon','arugula','shallots', 'shallot','leaf', 'leaves','tofu','Fennel','carrots', 'portobellos','portobello','artichokes','tomatillos','jalapeños','bean','cilantro','fennel', 'onions', 'sage','tomatoes','árbol','scallions','anise','mirepoix','celeriac','horseradish','parsnip','turmeric','chives','bok choy','beetroot','lemongrass','leeks','chillies','chilli','scallion','peppers','jalapeño','broth','fresh vegetables', 'salad vegetables', 'canned vegetables', 'leaf vegetables', 'greens', 'tomato', 'cucumber', 'onion', 'garlic', 'carrot', 'beets', 'potato', 'sweet pepper', 'paprika', 'hot pepper', 'chili pepper', 'green onions', 'spring onions', 'leek', 'mushrooms', 'cabbage', 'cauliflower', 'broccoli', 'brussels sprouts', 'collards', 'artichoke', 'lettuce', 'spinach', 'celery', 'asparagus', 'cress', 'watercress', 'eggplant', 'aubergine', 'squash', 'gourd', 'zucchini', 'pumpkin', 'turnip', 'radish', 'horse radish', 'pickled cucumbers', 'pickles', 'marinated cucumbers', 'sauerkraut', 'canned olives', 'green peas', 'sweet peas', 'string beans', 'lima beans', 'kidney beans', 'black beans', 'soybeans', 'corn', 'sweet corn', 'dill', 'parsley', 'basil', 'coriander', 'mint']}
basic_ing['beverage']  = {x:0 for x in ['port','sherry','juice','vermouth','limoncello','pastis','scotch', 'bourbon','apple juice', 'orange juice', 'grapefruit juice', 'lemon juice', 'tomato juice', 'fresh fruit juice', 'frozen fruit juice', 'tea', 'green tea', 'black tea', 'tea with milk', 'iced tea', 'herbal tea', 'mint tea', 'indian tea', 'coffee', 'instant coffee', 'espresso', 'cappuccino', 'decaffeinated coffee', 'decaf', 'coffee with milk', 'coffee with cream', 'half-and-half', 'black coffee', 'cocoa', 'hot chocolate', 'milkshake', 'mineral water', 'spring water', 'soft drinks', 'soda water', 'lemonade', 'cider', 'ginger ale', 'beer', 'wine', 'red wine', 'white wine', 'champagne', 'vodka', 'cognac', 'brandy', 'whisky', 'liqueur', 'cocktail', 'punch', 'rum']}
basic_ing['untagged']  = {x:0 for x in ['macadamia nuts apricot pits', 'preserves', 'vegetables', 'beans', 'vegetables', 'breadcrumbs', 'aubergines', 'lettuces', 'peas', 'beans', 'fruit juice', 'beverages', 'drinks', 'water', 'soda', 'water', 'ginger', 'alcoholic drinks', 'liquor', 'champagne vodka', 'liqueur cocktail', 'sauces', 'salad dressings', 'oil', 'fats', 'tamari', 'soy', 'seasoning and spices', 'candy']}
basic_ing['sauce']  = {x:0 for x in ['vinegar','vanilla','worcestershire','sauce','tomato sauce', 'ketchup', 'mushroom sauce', 'meat sauce', 'steak sauce', 'gravy', 'spaghetti sauce', 'hot sauce', 'chili sauce', 'barbecue sauce', 'sweet-and-sour sauce', 'soy sauce', 'garlic sauce', 'white sauce', 'dip sauce', 'apple sauce', 'cranberry sauce', 'salad dressing', 'russian dressing', 'italian dressing', 'french dressing', 'blue-cheese dressing', 'mayonnaise', 'vegetable oil', 'olive oil', 'corn oil', 'sunflower seed oil', 'sesame oil', 'margarine', 'grease', 'lard', 'animal fat', 'vegetable fat']}
basic_ing['seasoning']  = {x:0 for x in ['cumin', 'powder','tabasco','peppercorns','seasoning', 'spices', 'flavoring', 'condiment', 'relish', 'pepper', 'ground pepper', 'whole pepper', 'red pepper', 'hot pepper', 'chili pepper', 'salt', 'mustard', 'herbs', 'seeds', 'bay leaf', 'basil', 'cinnamon', 'cloves', 'coriander', 'dill', 'parsley', 'nutmeg', 'mint', 'caraway', 'thyme', 'cardamom', 'tarragon', 'lemon peel', 'oregano', 'marjoram', 'rosemary', 'viniger', 'balsamic']}

grade_basic_ing = dict.fromkeys([x for x in basic_ing_meat_fish], 4)
grade_basic_ing.update(dict.fromkeys([x for x in basic_ing_murder+basic_ing_dairy+basic_ing_grains], 3))
grade_basic_ing.update(dict.fromkeys([x for x in basic_ing_sweet+basic_ing_pastry+basic_ing_fruit+basic_ing_vegetable+basic_ing_beverage], 2))
grade_basic_ing.update(dict.fromkeys([x for x in basic_ing_sauce+basic_ing_seasoning], 1))

open_screen_products = ['butter', 'cheese', 'milk', 'cream', 'parmesan', 'cheddar', 'cream cheese', 'sour cream', 'yogurt', 'mozzarella',
                        'sugar', 'chocolate', 'syrup', 'crème', 'molasses', 'mascarpone', 'pistachios', 'cacao', 'marshmallow','nutella', 'toffee',
                        'flour', 'rice', 'pasta', 'wheat', 'cornstarch', 'oats', 'yeast', 'noodles', 'dough', 'spaghetti',
                        'chicken', 'beef', 'bacon', 'pork', 'chicken breast', 'ground beef', 'sausage', 'fish', 'shrimp', 'turkey', 'lamb', 'salmon', 'ham', 'meat', 'steak',
                        'lemon', 'potatoes', 'lime', 'coconut', 'apple', 'orange', 'almonds', 'walnuts', 'cherry', 'pecans', 'pineapple', 'raisins', 'strawberries', 'olives', 'peanut butter','cherries', 'maple syrup', 'nuts', 'cranberries',
                        'egg', 'honey', 'mayo',
                        'white wine', 'red wine','cider', 'orange juice',
                        'ginger','beans', 'peas', 'breadcrumbs','soy', 'tamari','bread','biscuit',
                        'olive oil', 'vanilla', 'vinegar',
                        'cinnamon', 'parsley','mustard', 'thyme', 'cumin', 'basil',
                        'onion', 'garlic', 'parsley', 'carrot', 'celery', 'broth', 'basil', 'tomato', 'corn', 'peppers', 'cilantro', 'paprika', 'coriander', 'chilli', 'spinach', 'mint', 'shallots', 'dill', 'pumpkin', 'chives']

ing_units = ['dashes', 'cups', 'cup', 'dash', 'teaspoon', 'teaspoons', 'tablespoon', 'tablespoons', 'slices', 'slice', 'whole', 'pinch','bag','package', 'packages', 'bags', 'quart', 'stick','sticks','bunch','can','jar','jars','loaf','pound','cubes','pieces','weight','bar','cans','cartons','clove','bunches','box']

ing_frac = ['¼','⅓','½','⅔','¾']
ing_nums = [str(i) for i in range(10)]
ing_optional = '((o|O)(p|P)(t|T)(i|I)(o|O)(n|N)(a|A)(l|L))|((a|A)(c|C)(c|C)(o|O)(m|M)(p|P)(a|A)(n|N)(i|I)(m|M)(e|E)(n|N)(t|T))'

def json_to_pandas(path):
    # read the entire file into a python array
    json_data = []
    with open(path, 'r') as f:
        for l in f:
            json_data.append(l.rstrip())

    # each element of 'data' is an individual JSON object.
    # i want to convert it into an *array* of JSON objects
    # which, in and of itself, is one large JSON object
    # basically... add square brackets to the beginning
    # and end, and have all the individual business JSON objects
    # separated by a comma
    data_json_str = "[" + ','.join(json_data) + "]"

    # now, load it into pandas
    return pd.read_json(data_json_str)

def drop_useless_columns(db):
    db = db.drop('creator',1)
    db = db.drop('dateModified',1)
    db = db.drop('datePublished',1)
    db = db.drop('totalTime',1)
    db = db.drop('recipeInstructions',1)
    db = db.drop('source',1)
    db = db.drop('ts',1)

    # change time format to total of minutes. first prepTime then cookTime
    for idx in range(len(db.prepTime)):
        if isinstance(db.prepTime[idx],str):
            time = re.match(r'PT(\d+)H?(\d+)?(M)?', db.prepTime[idx])
            if time:
                if time.group(2):   new_time = int(time.group(1)) * 60 + int(time.group(2))   # meaning we have both minutes and hours
                elif time.group(3): new_time = int(time.group(1))           # only minutes
                else:               new_time = int(time.group(1)) * 60      # only hours
            else: new_time = float('nan')
            db.prepTime[idx] = float(new_time)

    for idx in range(len(db.cookTime)):
        if isinstance(db.cookTime[idx],str):
            time = re.match(r'PT(\d+)H?(\d+)?(M)?', db.cookTime[idx])
            if time:
                if time.group(2):   new_time = int(time.group(1)) * 60 + int(time.group(2))   # meaning we have both minutes and hours
                elif time.group(3): new_time = int(time.group(1))           # only minutes
                else:               new_time = int(time.group(1)) * 60      # only hours
            else: new_time = float('nan')
            db.cookTime[idx] = float(new_time)


    # add 'time' axis, maximal of both times
    db.loc[:,'time'] = db.loc[:,('prepTime', 'cookTime')].max(axis=1)
    db.ix[db.time==0, 'time'] = float('nan')
    db = db.drop('cookTime',1)
    db = db.drop('prepTime',1)

    db['fix_ingredients'] = pd.Series(np.random.randn(len(db['time'])), index=db.index).astype(object)
    db['match'] = pd.Series(0 * (len(db['time'])), index=db.index)

    return db

def split_ingredients(db):
    for i in range(0,len(db)):
        db.ingredients[i] = db.ingredients[i].split("\n")

    return db

def clean_ingredients(db):
    # for ing_list in db.ingredients:
    for idx in range(len(db.ingredients)):
        cur_ingredients = []
        for product in db.ingredients[idx]:
            cur_product = product.strip().split('(recipe follows)')[0].strip().lower()

            # contains a number, in the form of "a X of Y", "an Orange", doesn't contain ':', 'or canned'
            if (set(ing_frac + ing_nums).intersection(set(cur_product))\
                    or re.match(r'^a|A(n)?\s(\w*)(\sof)?(.*)', cur_product))\
                    and not re.search(ing_optional, cur_product):

                cur_product_split = re.findall(r"[\w]+", cur_product)
                cur_product_split_pairs = [cur_product_split[i]+' '+cur_product_split[i+1] for i in range(len(cur_product_split)-1)]

                mutual_pairs = set(cur_product_split_pairs).intersection(       # add 2-word ingredients
                        set(basic_ing_murder+basic_ing_beverage+basic_ing_dairy+basic_ing_fruit+basic_ing_grains+basic_ing_meat_fish+\
              basic_ing_pastry+basic_ing_sauce+basic_ing_seasoning+basic_ing_sweet+basic_ing_vegetable))

                cur_ingredients.extend(mutual_pairs)
                for mp in mutual_pairs:
                    cur_product_split = [item for item in cur_product_split if item not in mp.split()]

                cur_ingredients.extend(     # add single word ingredients
                    set(cur_product_split).intersection(
                        set(basic_ing_murder+basic_ing_beverage+basic_ing_dairy+basic_ing_fruit+basic_ing_grains+basic_ing_meat_fish+\
              basic_ing_pastry+basic_ing_sauce+basic_ing_seasoning+basic_ing_sweet+basic_ing_vegetable))
                )

        db.set_value(idx,'fix_ingredients',cur_ingredients)

def add_veg(db):
    db['vegetarian'] = pd.Series(True * (len(db['time'])), index=db.index).astype(bool)
    db['vegan'] = pd.Series(True * (len(db['time'])), index=db.index).astype(bool)
    db['gluten_safe'] = pd.Series(True * (len(db['time'])), index=db.index).astype(bool)

    for idx in range(len(db)):
        if set(db.fix_ingredients[idx]).intersection(set(basic_ing_meat_fish)):
            db.vegetarian[idx] = False
            db.vegan[idx] = False
        elif set(db.fix_ingredients[idx]).intersection(set(basic_ing_dairy+basic_ing_murder)): db.vegan[idx] = False
        if set(db.fix_ingredients[idx]).intersection(set(basic_ing_grains+basic_ing_pastry)): db.gluten_safe[idx] = False


    return db

def return_recipes(db,kitchen,sort_by,filters,amount):
    ''' sort_by: m (match), t (time)
        filter:  vegetarian , vegan, gluten_safe  '''
    for i in range(len(db.fix_ingredients)):
        inter = set(kitchen).intersection(set(db.fix_ingredients[i]))
        db.match[i] = sum([grade_basic_ing[p] for p in inter])

    f_db = db
    for filter in filters:
        f_db = f_db[f_db[filter] == True]

    if sort_by == 'm': f_db = f_db.sort(['match'], ascending=[False])
    elif sort_by == 'mt': f_db = f_db.sort(['match', 'time'], ascending=[False, True])

    return f_db[0:amount]

def df_to_format(f_db):
    # {"recepies":[{"title":"hamburger","image":"http://www.mediterran-leben.com/wp-content/uploads/2012/09/Spaghetti-Bolognese-1.jpg","link":"https://www.yahoo.com/"}
    # ,{"title":"pizza","image":"http://i.imgur.com/MwBKTI8.jpg","link":"https://www.facebook.com/"}]}
    ret = '{"recepies":['
    for i in f_db.index:
        ret += '{"title":"' + str(f_db.name[i]) + '","image":"' + str(f_db.image[i]) + '","link":"' + str(f_db.url[i]) + '"},'
    ret = ret[:-1] + ']}'

    return(ret)

def list_to_format(l):
    # ['egg' , 'eggplant']  ->  "{\\\"ingredients\\\": [\\\"egg\\\", \\\"eggplant\\\" ]}"
    ret = '{\\\"ingredients\\\": ['
    for i in l[:-1]:
        ret += '\\\"' + str(i) + '\\\", '
    ret += '\\\"' +  str(l[-1]) + '\\\" ]}'

    return ret

def create_pickle():
    # db = json_to_pandas('./test.json')
    db = json_to_pandas('./recipeitems-latest.json')
    db = drop_useless_columns(db)
    db = split_ingredients(db)
    clean_ingredients(db)
    db = add_veg(db)
    # pickle.dump(db, open('test.p','wb'))
    pickle.dump(db, open('full_dump.p','wb'))


if __name__ == "__main__":
    create_pickle()
    # db = pickle.load( open('full_dump.p','rb') )
    # db = pickle.load( open('test.p','rb') )