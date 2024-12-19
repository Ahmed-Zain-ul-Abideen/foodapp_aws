from django.shortcuts import render,redirect  
from webApp.templatetags.webApp_extras import user_role


def Index(request):
    if not request.user.is_authenticated:
      return redirect('login-dashboard')
    chk = user_role(request.user) 


    print(chk)
    if len(chk) == 0:
      return redirect('login-dashboard')  
    # elif len(chk) == 1:
    #   return render(request, 'dashboard/permission_denied_updt.html')
    

    else: 
      context= {}
      return render(request, 'dashboard/Home_Page/index.html', context)
    