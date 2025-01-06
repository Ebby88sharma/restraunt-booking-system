from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def manage_tables(request):
    # Admin-only logic for managing tables
    pass
