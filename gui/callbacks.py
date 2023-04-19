import dearpygui.dearpygui as dpg
import backend.backend_parser as parser
import backend.backend_serial as ser
from multiprocessing import Queue
from stp_conf.load_json import *
from .misc import *
from .draw_scheme_stp import draw_info_table
import time
from typing import Any
err_pos: list[int] = [800, 700]


def close_err() -> None:
    global err_pos
    err_pos = [800, 700]


def err_callback(sender: int, app_data: str, user_data: dict[str, Any]) -> None:
    global err_pos
    bmk: str = user_data['bmk']
    if not user_data['data']['getStatus\r\n']:
        return
    err: str = user_data["data"]['getStatus\r\n']['Err']
    if dpg.does_item_exist(f"ERR:{bmk}"):
        if dpg.is_item_visible(f"ERR:{bmk}"):
            return
        else:
            dpg.delete_item(f"ERR:{bmk}")
    list_of_errors = parser.check_err(err)
    with dpg.window(tag=f"ERR:{bmk}", pos=err_pos, autosize=True, no_move=False, label=f"Ошибки {list_of_bmk[bmk]}", on_close=close_err, min_size=(400, 50)):
        if not list_of_errors:
            dpg.add_text(f"Ошибок нет")
        else:
            for i, err in enumerate(list_of_errors):
                dpg.add_text(f"{i+1}. {str(err)}")
        err_pos[0] -= 50
        err_pos[1] -= 50
    if err_pos[0] == 500 and err_pos[1] == 400:
        err_pos = [800, 700]




def close_inf() -> None:
    global inf_pos
    inf_pos = [0, 20]


def draw_window_table(sender: int, add_data: str, user_data: dict[str, dict[str, dict[str, str]]]) -> None:
    global inf_pos
    bmk: str = str(user_data['bmk'])
    data_for_table = user_data['data']['getStatus\r\n']
    if not data_for_table:
        return
    if dpg.does_item_exist(f"INFO:{bmk}"):
        if dpg.is_item_visible(f"INFO:{bmk}"):
            return
        else:
            dpg.delete_item(f"INFO:{bmk}")
    with dpg.window(tag=f"INFO:{bmk}", label=f"{list_of_bmk[bmk]}", autosize=True, pos=inf_pos, on_close=close_inf):
        with dpg.table(tag=f"MT_{bmk}", header_row=False, width=400, borders_innerH=True, borders_innerV=True, policy=dpg.mvTable_SizingFixedFit):
            dpg.add_table_column()
            dpg.add_table_column()
            draw_info_table(bmk, data_for_table)
        inf_pos[0] += 50
        inf_pos[1] += 50
        if inf_pos[0] == 300 and inf_pos[1] == 320:
            inf_pos[0] = 0
            inf_pos[1] = 20
    dpg.bind_item_font(f"INFO:{bmk}", 'table_font')

def close_plot(sender: int, app_data: str, q_task: Queue[list[bytes]]) -> None:
    commands_list: list[bytes] = []
    for bmk in list_of_bmk.keys():
        for command in list_of_control_com[:1]:
            commands_list.append(ser.commands_generator(bmk, command).encode())
    q_task.put(commands_list)


