from django.test import TestCase
from django.contrib.auth.models import Group
from apps.staff.models import Staff, StaffRole
from apps.staff.forms import StaffAdminForm

class StaffFormTest(TestCase):
    def test_staff_creation_hashes_password(self):
        form_data = {
            "username": "teststaff",
            "first_name": "Test",
            "last_name": "Staff",
            "email": "test@example.com",
            "password": "securepassword123",
            "role": StaffRole.TEACHER,
            "is_active": True,
            "phone": "1234567890",
            "address": "123 Street",
        }
        form = StaffAdminForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        staff = form.save()
        
        self.assertEqual(staff.username, "teststaff")
        self.assertTrue(staff.check_password("securepassword123"))
        self.assertNotEqual(staff.password, "securepassword123") # Hashed

    def test_staff_update_can_change_password(self):
        staff = Staff.objects.create_user(
            username="oldstaff",
            password="oldpassword",
            role=StaffRole.SALES
        )
        form_data = {
            "username": "oldstaff",
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@example.com",
            "password": "newpassword456",
            "role": StaffRole.SALES,
            "is_active": True,
            "phone": "0987654321",
            "address": "456 Avenue",
        }
        form = StaffAdminForm(data=form_data, instance=staff)
        self.assertTrue(form.is_valid(), form.errors)
        updated_staff = form.save()
        
        self.assertTrue(updated_staff.check_password("newpassword456"))
        self.assertFalse(updated_staff.check_password("oldpassword"))

    def test_staff_update_without_password_keeps_old_one(self):
        staff = Staff.objects.create_user(
            username="steady",
            password="steady-password",
            role=StaffRole.ADMIN
        )
        old_hash = staff.password
        form_data = {
            "username": "steady",
            "first_name": "Still",
            "last_name": "Steady",
            "email": "steady@example.com",
            "password": "", # Blank password
            "role": StaffRole.ADMIN,
            "is_active": True,
            "phone": "5555555",
            "address": "Steady Home",
        }
        form = StaffAdminForm(data=form_data, instance=staff)
        self.assertTrue(form.is_valid(), form.errors)
        updated_staff = form.save()
        
        self.assertEqual(updated_staff.password, old_hash)
        self.assertTrue(updated_staff.check_password("steady-password"))
