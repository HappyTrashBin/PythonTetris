class Colors:
    green = (47, 230, 23)
    red = (232, 18, 18)
    orange = (226, 116, 17)
    yellow = (237, 234, 4)
    purple = (166, 0, 247)
    cyan = (21, 204, 209)
    blue = (13, 64, 216)
    white = (255, 255, 255)
    black = (0, 0, 0)
    silver = (192, 192, 192)
    grey = (128, 128, 128)
    gold = (255, 215, 0)
    dark_orange = (255, 71, 0)

    # доступ к содержимому класса без создания и заполнения отдельного его экземпляра
    @classmethod
    def get_all_colors(cls):
        return [cls.black, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]
