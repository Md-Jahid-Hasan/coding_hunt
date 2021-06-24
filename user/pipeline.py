
def create_user(strategy, details, backend, user=None, *args, **kwargs):
    USER_FIELDS = ['name', 'email', 'picture']

    if user:
        strategy.request.session['email'] = user.email
        return {'is_new': False}
    fields = dict((name, kwargs['response'].get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))

    if not fields:
        return
    fields['is_active'] = False
    strategy.request.session['email'] = fields['email']

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }
