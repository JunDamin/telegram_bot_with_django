from conversations.tree_signing import sign_in_tree, sign_out_tree
from conversations.tree_get_back import get_back_tree


conversations = [
    sign_in_tree.get_conversation(),
    sign_out_tree.get_conversation(),
    get_back_tree.get_conversation(),
]