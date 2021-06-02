from conversations.sign_in_out import sign_in_tree, sign_out_tree
from conversations.get_back import get_back_tree


conversations = [
    sign_in_tree.get_conversation(),
    sign_out_tree.get_conversation(),
    get_back_tree.get_conversation(),
]