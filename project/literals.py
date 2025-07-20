class ProjectLiterals:
    max_length_project_name: int = 64
    project_name_by_default: str = "Проект"
    projects_verbose_name_plural: str = "Проекты"
    project_name_verbose_name: str = "Название проекта"
    project_draft_verbose_name: str = "Черновик"
    project_updated_at_verbose_name: str = "Дата обновления"
    project_created_at_verbose_name: str = "Дата создания"
    project_layout_requests_left_verbose_name: str = "Количество запросов на макет"
    project_layout_requests_left_max_value: int = 4
    project_layout_requests_left_min_value: int = 0
    project_layout_requests_left_min_value_message: str = (
        "Количество запросов на макет не может быть меньше "
        f"{project_layout_requests_left_min_value}"
    )
    project_layout_requests_left_max_value_message: str = (
        "Количество запросов на макет не может быть больше "
        f"{project_layout_requests_left_max_value}"
    )
    project_preferred_layout_verbose_name: str = "Предпочитаемый макет"
    project_str_output: str = "Создан проект '{}' для пользователя {} с id {}"


project_literals = ProjectLiterals()
