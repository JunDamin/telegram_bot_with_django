from conversations.tree_classes import (
    Node,
    ConditionalNode,
    ConversationTree,
    get_all_nodes,
)
from conversations.tree_callbacks import *

### sign in flow
sign_in_init = ConditionalNode(
    "sign in initiate",
    "sign.{0,4} in.{0,2}",
    sign_in_init,
    isEntry=True,
    isPublic=True,
    isReply=False,
)

# optional status
work_at_home = Node(
    "work at home", "Home", add_optional_status, isEntry=True
).set_parents([sign_in_init])
work_at_office = Node(
    "work at office", "Office", add_optional_status, isEntry=True
).set_parents([sign_in_init])
business_trip = Node(
    "on business trip", "Business Trip", add_optional_status, isEntry=True
).set_parents([sign_in_init])

# Over write flow
rewrite = Node("check rewrite", "Rewrite the log", check_rewrite_log, isEntry=True)
confirm_rewrite = (
    Node("confirm rewrite", "Yes, I delete and write again", rewrite_log)
    .set_parents([rewrite])
    .set_children([work_at_home, work_at_office, business_trip])
)
cancel = Node("cancel", "Cancel", cancel).set_parents([rewrite])

# ask reason
ask_reason = Node("Ask reason", "Yes. I text you the reason", ask_reason, isEntry=True)
receive_reason = (
    Node("Receved reason", "text", receive_reason, inputType="text")
    .set_parents([ask_reason])
    .set_children([work_at_home, work_at_office, business_trip])
)

# connect
sign_in_init.set_condtional_children(
    {
        "new": [work_at_home, work_at_office, business_trip],
        "duplicated": [rewrite, cancel],
        "late": [ask_reason],
    }
)

# location
location = Node("location", "location", add_location, inputType="location")
for i in [work_at_home, work_at_office, business_trip]:
    i.children = [location]
# Confirmation
confirm = Node("confirmation", "Confirm", confirm_log).set_parents([location])
edit = (
    Node("Go back", "Go back", lambda x, y: {"message": "Where do you work?"})
    .set_parents([location])
    .set_children([work_at_home, work_at_office, business_trip])
)

#
sign_in_tree = ConversationTree(sign_in_init)

conversations = [sign_in_tree.get_conversation()]

sign_in_tree.get_graph("telegram_bot/diagrams/tree_sign_in.wsd")
