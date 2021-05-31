from conversations.tree_classes import (
    Node,
    ConditionalNode,
    ConversationTree,
    get_all_nodes,
)
from conversations.tree_callbacks import *

### sign in flow
sign_in_init = ConditionalNode("sign in initiate", "sign.{0,4} in.{0,2}", create_log, isEntry=True)

# optional status
work_at_home = Node("work at home", "Home", add_optional_status)
work_at_office = Node("work at office", "Office", add_optional_status)
business_trip = Node("on business trip", "Business Trip", add_optional_status)

# Over write flow
rewrite = Node("check rewrite", "Rewrite the log", check_rewrite_log)
cancel = Node("cancel", "Cancel", cancel)
confirm_rewrite = Node("", "Yes, I delete and write again", rewrite_log)
rewrite.children = [confirm_rewrite, cancel]
confirm_rewrite.children = [work_at_home, work_at_office, business_trip]
# connect
sign_in_init.set_condtional_children(
    {
        "new": [work_at_home, work_at_office, business_trip],
        "duplicated": [rewrite, cancel],
    }
)

# location
location = Node("location", "location", add_location)
for i in [work_at_home, work_at_office, business_trip]:
    i.children = [location]
# Confirmation
confirm = Node("confirmation", "Confirm", confirm_log)
edit = Node(
    "back to edit",
    "Edit",
    lambda x, y: {"message": "Where do you work?"},
    [work_at_home, work_at_office, business_trip],
)
location.children = [confirm, edit]

#
sign_in_tree = ConversationTree(sign_in_init)

conversations = [sign_in_tree.get_conversation()]

sign_in_tree.get_graph("telegram_bot/diagrams/tree_sign_in.wsd")