def create_plot(sender: str, app_data: list[str], q_task: Queue[list[bytes]]) -> None:
    commands_list: list[bytes] = []
    for bmk in list_of_bmk.keys():
        for command in list_of_control_com[:1]:
            commands_list.append(ser.commands_generator(bmk, command).encode())
    if dpg.does_item_exist("plot_win"):
        if dpg.is_item_visible("plot_win"):
            return
        else:
            dpg.delete_item("plot_win")
    current_bmk: str = list_of_bmk[sender[3:]]
    with dpg.window(label=f"Показатели давления на {current_bmk}", tag="plot_win", pos=(1000, 80), no_background=False, no_title_bar=False, no_resize=True, on_close=close_plot, user_data=q_task, no_move=False):
        with dpg.plot(label=f"Давление датчика 1 и 2 {current_bmk}", height=450, width=450):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Счетчик", tag="x_axis")
            dpg.add_plot_axis(dpg.mvYAxis, label="Давление кПа", tag="y_axis")
            dpg.add_line_series(list_for_plot_x, list_for_plot_y1,
                                label=f"Давление датчика 1 {current_bmk}", parent="y_axis", tag="series_tag1")
            dpg.add_line_series(list_for_plot_x, list_for_plot_y2,
                                label=f"Давление датчика 2 {current_bmk}", parent="y_axis", tag="series_tag2")
            dpg.set_axis_limits("y_axis", 0, 500)
            dpg.bind_item_theme("series_tag1", "ser1_theme")
            dpg.bind_item_theme("series_tag2", "ser2_theme")
    for bmk in list_of_bmk.keys():
        for command in list_of_control_com[:1]:
            commands_list.append(ser.commands_generator(bmk, command).encode())
    for i in range(1, len(commands_list)*2, 2):
        commands_list.insert(i, f'bmk:{sender[3:]}:gPr\r\n'.encode())
    q_task.put(commands_list)


def empty_callback() -> None:
    pass


def cancel(s:int, a_p:str, u_d:str) -> None:
    dpg.delete_item(u_d)
    if dpg.does_item_exist('res_s'):
        dpg.delete_item('res_s')
    for bmk in list_of_bmk:
        dpg.set_value(f'pr_is_ref{bmk}', False)


def send_pr(s:str, a_p:str, u_d:list[Any]) -> None:
    i:int = 0
    st = s.split('_')[0]
    new_pr = dpg.get_value(f'new_pr_{st}{u_d[0]}')
    pr_com = f"bmk:{u_d[0]}:setP{st}={new_pr}".encode()
    commands_list: list[bytes] = []
    for bmk in list_of_bmk.keys():
        for command in list_of_control_com[:1]:
            commands_list.append(ser.commands_generator(bmk, command).encode())
    commands_list.insert(0, pr_com)
    u_d[1].put(commands_list)
    time.sleep(1)
    commands_list.pop(0)
    u_d[1].put(commands_list)
    dpg.set_value(f'pr_is_ref{u_d[0]}', False)
    while i < 10000000:
        i += 1
        dpg.set_value('p_b_pr', i / 13000000)
    if dpg.get_value(f'new_pr_{st}{u_d[0]}') != new_pr:
        with dpg.window(label='Результат настройки', tag = 'res_s', autosize= False, pos= (dpg.get_item_pos(f"set_pr_st{u_d[0]}")[0] + 40, dpg.get_item_pos(f"set_pr_st{u_d[0]}")[0] + 40), width= 500):
            dpg.add_text(default_value='Неудачная попытка насйтроки, попробуйте ещё!')
            dpg.add_button(label='Ок', callback=cancel, user_data=f"res_s")
            dpg.set_value('p_b_pr', 0)
    else: 
        with dpg.window(label='Результат настройки', tag = 'res_s', autosize= False, pos= (dpg.get_item_pos(f"set_pr_st{u_d[0]}")[0] + 40, dpg.get_item_pos(f"set_pr_st{u_d[0]}")[0] + 40), width= 300):
            dpg.add_text(default_value='Успех!')
            dpg.add_button(label='Ок', callback=cancel, user_data=f"res_s")
            dpg.set_value('p_b_pr', 1)
        

def refresh_pr(params: dict[str, dict[str, dict[str, str]]]) -> None:
    bmk: str = str(params['bmk'])
    data_for_table = params['data']['getStatus\r\n']
    if dpg.does_item_exist(f'set_pr_st{bmk}') and not dpg.get_value(f'pr_is_ref{bmk}'):
        for cnt, st in enumerate(stup):
            cnt += 7 
            dpg.set_value(f'new_pr_{st}{bmk}', int(data_for_table[list(data_for_table)[cnt]]))
        dpg.set_value(f'pr_is_ref{bmk}', True)

