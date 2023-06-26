from config.settings import PROJECT_NAME_BY_DEFAULT


def get_name(user):
    name = f'Проект{user.rooms.count()}'
    all_names = user.rooms.values_list('name', flat=True)
    if name in all_names:
        new_number = max(all_names, key=lambda value: int(value[len(PROJECT_NAME_BY_DEFAULT) :]))
        return f'Проект{int(new_number[len(PROJECT_NAME_BY_DEFAULT) :]) + 1}'
    else:
        return name
