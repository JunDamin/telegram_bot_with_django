import re
from telegram import KeyboardButton
from telegram.ext import MessageHandler, Filters, ConversationHandler
from features.message import send_markdown, reply_markdown

class Node:
    """ define node in conversation """

    def __init__(
        self,
        name,
        button,
        procedure,
        children=[],
        root=None,
        handler=MessageHandler,
        isPublic=False,
        isEntry=False,
    ):
        self.added = False
        self.state = None
        self.name = name
        self.button = button
        self.procedure = procedure
        self.children = children
        self.root = root
        self.handler = handler
        self.isPublic = isPublic
        self.isEntry = isEntry

    def get_handler(self):
        # need to distinguish location command handler
        if type(self.button) == KeyboardButton:
            button_filter = Filters.location
        else:
            pattern = re.compile(f"^{self.button}$", re.IGNORECASE)
            button_filter = Filters.regex(pattern)
        if not self.isPublic:
            button_filter = button_filter & Filters.chat_type.private
        return self.handler(button_filter, self.get_callback)

    def get_callback(self, update, context):
        msg = self.procedure(update, context)
        reply_markdown(update, context, msg, self.get_keyboard())
        return self.state if self.children else ConversationHandler.END

    def get_keyboard(self):
        """ get children's button into keyboard """
        return [[child.button for child in self.children]] if self.children else None


class ConversationTree:
    def __init__(self, root):
        self.root = root
        self.nodes = get_all_nodes(self.root)

    def get_conversation(self):
        entry_points = [node.get_handler() for node in self.nodes if node.isEntry]
        states = {}
        for i, node in enumerate(self.nodes):
            node.state = i
            states[i] = (
                states[i].extend([child.get_handler() for child in node.children])
                if states.get(i)
                else [child.get_handler() for child in node.children]
            )
        fallbacks = []
        return ConversationHandler(
            entry_points=entry_points,
            states=states,
            fallbacks=fallbacks,
            map_to_parent={},
            allow_reentry=True,
        )

    def get_graph(self, path):
        print(len(self.nodes))
        header = "@startuml\n'default\ntop to bottom direction\n"
        footer = "@enduml"
        with open(path, 'w') as f:
            f.write(header)
            for node in self.nodes:
                for child in node.children:
                    f.write(f"({node.name}) --> ({child.name}): {child.button}\n")
            f.write(footer)

def get_all_nodes(node, nodes=[]):
    """ search all the nodes from node """
    if node.added:
        return nodes
    node.added = True
    nodes.append(node)
    for child in node.children:
        nodes = get_all_nodes(child, nodes)
    return nodes


test_root = Node("Initial", "test", lambda update, context: update.message.text, isEntry=True)
child1 = Node("check", "child1", lambda update, context: "child1")
child2 = Node("test2", "Child2", lambda update, context: "child2")
test_root.children = [child1, child2]
grand1 = Node("Whot", "grand1", lambda update, context: "grand1")
grand2 = Node("test", "grand2", lambda update, context: "grand2")
child1.children = [grand1, grand2]
child2.children = [grand1, grand2]
tree = ConversationTree(test_root)

tree_conv = tree.get_conversation()
tree.get_graph("test.wsd")