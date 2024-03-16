from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from types import MappingProxyType
import datetime as dt
from copy import deepcopy
import locale


locale.setlocale(locale.LC_ALL, "")
pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
page_w, page_h = (212*mm, 299*mm)
pagesize = (page_w, page_h)

borders_left = 5 * mm
borders_right = 5 * mm
borders_top = 5 * mm
borders_bottom = 5 * mm


def liner_horizontal(pagesize,  # num_of_lines: int = 33,
                     increment,
                     borders_left=borders_left, borders_right=borders_right,
                     borders_top=borders_top, borders_bottom=borders_bottom):
    x1 = borders_left
    x2 = pagesize[0] - borders_right
    y = borders_bottom
    coords_list = []
    while y <= pagesize[1] - borders_top:
        coords_list.append((x1, y, x2, y))
        y += increment
    # page_height = pagesize[1] - borders_top
    # draw_height = pagesize[1] - borders_top - borders_bottom
    # for line in range(num_of_lines-1):
    #     coords_list.append((x1, y, x2, y))
    #     y += draw_height / (num_of_lines - 1)
    # coords_list.append((x1, pagesize[1] - borders_top, x2, pagesize[1] - borders_top))
    # print(y)
    # for y in range(int(borders['bottom']), page_height):
    #     if y / (page_h // num_of_lines) == y // (page_h // num_of_lines):
    #         coords_list.append((x1, y, x2, y))
    return coords_list


def liner_vertical(pagesize,  # num_of_lines: int = 7,
                   increment,
                   borders_left=borders_left, borders_right=borders_right,
                   borders_top=borders_top, borders_bottom=borders_bottom):
    y1 = borders_bottom
    y2 = pagesize[1] - borders_top
    x = borders_left
    coords_list = []
    while x <= pagesize[0]:
        coords_list.append((x, y1, x, y2))
        x += increment
    # draw_width = pagesize[0] - borders_right - borders_left
    # for line in range(num_of_lines-1):
    #     coords_list.append((x, y1, x, y2))
    #     x += draw_width / (num_of_lines-1)
    # coords_list.append((pagesize[0] - borders_right, y1, pagesize[0] - borders_right, y2))
    return coords_list


def month_by_weeks(year=2024, month=1) -> list[list]:
    start_date = dt.date(year, month, 1)
    end_date = start_date + dt.timedelta(days=31)
    # print(f'{start_date = }\n{end_date = }')
    dates = []
    increment = dt.timedelta(days=1)
    weeks = []
    week = [None for _ in range(7)]
    for i in range((end_date - start_date).days + 1):
        date = start_date + increment * i
        if date.month == start_date.month:
            dates.append(date)
    for day in dates:
        if day.weekday() == 0:
            week = [None for _ in range(7)]
        week[day.weekday()] = day  # .strftime('%d, %a')
        if day.weekday() == 6:
            weeks.append(week)
        last_day = day
    if last_day.weekday() != 6:
        weeks.append(week)
    # for day in dates:
    #     print(day.strftime('%d, %a'))
    return weeks


def planer_month_weeks(canvas: Canvas, weeks: list[list[dt.date]]):
    borders_top = 12 * mm
    draw_height = pagesize[1] - borders_top - borders_bottom
    increment_v = draw_height / (33 - 1)
    lines = liner_horizontal(pagesize, increment_v, borders_top=borders_top)
    for week in weeks:
        for n, line in enumerate(lines[::-1], start=1):
            if n in [1, 9, 15, 21, 27]:
                day = week.pop(0)
                if day is not None:
                    day_string = day.strftime('%d, %a')
                    canvas.setFillColorRGB(0.988, 0.882, 0.541)
                    canvas.rect(line[0], line[1], 20 * mm, 7 * mm, stroke=0, fill=1)
                    canvas.setFont('Arial', 16)
                    canvas.setFillGray(0.3)
                    canvas.drawString(line[0] + 1 * mm, line[1] + 1.5 * mm, day_string)
        canvas.setStrokeGray(0.8)
        canvas.lines(lines)
        canvas.showPage()
    # canvas.setStrokeGray(0.8)
    # canvas.lines(lines)
    # canvas.showPage()
    # canvas.save()


def planer_month_whole(canvas: Canvas, weeks: list[list[dt.date]], month_name):
    borders_left = 5 * mm
    borders_right = 5 * mm
    borders_top = 20 * mm
    borders_bottom = 40 * mm
    canvas.setFillGray(0.3)
    canvas.setFont('Arial', 20)
    canvas.drawString(borders_left, pagesize[1] - 15 * mm, month_name)
    draw_width = pagesize[0] - borders_right - borders_left
    draw_height = pagesize[1] - borders_top - borders_bottom
    increment_v = draw_height / (6 - 1)
    increment_h = draw_width / (8 - 1)
    lines_h = liner_horizontal(pagesize, increment_v, borders_top=borders_top, borders_bottom=borders_bottom)
    lines_v = liner_vertical(pagesize, increment_h, borders_top=borders_top, borders_bottom=borders_bottom)
    for wom, week in enumerate(weeks):
        # for n, line in enumerate(lines_h[::-1], start=1):
        for line_v in lines_v[:-1]:
            day = week.pop(0)
            if day is not None:
                day_string = day.strftime('%d, %a')
                canvas.setFont('Arial', 16)
                if day.weekday() in [5, 6]:
                    canvas.setFillColorRGB(0.9, 0.7, 0.6)
                else:
                    canvas.setFillColorRGB(0.988, 0.882, 0.541)
                canvas.rect(line_v[0], line_v[3] - 7 * mm - increment_v * wom, increment_h, 7 * mm, stroke=0, fill=1)
                canvas.setFillGray(0.3)
                canvas.drawString(line_v[0] + 1 * mm, line_v[3] - 7 * mm - increment_v * wom + 1.5 * mm, day_string)
    canvas.setStrokeGray(0.8)
    canvas.lines(lines_h)
    canvas.lines(lines_v)
    canvas.showPage()


def planer_blank_pages(canvas, pages=5):
    borders_top = 12 * mm
    draw_height = pagesize[1] - borders_top - borders_bottom
    increment_v = draw_height / (33 - 1)
    lines = liner_horizontal(pagesize, increment_v, borders_top=borders_top)
    for _ in range(pages):
        canvas.setStrokeGray(0.8)
        canvas.lines(lines)
        canvas.setFillColorRGB(0.988, 0.882, 0.541)
        canvas.rect(lines[-1][0], lines[-1][1], 110 * mm, 7 * mm, stroke=0, fill=1)
        canvas.showPage()


def planer_month(year=2024, month=1):
    filename = f'{year}_{month:02}.pdf'
    canvas = Canvas(filename, pagesize=pagesize)
    month_name = dt.date(year, month, 1).strftime('%B')
    weeks = month_by_weeks(year, month)
    planer_month_whole(canvas, deepcopy(weeks), month_name)
    planer_month_weeks(canvas, deepcopy(weeks))
    planer_blank_pages(canvas)
    canvas.save()


if __name__ == '__main__':
    planer_month(month=4)
