import re
from telegram import KeyboardButton
from telegram.ext import MessageHandler, Filters, ConversationHandler, CommandHandler
from telegram.utils.types import JSONDict
from features.message import send_markdown, reply_markdown


class Node:
    """ define node in conversation """

    def __init__(
        self,
        name,
        button,
        procedure,
        root=None,
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
        self._children = []
        self._parents = []
        self.root = root
        self.isPublic = isPublic
        self.isEntry = isEntry
        self.isReply = isReply
        self.isLocation = inputType == "location"
        self.isText = inputType == "text"
        self.isRegex = inputType == "regex"
        self.isCommand = inputType == "command"

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
        if self.isCommand:
            return CommandHandler(self.button, self.get_callback)
        if self.isLocation:
            button_filter = Filters.location
        if self.isRegex:
            pattern = re.compile(f"^{self.button}$", re.IGNORECASE)
            button_filter = Filters.regex(pattern)
        if self.isText:
            button_filter = Filters.text
        if not self.isPublic:
            button_filter = button_filter & Filters.chat_type.private
        return MessageHandler(button_filter, self.get_callback)

    def get_callback(self, update, context):
        # procdure should return id and msg, id is optional if isReply
        self.data = self.procedure(update, context)
        if self.isReply:
            reply_markdown(
                update,
                context,
                self.data["message"],
                self.get_keyboard(),
            )
        else:
            send_markdown(
                update,
                context,
                self.data["id"],
                self.data["message"],
                self.get_keyboard(),
            )
        
        if self.data.get("path"):
            options = {"redo": self._parents[0].state, "escape": ConversationHandler.END}
            if self.data.get("path") == "escape":
                context.user_data.clear()
            return options[self.data.get("path")]
        if self._children:
            return self.state
        else:
            context.user_data.clear()
            return ConversationHandler.END

    def get_keyboard(self):
        """ get children's button into keyboard """
        # check cumstom keyboard
        if self.data.get("keyboard"):
            return self.data.get("keyboard") if not [[]] else None

        keyboard = [[child.get_button() for child in self._children]]
        #  check none key
        if [key for key in keyboard[0] if not key]:
            keyboard = None
        return keyboard if self._children else None

    def set_parents(self, parents: list):
        for parent in parents:
            if self not in parent._children:
                parent._children.append(self)
            if parent not in self._parents:
                self._parents.append(parent)
        return self

    def set_children(self, children: list):
        for child in children:
            if child not in self._children:
                self._children.append(child)
            if self not in child._parents:
                child._parents.append(self)
        return self


class ConditionalNode(Node):
    def get_keyboard(self):
        condition = self.data["condition"]
        keyboard = [[child.get_button() for child in self._children_dict[condition]]]
        if [key for key in keyboard[0] if not key]:
            keyboard = None
        return keyboard if self._children_dict[condition] else None

    def set_conditional_children(self, children_dict):
        self._children_dict = children_dict
        self._children = [
            node for key in children_dict.keys() for node in children_dict[key]
        ]
        for child in self._children:
            if self not in child._parents:
                child._parents.append(self)


class ConversationTree:
    def __init__(self, root):
        self.root = root
        self.nodes = get_all_nodes(root)
        for node in self.nodes:
            node.added = False

    def get_conversation(self):
        entry_points = [node.get_handler() for node in self.nodes if node.isEntry]
        states = {}
        for i, node in enumerate(self.nodes):
            node.state = i
            states[i] = (
                states[i].extend([child.get_handler() for child in node._children])
                if states.get(i)
                else [child.get_handler() for child in node._children]
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
                for child in node._children:
                    f.write(f"({node.name}) --> ({child.name}): {child.button}\n")
            f.write(footer)


def get_all_nodes(node, nodes=[]):
    """ search all the nodes from node """
    nodes = nodes[:]  # new reference
    if node.added:
        return nodes
    node.added = True
    nodes.append(node)
    for child in node._children:
        nodes = get_all_nodes(child, nodes)
    return nodes
