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
        isReply=True,
        inputType="regex",
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
        self.isReply = isReply
        self.isLocation = inputType == "location"
        self.isText = inputType == "text"
        self.isRegex = inputType == "regex"

    def __str__(self):
        return f"Node: {self.name}"

    def get_button(self):
        if self.isLocation:
            button = KeyboardButton("Share Location", request_location=True)
        if self.isRegex:
            button = self.button
        if self.isText:
            button = None
        return button

    def get_handler(self):
        if self.isLocation:
            button_filter = Filters.location
        if self.isRegex:
            pattern = re.compile(f"^{self.button}$", re.IGNORECASE)
            button_filter = Filters.regex(pattern)
        if self.isText:
            button_filter = Filters.text
        if not self.isPublic:
            button_filter = button_filter & Filters.chat_type.private
        return self.handler(button_filter, self.get_callback)

    def get_callback(self, update, context):
        # procdure should return id and msg, id is optional if isReply
        id, msg = self.procedure(update, context)
        if self.isReply:
            reply_markdown(update, context, msg, self.get_keyboard())
        else:
            send_markdown(update, context, id, msg, self.get_keyboard())
        return self.state if self.children else ConversationHandler.END

    def get_keyboard(self):
        """ get children's button into keyboard """
        keyboard = [[child.get_button() for child in self.children]]
        #  check none key
        if [key for key in keyboard[0] if not key]:
            keyboard = None
        return keyboard if self.children else None

    def set_condtional_children(self, func, child_dict):
        # self.children = #flatten list?
        pass


class ConversationTree:
    def __init__(self, root):
        self.root = root
        self.nodes = get_all_nodes(root)

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
        header = "@startuml\n'default\ntop to bottom direction\n"
        footer = "@enduml"
        with open(path, "w") as f:
            f.write(header)
            for node in self.nodes:
                for child in node.children:
                    f.write(f"({node.name}) --> ({child.name}): {child.button}\n")
            f.write(footer)


def get_all_nodes(node, nodes=[]):
    """ search all the nodes from node """
    nodes = [node for node in nodes]    # new reference
    if node.added:
        return nodes
    node.added = True
    nodes.append(node)
    for child in node.children:
        nodes = get_all_nodes(child, nodes)
    return nodes
