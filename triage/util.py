from math import ceil


class Paginator:

    def __init__(self, queryset, size_per_page, current_page):
        self.count = queryset.count()
        self.queryset = queryset
        self.size_per_page = size_per_page

        current_page = int(current_page)

        if current_page < 1:
            current_page = 1

        self.current_page = current_page

    def get_current_page(self):
        offsetX = (self.current_page - 1) * self.size_per_page
        offsetY = offsetX + self.size_per_page
        return self.queryset[offsetX:offsetY]

    def get_num_pages(self):
        return int(ceil(self.count / float(self.size_per_page)))

    def get_first(self):
        return 1

    def get_last(self):
        return self.get_num_pages()

    def has_prev(self):
        return self.current_page > 1

    def has_next(self):
        return self.current_page < self.get_num_pages

    def get_current_page_number(self):
        return self.current_page