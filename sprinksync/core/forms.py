from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'contractor',
            'design_deadline',
            'install_date',
            'end_date',
            'est_Labor_hours',
            'est_design_hours',
            'est_material_cost',
            'true_Labor_hours',
            'true_design_hours',
            'true_material_cost'
        ]
