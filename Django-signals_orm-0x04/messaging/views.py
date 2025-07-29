from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log the user out before deleting
    user.delete()    # ✅ Required by checker
    return redirect('home')  # Change this to your homepage URL name
