from conversations.tree_classes import (
    Node,
    ConditionalNode,
    ConversationTree,
    get_all_nodes,
)
from conversations.tree_callbacks import *

### sign in flow
signing_in = ConditionalNode(
    "sign in initiate",
    "sign.{0,4} in.{0,2}",
    sign_in_init,
    isEntry=True,
    isPublic=True,
    isReply=False,
)

signing_out = ConditionalNode(
    "sign out initiate",
    "sign.{0,4} out.{0,2}",
    sign_in_init,
    isEntry=True,
    isPublic=True,
    isReply=False,
)

# optional status
work_at_home = Node(
    "work at home", "Home", add_optional_status, isEntry=True
).set_parents([signing_in])
work_at_office = Node(
    "work at office", "Office", add_optional_status, isEntry=True
).set_parents([signing_in])
business_trip = Node(
    "on business trip", "Business Trip", add_optional_status, isEntry=True
).set_parents([signing_in])
optional_status = [work_at_home, work_at_office, business_trip]
# Over write flow
rewrite = Node("check rewrite", "Rewrite the log", check_rewrite_log, isEntry=True)
confirm_rewrite = (
    Node("confirm rewrite", "Yes, I delete and write again", rewrite_log)
    .set_parents([rewrite])
    .set_children(optional_status)
)
cancel = Node("cancel", "Cancel", cancel).set_parents([rewrite])

# ask reason
ask_reason = Node("Ask reason", "Yes. I text you the reason", ask_reason, isEntry=True)
receive_reason = (
    Node("Receved reason", "text", receive_reason, inputType="text")
    .set_parents([ask_reason])
    .set_children(optional_status)
)

# connect
signing_in.set_condtional_children(
    {
        "new": optional_status,
        "duplicated": [rewrite, cancel],
        "late": [ask_reason],
    }
)

signing_out.set_condtional_children(
    {
        "new": optional_status,
        "duplicated": [rewrite, cancel],
        "late": [ask_reason],
    }
)

# location
location = ConditionalNode(
    "location", "location", add_location, inputType="location"
).set_parents(optional_status)
not_available = ConditionalNode(
    "location Not available", "Not Available", add_location
).set_parents(optional_status)

# Confirmation
confirm = Node("confirmation", "Confirm", confirm_log).set_parents([location])
edit = (
    Node("Go back", "Go back", lambda x, y: {"message": "Where do you work?"})
    .set_parents([location])
    .set_children(optional_status)
)

# Ask content
asking_content = Node(
    "Report content", "Send content of today", ask_content
).set_parents([location])
ask_content_confirmation = Node(
    "receve content", "text", confirm_content, inputType="text"
).set_parents([asking_content])
save_content = (
    Node("save content", "Save content", save_content)
    .set_parents([ask_content_confirmation])
    .set_children([confirm, edit])
)
content_edited = (
    Node("edit content", "Edit content", ask_content)
    .set_parents([ask_content_confirmation])
    .set_children([confirm, edit])
)

# update location
location.set_condtional_children(
    {
        "done": [confirm, edit],
        "content": [asking_content, edit],
    }
)

not_available.set_condtional_children(
    {
        "done": [confirm, edit],
        "content": [asking_content, edit],
    }
)
# create tree
sign_in_tree = ConversationTree(signing_in)
sign_out_tree = ConversationTree(signing_out)
sign_in_tree.get_graph("telegram_bot/diagrams/tree_sign_in.wsd")