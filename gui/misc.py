import dearpygui.dearpygui as dpg
import datetime

stup:list[str] = ['05', '10', '15', '20', '25', '30', '35']
list_for_plot_x: list[float] = []
list_for_plot_y1: list[float] = []
list_for_plot_y2: list[float] = []
win_pos: list[int] = [400, 100]
inf_pos: list[int] = [0, 20]


def styp_torm(styp:str) ->str:
    if styp == '00':
        return "Нет ступени"
    if styp == '01':
        return "Оттормаживание"
    if styp == '02':
        return "Ступень 0,5"
    if styp == '03':
        return "Ступень 1,0"
    if styp == '04':
        return "Ступень 1,5"
    if styp == '05':
        return "Ступень 2,0"
    if styp == '06':
        return "Ступень 2,5"
    if styp == '07':
        return "Ступень 3,0"
    if styp == '08':
        return "Ступень 3,5"
    if styp == '09':
        return "Ступень 4,0"
    if styp == '10':
        return "Не распознанно"
    if styp == '11':
        #TODO: Log tihs!
        return "Ошибка"
    return ""

def state_l(s:str) ->str:
    if int(s) == 0:
        return "Цепи выключены"
    s_b = bin(int(s))
    s_out:str =""
    if s_b[2] == '1':
        s_out +="P "
    if s_b[3] == '1':
        s_out +="T4 "
    if s_b[4] == '1':
        s_out +="T3 "
    if s_b[5] == '1':
        s_out +="T2 "
    if s_b[6] == '1':
        s_out +="T1 "
    return s_out

def print_real_time() ->None:
    c_t = datetime.datetime.now()
    time_str = c_t.strftime("%H:%M:%S")
    dpg.set_value(item="time_tag", value = time_str)


