from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    environments=False,
    load_dotenv=False,
    settings_files=['settings.toml'],

    validators=[
        Validator('dim_x', must_exist=True, gt=0, is_type_of=int),
        Validator('dim_y', must_exist=True, gt=0, is_type_of=int),

        Validator('input_interface', must_exist=True, is_in=['Keyboard', 'MLInput', 'RandomInput']),
        Validator('output_interface', must_exist=True, is_in=['Text', 'Pygame']),

        Validator('time_step_seconds', when=Validator('input_interface', eq='Keyboard'), must_exist=True, gte=0,
                  is_type_of=float),
    ]
)