def set_pr_st(s:int, a_d:str, user_data:list[Any]) -> None:
    global list_for_plot_y2, list_for_plot_x, list_for_plot_y1
    commands_list: list[bytes] = []
    for bmk in list_of_bmk.keys():
        for command in list_of_control_com[:1]:
            commands_list.append(ser.commands_generator(bmk, command).encode())
    if dpg.does_item_exist("plot_win"):
        dpg.delete_item("plot_win")
        list_for_plot_x = []
        list_for_plot_y1 = []
        list_for_plot_y2 = []
        user_data[1].put(commands_list)
    if dpg.does_item_exist(f"set_pr_st{user_data[0]}"):
        if dpg.is_item_visible(f"set_pr_st{user_data[0]}"):
            return
        else:
            dpg.delete_item("set_pt_st")
    with dpg.window(label=f"Настройка далвения по ступеням {list_of_bmk[user_data[0]]}", tag=f"set_pr_st{user_data[0]}", pos=(500, 400), no_resize=False, autosize=True, on_close=cancel, user_data= f"set_pr_st{user_data[0]}"):
        with dpg.group(horizontal= True):
            dpg.add_text(default_value= 'Значение давления ступени 0,5:')
            dpg.add_input_int(default_value=5, width=200, tag=f'new_pr_05{user_data[0]}', max_value=125, min_value=15, max_clamped=True, min_clamped=True)
            dpg.add_button(label= 'Настроить', callback= send_pr, tag = f'05_{user_data[0]}', user_data= user_data)
        with dpg.group(horizontal= True):
            dpg.add_text(default_value= 'Значение давления ступени 1,0:')
            dpg.add_input_int(default_value=5, width=200, tag=f'new_pr_10{user_data[0]}', max_value=170, min_value=76, max_clamped=True, min_clamped=True)
            dpg.add_button(label= 'Настроить', callback= send_pr, tag = f'10_{user_data[0]}', user_data= user_data)
        with dpg.group(horizontal= True):
            dpg.add_text(default_value= 'Значение давления ступени 1,5:')
            dpg.add_input_int(default_value=5, width=200, tag=f'new_pr_15{user_data[0]}', max_value=277, min_value=137, max_clamped=True, min_clamped=True)
            dpg.add_button(label= 'Настроить', callback= send_pr, tag = f'15_{user_data[0]}', user_data= user_data)
        with dpg.group(horizontal= True):
            dpg.add_text(default_value= 'Значение давления ступени 2,0:')
            dpg.add_input_int(default_value=5, width=200, tag=f'new_pr_20{user_data[0]}', max_value=395, min_value=213, max_clamped=True, min_clamped=True)
            dpg.add_button(label= 'Настроить', callback= send_pr, tag = f'20_{user_data[0]}', user_data= user_data)
        with dpg.group(horizontal= True):
            dpg.add_text(default_value= 'Значение давления ступени 2,5:')
            dpg.add_input_int(default_value=5, width=200, tag=f'new_pr_25{user_data[0]}', max_value=502, min_value=289, max_clamped=True, min_clamped=True)
            dpg.add_button(label= 'Настроить', callback= send_pr, tag = f'25_{user_data[0]}', user_data= user_data)
        with dpg.group(horizontal= True):
            dpg.add_text(default_value= 'Значение давления ступени 3,0:')
            dpg.add_input_int(default_value=5, width=200, tag=f'new_pr_30{user_data[0]}', max_value=577, min_value=395, max_clamped=True, min_clamped=True)
            dpg.add_button(label= 'Настроить', callback= send_pr, tag = f'30_{user_data[0]}', user_data= user_data)
        with dpg.group(horizontal= True):
            dpg.add_text(default_value= 'Значение давления ступени 3,5:')
            dpg.add_input_int(default_value=5, width=200, tag=f'new_pr_35{user_data[0]}', max_value=486, min_value=684, max_clamped=True, min_clamped=True)
            dpg.add_button(label= 'Настроить', callback= send_pr, tag = f'35_{user_data[0]}', user_data= user_data)
        dpg.add_text(default_value="")
        with dpg.group(horizontal= True):
            dpg.add_button(label="Отмена", callback=cancel, user_data=f"set_pr_st{user_data[0]}", tag='canc')         
            dpg.add_progress_bar(default_value=0, tag = 'p_b_pr', width=450)  
            dpg.add_button(label="Готово", callback=cancel, user_data=f"set_pr_st{user_data[0]}", tag='set')   


