from django.shortcuts import render
from webApp.models import *

def  Home(request):
    # chks = Menuitems.objects.create(
    #     title =  "Fried Rice w Tandoori",
    #     description =  "new iteems",
    #     parent_menu_id =  3,
    #     subdivision_id= 999
    # )
    # chks.save()
    menus_categories = MenuCategory.objects.all() #.exclude(pk=2)
    return render(request,'Demo/demo.html',{'menus_categories':menus_categories})


def  Homec(request):
    # chks = Menuitems.objects.create(
    #     title =  "Fried Rice w Tandoori",
    #     description =  "new iteems",
    #     parent_menu_id =  3,
    #     subdivision_id= 999
    # )
    # chks.save()
    menus_categories = MenuCategory.objects.all() #.exclude(pk=2)
    return render(request,'Demo/demo.html',{'menus_categories':menus_categories})



def  Homecf(request):
    # chks = Menuitems.objects.create(
    #     title =  "Fried Rice w Tandoori",
    #     description =  "new iteems",
    #     parent_menu_id =  3,
    #     subdivision_id= 999
    # )
    # chks.save()
    menus_categories = MenuCategory.objects.all()[:1] #.exclude(pk=2)
    return render(request,'Demo/demo.html',{'menus_categories':menus_categories})



# from django.core.paginator import Paginator
# def  Users_Suggestions(request):
#     if UsersSuggestions.objects.exists():
#         p = Paginator(UsersSuggestions.objects.all().order_by('-id'),2)
#         page = request.GET.get('page')
#         ven = p.get_page(page) 
#         context = {'ven':ven}
#     else:
#         context = {'ven':False}
#     return render(request,'Demo/userssuggestions.html',context=context)


from django.http import JsonResponse
def   DeleteQuiz(request):
    quiz_id = request.GET.get("quiz_id") 
    print("quiz_id",quiz_id)
    return JsonResponse({'success':True})