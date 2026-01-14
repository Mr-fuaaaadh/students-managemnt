from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from .models import Staff


UNFOLD_INPUT = {
    "class": "w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
}


class TogglePasswordInput(forms.PasswordInput):
    template_name = "django/forms/widgets/password.html"

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        toggle_html = (
            '<button type="button" onclick="const p=this.previousElementSibling; p.type=p.type===\'password\'?\'text\':\'password\';" '
            'style="margin-left:-40px; background:none; border:none; cursor:pointer; color:#4f46e5; font-size:12px; font-weight:600; vertical-align:middle;">'
            'Show/Hide</button>'
        )
        return mark_safe(
            f'<div style="display:flex; align-items:center;">{html}{toggle_html}</div>'
        )


class StaffAdminForm(forms.ModelForm):
    # User fields
    username = forms.CharField(
        widget=forms.TextInput(attrs={**UNFOLD_INPUT, "placeholder": "Username"})
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**UNFOLD_INPUT, "placeholder": "First name"})
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**UNFOLD_INPUT, "placeholder": "Last name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={**UNFOLD_INPUT, "placeholder": "Email"})
    )
    password = forms.CharField(
        required=False,
        widget=TogglePasswordInput(
            render_value=False,
            attrs={**UNFOLD_INPUT, "placeholder": "Password (leave blank to keep current)"}
        )
    )

    class Meta:
        model = Staff
        fields = ("role", "is_active", "phone", "address")
        widgets = {
            "role": forms.Select(attrs=UNFOLD_INPUT),
            "phone": forms.TextInput(attrs={**UNFOLD_INPUT, "placeholder": "Phone"}),
            "address": forms.Textarea(
                attrs={**UNFOLD_INPUT, "rows": 3}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "toggle"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")

        allowed_domain = "@corusinfo.com"
        if not email.lower().endswith(allowed_domain):
            raise forms.ValidationError(
                "Only corusinfo.com email addresses are allowed."
            )

        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["username"].initial = self.instance.username
            self.fields["first_name"].initial = self.instance.first_name
            self.fields["last_name"].initial = self.instance.last_name
            self.fields["email"].initial = self.instance.email
            self.fields["password"].required = False

    def save(self, commit=True):
        staff = super().save(commit=False)
        
        # Update user fields directly on the Staff instance
        staff.username = self.cleaned_data["username"]
        staff.first_name = self.cleaned_data.get("first_name", "")
        staff.last_name = self.cleaned_data.get("last_name", "")
        staff.email = self.cleaned_data["email"]

        password = self.cleaned_data.get("password")
        if password:
            staff.set_password(password)

        if commit:
            staff.save()
        return staff
