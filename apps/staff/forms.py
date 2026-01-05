from django import forms
from django.contrib.auth.models import User
from .models import Staff


UNFOLD_INPUT = {
    "class": "w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
}


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
        widget=forms.PasswordInput(
            render_value=True,
            attrs={**UNFOLD_INPUT, "placeholder": "Password"}
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

    def save(self, commit=True):
        staff = super().save(commit=False)

        if not staff.pk:
            user = User.objects.create_user(
                username=self.cleaned_data["username"],
                first_name=self.cleaned_data.get("first_name", ""),
                last_name=self.cleaned_data.get("last_name", ""),
                email=self.cleaned_data["email"],
                password=self.cleaned_data["password"],
            )
            staff.user = user

        if commit:
            staff.save()

        return staff
