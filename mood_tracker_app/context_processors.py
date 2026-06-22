from login_app.models import User

def user_info(request):
    if 'user_id' in request.session:
        try:
            user = User.objects.get(id=request.session['user_id'])
            first_name = user.first_name
            last_name = user.last_name
            
            first_letter = first_name[0].upper() if first_name else ''
            last_letter = last_name[0].upper() if last_name else ''
            initials = f"{first_letter}{last_letter}"
            
            if not initials:
                initials = 'U'

            return {
                'username': first_name,
                'initials': initials,
            }
        except User.DoesNotExist:
            pass
    
    return {'username': 'Guest', 'initials': 'G'}