from users.forms import LoginForm


def get_context_data(request):
    context = {
        "login_ajax": LoginForm()
    }
    return context
