import dearpygui.dearpygui as dpg
import backend.backend_parser as parser
import backend.backend_serial as ser
from stp_conf.load_json import *
from .misc import *
from .draw_scheme_stp import draw_info_table
err_pos: list[int] = [800, 700]


def close_err() -> None:
    global err_pos
    err_pos = [800, 700]


def err_callback(sender, app_data, user_data):
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
            dpg.add_text("Ошибок нет")
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


def draw_window_table(sender: int, add_data: str, user_data):
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


def close_plot(sender, app_data, q_task):
    commands_list: list[bytes] = []
    for bmk in list_of_bmk.keys():
        for command in list_of_control_com[:1]:
            commands_list.append(ser.commands_generator(bmk, command).encode())
    q_task.put(commands_list)


def create_plot(sender, app_data, q_task):
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
            dpg.set_axis_limits("y_axis", 0, 700)
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
