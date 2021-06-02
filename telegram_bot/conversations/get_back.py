from conversations.tree_classes import (
    Node,
    ConditionalNode,
    ConversationTree,
)
from conversations.tree_callbacks import *



# getting back
getting_back = ConditionalNode(
    "getting back",
    "back from break.?|back to work.?|lunch over.?|break over.?",
    sign_in_init,
    isEntry=True,
    isPublic=True,
    isReply=False,
)

with_koica = (
    Node("lunch_with_koica", "With KOICA Colleagues", add_optional_status, isEntry=True)
    .set_parents([getting_back])
)

without_koica = (
    Node(
        "lunch wihtout koica",
        "Without any member of KOICA",
        add_optional_status,
        isEntry=True,
    )
    .set_parents([getting_back])
)

lunch_options = [with_koica, without_koica]

# location
location = ConditionalNode(
    "location", "location", add_location, inputType="location"
).set_parents(lunch_options)
not_available = ConditionalNode(
    "location Not available", "Not Available", add_location
).set_parents(lunch_options)

# Confirmation
confirm = Node("confirmation", "Confirm", confirm_log).set_parents([location])
edit_lunch = (
    Node(
        "Go back",
        "Go_back",
        lambda x, y: {"message": "Did you have lunch with KOICA collague?"},
    )
    .set_parents([location])
    .set_children(lunch_options)
)

# Over write flow
rewrite_lunch = Node(
    "check rewrite lunch log", "Rewrite the lunch log", check_rewrite_log, isEntry=True
)
confirm_rewrite_lunch = (
    Node("confirm rewrite", "Yes, I delete and write again", rewrite_log)
    .set_parents([rewrite_lunch])
    .set_children(lunch_options)
)
cancel = Node("cancel", "Cancel", cancel).set_parents([rewrite_lunch])

# set getting back
getting_back.set_condtional_children(
    {
        "new": lunch_options,
        "duplicated": [rewrite_lunch, cancel],
    }
)

# update location
location.set_condtional_children(
    {
        "lunch": [confirm, edit_lunch],
    }
)

not_available.set_condtional_children(
    {
        "lunch": [confirm, edit_lunch],
    }
)
# create tree
get_back_tree = ConversationTree(getting_back)