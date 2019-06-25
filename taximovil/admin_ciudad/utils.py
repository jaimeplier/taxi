
def is_callcenter_owner(User, Callcenter):
    if Callcenter.sitio.admin_ciudad.pk == User.pk:
        return True
    else:
        return False
