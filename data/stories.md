## success all queries in one go no nonsense part 1 plus round 2 of querying
* greet
  - utter_greet
* search_provider
  - pincode_category_form
  - form{"name": "pincode_category_form"}
  - form{"name": null}
  - utter_did_that_help
* affirm
  - utter_ask_round_two
* round_two
  - action_deactivate_form
  - utter_happy
  - utter_ask_same_pincode
* confirm
  - action_for_same_pincode
  - utter_ask_same_category
* confirm
  - action_for_same_category
  - pincode_category_form
  - form{"name": "pincode_category_form"}
  - form{"name": null}

## success all queries in one go plus explicit no round 2 of querying
* greet
  - utter_greet
* search_provider
  - pincode_category_form
  - form{"name": "pincode_category_form"}
  - form{"name": null}
  - utter_did_that_help
* affirm
  - utter_ask_round_two
* deny
  - action_deactivate_form
  - utter_goodbye

## success all queries in one go no implicit no round 2 of querying
* greet
  - utter_greet
* search_provider
  - pincode_category_form
  - form{"name": "pincode_category_form"}
  - form{"name": null}
  - utter_did_that_help
* goodbye
  - action_deactivate_form
  - utter_goodbye

## success all queries iteratively explicit no round 2 of querying
* greet
  - utter_greet
* affirm
  - pincode_category_form
  - form{"name": "pincode_category_form"}
  - form{"name": null}
  - utter_did_that_help
* affirm
  - utter_ask_round_two
* deny
  - action_deactivate_form
  - utter_goodbye

## success all queries iteratively plus round 2 of querying
* greet
  - utter_greet
* affirm
  - pincode_category_form
  - form{"name": "pincode_category_form"}
  - form{"name": null}
  - utter_did_that_help
* affirm
  - utter_ask_round_two
* round_two
  - action_deactivate_form
  - utter_happy
  - utter_ask_same_pincode
* confirm
  - action_for_same_pincode
  - utter_ask_same_category
* confirm
  - action_for_same_category
  - pincode_category_form
  - form{"name": "pincode_category_form"}
  - form{"name": null}

## failure queries when iteratively asking for ip
* greet
  - utter_greet
* affirm
  - pincode_category_form
  - form{"name": "pincode_category_form"}
* out_of_scope:
  - action_deactivate_form
  - form{"name": null}
  - utter_goodbye

## failure queries when ip asked all at once
* greet
  - utter_greet
* search_provider
  - pincode_category_form
  - form{"name": "pincode_category_form"}
* out_of_scope:
  - action_deactivate_form
  - form{"name": null}
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
