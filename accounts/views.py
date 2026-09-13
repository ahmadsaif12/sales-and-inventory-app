from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from django.views.generic import(
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
#third party package imports
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

from .models import Profile, Customer, Vendor
from .forms import(
    CreateUserForm, UserUpdateForm,
    ProfileUpdateForm,CustomerForm,
    VendorForm
)
from .tables import ProfileTable

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    else:
        form = CreateUserForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile_update.html', {'u_form': u_form, 'p_form': p_form})

class ProfileListView(LoginRequiredMixin, ExportMixin, SingleTableView):
    model = Profile
    template_name = 'accounts/stafflist.html'
    context_object_name = 'profiles'
    table_class = ProfileTable
    table_pagination = False

class ProfileCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Profile
    template_name = 'accounts/staffcreate.html'
    fields = ['user', 'role', 'status']

    def get_success_url(self):
        return reverse('profile_list')

    def test_func(self):
        return self.request.user.is_superuser

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'accounts/staffupdate.html'
    fields = ['user', 'role', 'status']

    def get_success_url(self):
        return reverse('profile_list')

    def test_func(self):
        return self.request.user.is_superuser

class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/staff_delete.html'

    def get_success_url(self):
        return reverse('profile_list')

    def test_func(self):
        return self.request.user.is_superuser

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'accounts/customer_list.html'
    context_object_name = 'customers'

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'accounts/customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'accounts/customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')

class CustomerDeleteView(LoginRequiredMixin,DeleteView):
    model = Customer
    template_name = 'accounts/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@csrf_exempt
@require_POST
@login_required
def get_customers(request):
    # Check if the request was made using AJAX
    if is_ajax(request):
        # Get the search text entered by the user
        term = request.POST.get('term', '')

        # Find customers whose name contains the search text
        customers = Customer.objects.filter(
            name__icontains=term
        ).values('id', 'name')

        # Convert the query results to a list
        customer_list = list(customers)

        # Send the customer list back as JSON
        return JsonResponse(customer_list, safe=False)

    # Return an error if the request is not AJAX
    return JsonResponse({'error': 'Invalid request'}, status=400)

class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = 'accounts/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 10

class VendorCreateView(LoginRequiredMixin, CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'accounts/vendor_form.html'
    success_url = reverse_lazy('vendor-list')

class VendorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'accounts/vendor_form.html'
    success_url = reverse_lazy('vendor-list')

class VendorDeleteView(LoginRequiredMixin, DeleteView):
    model = Vendor
    template_name = 'accounts/vendor_confirm_delete.html'
    success_url = reverse_lazy('vendor-list')