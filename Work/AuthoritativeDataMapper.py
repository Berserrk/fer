AuthoritativeDataMapper.use_koalas()
data_repo = AuthoritativeDataMapper.map_data(
    raw_repo,
    technical_config.exec_config,
    partner_ids_in_scope,
    partner_ids_out_of_scope
)
data_repo.partner_scope = {'IN': partner_ids_in_scope, 'OUT': partner_ids_out_of_scope}
data_repo.prepare_data()

model = Review(technical_config.exec_config)
model._data = data_repo
model._indicators = IndicatorsRepo(model._data)
model._scenarios = ScenariosRepo(model._indicators)

model._checks = DataChecker(data_repo)
model._checks.complete_check()

model.evaluate_modules()


def process_data_and_evaluate_model(raw_repo, technical_config, partner_ids_in_scope, partner_ids_out_of_scope):
    AuthoritativeDataMapper.use_koalas()
    data_repo = AuthoritativeDataMapper.map_data(
        raw_repo,
        technical_config.exec_config,
        partner_ids_in_scope,
        partner_ids_out_of_scope
    )
    data_repo.partner_scope = {'IN': partner_ids_in_scope, 'OUT': partner_ids_out_of_scope}
    data_repo.prepare_data()

    model = Review(technical_config.exec_config)
    model._data = data_repo
    model._indicators = IndicatorsRepo(model._data)
    model._scenarios = ScenariosRepo(model._indicators)

    model._checks = DataChecker(data_repo)
    model._checks.complete_check()

    model.evaluate_modules()

    return model