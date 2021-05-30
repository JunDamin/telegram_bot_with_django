from conversations.tree_classes import Node, ConversationTree


test_root = Node("test", "test", lambda update, context: (None, "Please text me the reason."), isEntry=True)
child1 = Node("test location", "location", lambda update, context: (None, "child1"), inputType="location")
child2 = Node("test2", "Child2", lambda update, context: (None, "child2"))
test_root.children = [child1, child2]
grand1 = Node("test", "grand1", lambda update, context: (None, "type text"))
grand2 = Node("test", "grand2", lambda update, context: (None, "grand2"))
child1.children = [grand1, grand2]
child2.children = [grand1, grand2]
grandgrand = Node("text", "text", lambda update, context: (None, "get text"), inputType="text")
grand1.children = [grandgrand]
end_node = Node("End", "Confirm", lambda update, context: (None, "Confirmed"))
grandgrand.children = [end_node]

tree = ConversationTree(test_root)
tree_conv = tree.get_conversation()
tree.get_graph("telegram_bot/diagrams/conversation_tree.wsd")

conversations = [
    tree_conv
]