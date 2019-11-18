from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class ConteudoCalendar(HTMLCalendar):

    def __init__(self, conteudos):
        super(ConteudoCalendar, self).__init__()
        self.conteudos = self.group_by_day(conteudos)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.conteudos:
                cssclass += ' filled'
                body = ['<ul>']
                for conteudo in self.conteudos[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % conteudo.get_admin_url())
                    body.append(esc(conteudo))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(ConteudoCalendar, self).formatmonth(year, month)

    def group_by_day(self, conteudos):
        field = lambda conteudo: conteudo.data.day
        return dict(
            [(day, list(items)) for day, items in groupby(conteudos, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)