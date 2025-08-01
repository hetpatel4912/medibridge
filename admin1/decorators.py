from django.http import HttpResponse
def only_admin(func):
 
    # inner1 is a Wrapper function in 
    # which the argument is called
     
    # inner function can access the outer local
    # functions like in this case "func"
    def inner1(request, *args, **kwargs):
        role = request.session.get('role')
        print("dfs : ", role, type(role))
        if role != 1:
            return HttpResponse('not allowed')
        return func(request, *args, **kwargs)         
    return inner1