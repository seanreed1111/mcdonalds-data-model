

- Takes customer orders for McDonald's menu items
- Searches and validates items against a real McDonald's menu
- Handles item modifiers (with bacon)
- Confirms each item as it's added
- Reads back the complete order
- Saves orders as JSON files for processing

### How It Works


  - `Menu` - Complete menu with categories
  - `Item` - Individual menu item with modifiers
  - `Modifier` - Item variations (e.g., "Extra Cheese", "No Tomatos")

Categories include:
- Breakfast
- Beef & Pork
- Chicken & Fish
- Snacks & Sides
- Beverages
- Coffee & Tea
- Desserts
- Smoothies & Shakes

- Default size is medium for all drinks. If customer asks for different size they can get it.

Size should be an strenum
Category, Item, Modifier, Combo, Menu are all pydantic v2 models
Category: category_id, name
Item: item_id, name, category_name, size, default_size, quantity
Combo: combo_id, list[Item]
Modifier: modifier_id, name, restrictions: list[Category]
Menu: name,  allowed_categories: list[Category]