def cleanup_social_account(backend, uid, user=None, *args, **kwargs):
    print(kwargs)
    if user.first_name == "":
        user.first_name = kwargs["details"]["username"]
        user.save()
    return {
        "user": user,
    }
