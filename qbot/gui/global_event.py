from qbot.common.logging.logger import LOGGER as logger


class GlobalEvent:
    MSG_TYPE_SERIES = 1

    def __init__(self):
        self.observers = {}

    def add_observer(self, msg_type, observer):
        if msg_type in self.observers.keys():
            self.observers[msg_type].append(observer)
        else:
            self.observers[msg_type] = [observer]

    def notify(self, msg_type, data):
        logger.info("[GlobalEvent] get a notify ...")
        # print("data: ", data)
        if msg_type in self.observers.keys():
            for observer in self.observers[msg_type]:
                observer.handle_data(data)


GlobalEvent = GlobalEvent()
