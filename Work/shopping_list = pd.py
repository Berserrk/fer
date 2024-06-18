shopping_list = pd.Series(list(raw_repo.df_pich.PARTNER_ID.unique()), name='PARTNER_ID')
raw_repo.load_shopping_list_info(date=technical_config.exec_config.CALCULATION_DATE, partner_ids=shopping_list)

partner_ids_in_scope, partner_ids_out_of_scope = shopping_list_processing.apply_include_exclude_rules(raw_repo.df_shopping_list_info)

partner_ids_in_scope = partner_ids_in_scope.drop_duplicates()
partner_ids_out_of_scope = partner_ids_out_of_scope.drop_duplicates()

partner_id_in_scope = partner_ids_in_scope[~partner_ids_in_scope.isin(partner_ids_out_of_scope)]

scope_ids = list(partner_id_in_scope) + list(partner_ids_out_of_scope)
legal_entities_and_old_clients = []
for id in shopping_list:
    if id in scope_ids:
        legal_entities_and_old_clients.append(id)
for id in not_anymore_clients:
    legal_entities_and_old_clients.append(id)
tmp = pd.Series(legal_entities_and_old_clients)
partner_ids_out_of_scope = pd.concat([partner_ids_out_of_scope, tmp])

logging.info(f'IN SCOPE POP: {len(partner_id_in_scope)}')
logging.info(f'OUT OF SCOPE POP: {len(partner_ids_out_of_scope)}')



def process_shopping_list(raw_repo, shopping_list_processing, technical_config, not_anymore_clients):
    shopping_list = pd.Series(list(raw_repo.df_pich.PARTNER_ID.unique()), name='PARTNER_ID')
    raw_repo.load_shopping_list_info(date=technical_config.exec_config.CALCULATION_DATE, partner_ids=shopping_list)

    partner_ids_in_scope, partner_ids_out_of_scope = shopping_list_processing.apply_include_exclude_rules(raw_repo.df_shopping_list_info)

    partner_ids_in_scope = partner_ids_in_scope.drop_duplicates()
    partner_ids_out_of_scope = partner_ids_out_of_scope.drop_duplicates()

    partner_id_in_scope = partner_ids_in_scope[~partner_ids_in_scope.isin(partner_ids_out_of_scope)]

    scope_ids = list(partner_id_in_scope) + list(partner_ids_out_of_scope)
    legal_entities_and_old_clients = [id for id in shopping_list if id in scope_ids] + list(not_anymore_clients)
    
    partner_ids_out_of_scope = pd.concat([partner_ids_out_of_scope, pd.Series(legal_entities_and_old_clients)])

    logging.info(f'IN SCOPE POP: {len(partner_id_in_scope)}')
    logging.info(f'OUT OF SCOPE POP: {len(partner_ids_out_of_scope)}')

    return partner_id_in_scope, partner_ids_out_of_scope