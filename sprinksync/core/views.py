from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Project, Company, CustomUser
from .forms import ProjectForm


def landing_page(request):
    return render(request, 'core/landing.html')

# Company Sign-Up (Creates Company + Admin User)
def company_signup(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        company = Company.objects.create(name=company_name)
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            role='admin',
            company=company
        )
        login(request, user)
        return redirect('dashboard')  # redirect to dashboard or project list

    return render(request, 'core/company_signup.html')

# Admin: Add User to Company
@login_required
def add_user(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("You do not have permission to add users.")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            company=request.user.company,
            role=role
        )
        return redirect('dashboard')  # You can update this to a dashboard or user view

    return render(request, 'core/add_user.html')

#Dashboard
def dashboard(request):
    return render(request, 'core/dashboard.html')  # ✅ path must match folder



# List View - Display All Projects for the Logged-in User's Company
@login_required
def project_list(request):
    projects = Project.objects.filter(company=request.user.company)
    return render(request, 'core/project_list.html', {'projects': projects})

# Detail View - Display Single Project (Scoped to Company)
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, company=request.user.company)
    return render(request, 'core/project_detail.html', {'project': project})

# Create View - Add New Project
@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.company = request.user.company
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'core/project_form.html', {'form': form})

# Edit View - Update Project (Scoped to Company)
@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, company=request.user.company)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/project_form.html', {'form': form})

# Delete View - Delete Project (Scoped to Company)
@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, company=request.user.company)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'core/project_confirm_delete.html', {'project': project})