def send_temp_set(s:int, a_p:str, u_d:list[Any]) -> None:
    i:int = 0
    temp:int = dpg.get_value('new_temp')
    temp_com:bytes = f'bmk:{u_d[0]}:setTempHeart={temp}'.encode()
    commands_list: list[bytes] = []
    for bmk in list_of_bmk.keys():
        for command in list_of_control_com[:1]:
            commands_list.append(ser.commands_generator(bmk, command).encode())
    commands_list.insert(0, temp_com)
    u_d[1].put(commands_list)
    time.sleep(1)
    commands_list.pop(0)
    u_d[1].put(commands_list)
    dpg.set_item_callback('canc', empty_callback)
    dpg.set_item_callback('set', empty_callback)
    while int(dpg.get_value(f'set_temp_c_v_{u_d[0]}').replace('+', '')) != dpg.get_value('new_temp'):
        dpg.set_value('p_b_temp', i / 140000)
        i += 1
        if i > 10000000:
            with dpg.window(label='Результат настройки', tag = 'res_s', autosize= False, pos= (dpg.get_item_pos('set_temp_w')[0] + 40, dpg.get_item_pos('set_temp_w')[0] + 40), width= 500):
                dpg.add_text(default_value='Неудачная попытка насйтроки, попробуйте ещё!')
                dpg.add_button(label='Ок', callback=cancel, user_data='set_temp_w')
            return
    with dpg.window(label='Результат настройки', tag = 'res_s', autosize= False, pos= (dpg.get_item_pos('set_temp_w')[0] + 40, dpg.get_item_pos('set_temp_w')[0] + 40), width= 300):
        dpg.add_text(default_value='Успех!')
        dpg.add_button(label='Ок', callback=cancel, user_data='set_temp_w')
    dpg.set_value('p_b_temp', 1)
    return

    
def set_temp(s:int, a_d:str, user_data:list[Any]) -> None:
    global list_for_plot_y2, list_for_plot_x, list_for_plot_y1
    commands_list: list[bytes] = []
    for bmk in list_of_bmk.keys():
        for command in list_of_control_com[:1]:
            commands_list.append(ser.commands_generator(bmk, command).encode())
    if dpg.does_item_exist("plot_win"):
        dpg.delete_item("plot_win")
        list_for_plot_x = []
        list_for_plot_y1 = []
        list_for_plot_y2 = []
        user_data[1].put(commands_list)
    if dpg.does_item_exist("set_temp_w"):
        if dpg.is_item_visible("set_temp_w"):
            return
        else:
            dpg.delete_item("set_temp_w")
    with dpg.window(label=f"Настройка температуры включения обогрева {list_of_bmk[user_data[0]]}", tag="set_temp_w", pos=(500, 400), no_resize=False, width=500, height=150):
        with dpg.group(horizontal= True):
            dpg.add_text(default_value= 'Текущее значение (С):')
            dpg.add_text(default_value="", tag=f'set_temp_c_v_{user_data[0]}')
        with dpg.group(horizontal=True):
            dpg.add_text(default_value="Введите новое значение (C):")
            dpg.add_input_int(default_value=5, width=200, tag='new_temp', max_value=63, min_value=1, max_clamped=True, min_clamped=True)
        with dpg.group(horizontal=True, horizontal_spacing= 287):
            dpg.add_button(label="Отмена", callback=cancel, user_data='set_temp_w', tag='canc')         
            dpg.add_button(label="Настроить", callback=send_temp_set, user_data= user_data, tag='set')       
        dpg.add_progress_bar(default_value=0, tag = 'p_b_temp', width=450)  
      