from django import template
from webApp.models import *
import json

register = template.Library() 
@register.filter(name='get_item')
def get_item(dictionary, key):    
    value_id = dictionary.get(str(key))

    item_instance = Menuitems.objects.filter(pk = value_id).first()

        
    return item_instance.title
    





@register.filter(name='get_description')
def get_description(dictionary, key):    
    value_id = dictionary.get(str(key))
    item_instance = Menuitems.objects.filter(pk = value_id).first()
    
    return item_instance.description



@register.filter(name='condition_check')
def condition_check(dictionary, key):
    
    return dictionary.get(str(key))









# def some_condition_based_on_menu_items(dictionary, key,menu_id):

#     value_id = dictionary.get(str(key))
#     if Menuitems.objects.filter(pk = value_id).exists():
#         flag = True
        
#         return flag
#     else:
#         menu_instance = Menu.objects.filter(id = menu_id).first()
#         menu_items = json.decoder.JSONDecoder().decode(menu_instance.associated_items)
#         value = None
#         menu_items[str(key)] = str(value)
#         menu_instance.associated_items = json.dumps(menu_items)
#         menu_instance.save()
#         flag = False

#         return flag




# @register.filter
# def condition_check_items_in_system(menu_items, args):
    
#     counter, menu_id = args
    
#     return some_condition_based_on_menu_items(menu_items, counter, menu_id)




@register.filter(name='condition_check_items_in_system')
def condition_check_items_in_system(dictionary, key):

    value_id = dictionary.get(str(key))
    if Menuitems.objects.filter(pk = value_id).exists():
        flag = True
        
        return flag
    else:
        # menu_instance = Menu.objects.filter(id = menu_id).first()
        # menu_items = json.decoder.JSONDecoder().decode(menu_instance.associated_items)
        # value = None
        # menu_items[str(key)] = str(value)
        # menu_instance.associated_items = json.dumps(menu_items)
        # menu_instance.save()
        flag = False

        return flag
    

@register.filter(name='check_group_id')
def check_group_id(user_id):

    user = User.objects.get(id=user_id)
    if user.groups.exists() :
        group_id = user.groups.first().id
    else: 
        None

        
    return group_id
    

    



@register.filter(name='approved_owner_check')
def approved_owner_check(user_id): 
    return  Kitchen.objects.filter(approved_owner_id=user_id).exists()
 

        
    