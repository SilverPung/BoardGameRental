from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.views import PasswordChangeView
from .forms import UserForm, CustomPasswordChangeForm
# Create your views here.


@login_required
def profile(request):
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('core:home')
    else:
        user_form = UserForm(instance=request.user)

    return render(request, 'account/profile.html', {'form': user_form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'account/password_change.html'
    form_class = CustomPasswordChangeForm

    def get_success_url(self):
        return reverse('core:home')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)