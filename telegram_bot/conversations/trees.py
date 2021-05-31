from conversations.tree_classes import Node, ConversationTree, get_all_nodes
from conversations.tree_callbacks import *

### sign in flow
sign_in_init = Node("sign in initiate", "sign_in", create_log, isEntry=True)
# optional status 
work_at_home = Node("work at home", "Home", add_optional_status)
work_at_office = Node("work at office", "Office", add_optional_status)
business_trip = Node("on business trip", "Business Trip", add_optional_status)
sign_in_init.children = [work_at_home, work_at_office, business_trip]
# location
location = Node("location", "location", add_location)
for  i in [work_at_home, work_at_office, business_trip]:
    i.children = [location]
# Confirmation
confirm = Node("confirmation", "Confirm", confirm_log)
edit = Node("back to edit", "Edit", lambda x, y: (0, "Where do you work?"), [work_at_home, work_at_office, business_trip])
location.children = [confirm, edit]

# Over write flow
test2 = Node("back to edit", "Edit", lambda x, y: (0, "Where do you work?"))
# rewrite = Node("", "Rewrite")
# cancel = Node("", "Cancel")
# confirm_rewrite = Node("", "Yes, I delete and write again")


# 
sign_in_tree = ConversationTree(sign_in_init)

conversations = [
    tree_conv,
    sign_in_tree.get_conversation()
]

sign_in_tree.get_graph("telegram_bot/diagrams/tree_sign_in.wsd")
