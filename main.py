# For GUI we chose dear pygui. For each of BUKs we made a different window, and show all
# data in tables. For each of commands we made different button that callback
# a function to create a context menu of command.

import dearpygui.dearpygui as dpg
import backend.backend_serial as ser
from stp_conf.load_json import *
from gui.misc import *
from gui.callbacks import *
from gui.draw_scheme_stp import *
from multiprocessing import Process, Value, Queue, freeze_support
import serial
from typing import Any

cnt: int = 0
new_temp: int = 5


def main_com_loop(q: Any, q_task: Any) -> None:
    commands_list: list[bytes] = []
    for bmk in list_of_bmk.keys():
        for command in list_of_control_com[:1]:
            commands_list.append(ser.commands_generator(bmk, command).encode())
    ser.PORT = ser.avilable_com()
    while True:
        try:
            with serial.Serial(ser.PORT,
                               ser.BAUD,
                               ser.BYTE_SIZE,
                               ser.PARITY,
                               ser.STOP_BITS,
                               timeout=0.5) as port:
                while True:
                    try:
                        sending_commands_loop(commands_list, q, port)
                    except serial.SerialException:
                        break
                    if not q_task.empty():
                        commands_list = q_task.get_nowait()
                        if commands_list == [b'KILL']:
                            return
        except serial.SerialException:
            ser.PORT = ser.avilable_com()
            if ser.PORT == "0":
                continue
            pass


def sending_commands_loop(commands_list, q, port) -> None:
    for command in commands_list:
        bmk_num = f'{command[4:7].decode()}'
        try:
            q.put({'bmk': bmk_num,
                   'data': ser.send_command(command.decode(), port)})
        except serial.SerialException:
            for bmk in list_of_bmk:
                q.put({'bmk': bmk, 'data': {'getStatus\r\n': ""}})
            raise serial.SerialException


def show_bmk(q: Any) -> None:
    global current_buks_list
    if not q.empty():
        params_dict = q.get_nowait()
        current_bmk: str = params_dict['bmk']
        redraw_data(params_dict)
        try:
            if params_dict['data']['getStatus\r\n']:
                if current_bmk not in current_buks_list:
                    current_buks_list.append(current_bmk)
                    redraw_bmk_window(params_dict)
                manage_error_in_get_status(current_bmk, params_dict)
                dpg.set_item_user_data(f"bmk_{current_bmk}", params_dict)
            else:
                current_buks_list = find_false(current_bmk, current_buks_list)
        except KeyError:
            try:
                if params_dict['data']['gPr\r\n']:
                    redraw_pr_plot(params_dict['data']['gPr\r\n'])
                else:
                    dpg.delete_item(f'line_{current_bmk}')
                    dpg.draw_line(parent=f"BMK:{current_bmk}", p1=(0, 50),
                                  p2=(150, 50), thickness=4,
                                  color=(255, 0, 255, 255),
                                  tag=f'line_{current_bmk}')
            except KeyError:
                pass
    blinker(current_buks_list)


def manage_error_in_get_status(current_bmk, params_dict):
    if int(params_dict['data']['getStatus\r\n']['Err']):
        if not dpg.get_value(f"line_err{current_bmk}"):
            dpg.set_value(f"line_err{current_bmk}", True)
        dpg.set_item_user_data(f"err_{current_bmk}", params_dict)
    else:
        if dpg.get_value(f"line_err{current_bmk}"):
            dpg.set_value(f"line_err{current_bmk}", False)


def find_false(current_bmk, current_buks_list):
    dpg.delete_item(f'line_bmk_{current_bmk}')
    dpg.draw_line(parent=f"BMK:{current_bmk}",
                  p1=(75, 65), p2=(110, 65),
                  thickness=10,
                  color=(255, 0, 255, 255),
                  tag=f'line_bmk_{current_bmk}')
    if dpg.get_value(f"line_err{current_bmk}"):
        dpg.set_value(f"line_err{current_bmk}", False)
    dpg.set_item_callback(f'bmk_{current_bmk}', callback=empty_callback)
    dpg.set_item_callback(f'err_{current_bmk}', callback=empty_callback)
    dpg.set_item_callback(f'pr_{current_bmk}', callback=empty_callback)
    if current_bmk in current_buks_list:
        current_buks_list.pop(current_buks_list.index(current_bmk))
    return current_buks_list


def blinker(current_buks_list: list[str]) -> None:
    if dpg.get_value("cnt") == 60:
        for bmk in current_buks_list:
            if dpg.get_value(f"line_err{bmk}"):
                dpg.delete_item(f'line_bmk_{bmk}')
                dpg.draw_line(parent=f"BMK:{bmk}",
                              p1=(70, 65),
                              p2=(115, 65),
                              thickness=12,
                              color=(255, 0, 0, 255),
                              tag=f'line_bmk_{bmk}')
    if dpg.get_value("cnt") == 120:
        for bmk in current_buks_list:
            if dpg.get_value(f"line_err{bmk}"):
                dpg.delete_item(f'line_bmk_{bmk}')
                dpg.draw_line(parent=f"BMK:{bmk}",
                              p1=(70, 65),
                              p2=(115, 65),
                              thickness=12,
                              color=(0, 0, 255, 255),
                              tag=f'line_bmk_{bmk}')

    dpg.set_value("cnt", dpg.get_value('cnt') + 1)
    if dpg.get_value('cnt') > 120:
        dpg.set_value('cnt', 0)


def redraw_data(params):
    bmk: str = str(params['bmk'])
    try:
        data_for_plot = params['data']['gPr\r\n']
        if int(data_for_plot['pr1']) > 5:
            dpg.delete_item(f'line_{bmk}')
            dpg.draw_line(parent=f"BMK:{bmk}", p1=(0, 53), p2=(
                200, 53), thickness=4, color=(255, 0, 0, 255), tag=f'line_{bmk}')
        else:
            dpg.delete_item(f'line_{bmk}')
            dpg.draw_line(parent=f"BMK:{bmk}", p1=(0, 53), p2=(
                200, 53), thickness=4, color=(0, 0, 0, 255), tag=f'line_{bmk}')
    except KeyError:
        pass
    try:
        data_for_table = params['data']['getStatus\r\n']
    except KeyError:
        return
    if not data_for_table:
        return
    if int(data_for_table['pr0']) > 5:
        dpg.delete_item(f'line_{bmk}')
        dpg.draw_line(parent=f"BMK:{bmk}", p1=(0, 53), p2=(
            200, 53), thickness=4, color=(255, 0, 0, 255), tag=f'line_{bmk}')
    else:
        dpg.delete_item(f'line_{bmk}')
        dpg.draw_line(parent=f"BMK:{bmk}", p1=(0, 53), p2=(
            200, 53), thickness=4, color=(0, 0, 0, 255), tag=f'line_{bmk}')
    if dpg.does_item_exist(f'set_temp_c_v_{bmk}'):
        dpg.set_value(f'set_temp_c_v_{bmk}', data_for_table[list(data_for_table)[
                      16]][0] + str(int(data_for_table[list(data_for_table)[16]][1:])))
    if dpg.does_item_exist(f"MT_{bmk}"):
        for i in range(len(list(data_for_table)) - 1):
            if i == 14 or i == 5:
                continue
            elif i == 6:
                dpg.set_value(f"row{bmk}_{i}", str(data_for_table[list(data_for_table)[6]])[
                              0] + str(data_for_table[list(data_for_table)[6]])[1:-1] + '.'+str(data_for_table[list(data_for_table)[i]])[3:])
            elif i == 16:
                dpg.set_value(f"row{bmk}_{i}", data_for_table[list(data_for_table)[
                              16]][0] + str(int(data_for_table[list(data_for_table)[16]][1:])))
            elif i == 20:
                dpg.set_value(f"row{bmk}_{i}", styp_torm(
                    data_for_table[list(data_for_table)[20]]))
            elif i == 21:
                dpg.set_value(f"row{bmk}_{i}", state_l(
                    data_for_table[list(data_for_table)[21]]))
            elif i == 22:
                dpg.set_value(f"row{bmk}_{i}", data_for_table[list(data_for_table)[22]][0] + str(
                    data_for_table[list(data_for_table)[22]])[1:-1] + '.'+str(data_for_table[list(data_for_table)[22]])[3:])
            elif i == 15:
                dpg.set_value(f"row{bmk}_{i}", str(
                    int(data_for_table[list(data_for_table)[15]])) + "B")
            elif i == 19 or i == 18:
                dpg.set_value(f"row{bmk}_{i}",
                              data_for_table[list(data_for_table)[i]])
            else:
                dpg.set_value(f"row{bmk}_{i}", int(
                    data_for_table[list(data_for_table)[i]]))


i: int = 0


def redraw_pr_plot(data: dict[str, str]) -> None:
    global i, list_for_plot_y1, list_for_plot_y2, list_for_plot_x
    if dpg.does_item_exist("plot_win"):
        if dpg.is_item_visible("plot_win"):
            i += 1
            list_for_plot_y1.append(int(data['pr1']))
            list_for_plot_y2.append(int(data['pr2']))
            list_for_plot_x.append(i)
            dpg.set_value("series_tag1", [list_for_plot_x, list_for_plot_y1])
            dpg.set_value("series_tag2", [list_for_plot_x, list_for_plot_y2])
            dpg.fit_axis_data("x_axis")
            if i > 40:
                list_for_plot_y1.pop(0)
                list_for_plot_y2.pop(0)
                list_for_plot_x.pop(0)
        else:
            list_for_plot_y1 = []
            list_for_plot_y2 = []
            list_for_plot_x = []
            dpg.delete_item("plot_win")
            i = 0


def redraw_bmk_window(params_dict):
    bmk: str = str(params_dict['bmk'])
    dpg.delete_item(f'line_{bmk}')
    dpg.draw_line(parent=f"BMK:{bmk}", p1=(0, 53), p2=(
        200, 53), thickness=4, color=(0, 0, 0, 255), tag=f'line_{bmk}')
    dpg.delete_item(f'line_bmk_{bmk}')
    dpg.draw_line(parent=f"BMK:{bmk}", p1=(70, 65), p2=(
        115, 65), thickness=12, color=(0, 0, 255, 255), tag=f'line_bmk_{bmk}')
    dpg.set_item_callback(f'bmk_{bmk}', callback=draw_window_table)
    dpg.set_item_callback(f'err_{bmk}', callback=err_callback)
    dpg.set_item_callback(f'pr_{bmk}', callback=create_plot)
    dpg.set_item_user_data(f'bmk_{bmk}', params_dict)
    dpg.set_item_user_data(f'err_{bmk}', params_dict)


def main_window(q: Any, q_task: Any):
    dpg.create_context()
    dpg.bind_theme(create_theme_imgui_light())
    with dpg.window(tag="Main window", no_scrollbar=True, no_focus_on_appearing=False, no_resize=False, no_move=True, autosize=False):
        with dpg.menu_bar():
            with dpg.menu(label="О программе"):
                dpg.add_text(
                    default_value="""Разработано в ЦКЖТ в 2023 году\nРазработчик Волков Егор Алексеевич\nПо всем вопросам обращаться по адресу: gole00201@gmail.com""")
    draw_bmk_at_runtime(q_task)
    draw_scheme_at_run_time()
    dpg.set_primary_window("Main window", True)
    dpg.create_viewport(title="STP ARS-4", width=1980, height=1024,
                        resizable=True, min_width=1000, min_height=800)
    with dpg.value_registry():
        for bmk in list_of_bmk.keys():
            dpg.add_bool_value(tag=f"line_err{bmk}", default_value=False)
            dpg.add_bool_value(tag=f"line_cnt{bmk}", default_value=True)
            dpg.add_bool_value(tag=f'pr_is_ref{bmk}', default_value=False)
        dpg.add_int_value(tag=f"cnt", default_value=- 120)
    with dpg.theme(tag="ser1_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 255, 0),
                                category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="ser2_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 0, 0),
                                category=dpg.mvThemeCat_Plots)
    with dpg.font_registry():
        with dpg.font("./fonts/Cousine-Bold.ttf", 18, default_font=True, tag='Main_font'):
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        with dpg.font("./fonts/Cousine-Regular.ttf", 15, default_font=True, tag='table_font'):
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        with dpg.font("./fonts/Cousine-Bold.ttf", 25, default_font=True, tag='lable_font'):
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        with dpg.font("./fonts/Cousine-Bold.ttf", 18, default_font=True, tag='time_font'):
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
    dpg.bind_item_font("TIME", "time_font")
    dpg.bind_item_font("Main lable", "lable_font")
    dpg.bind_font('Main_font')
    dpg.setup_dearpygui()
    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        if q.qsize() > 10000:
            while not q.empty():
                q.get()
        print_real_time()
        show_bmk(q)
        dpg.render_dearpygui_frame()
    q_task.put([b'KILL'])
    dpg.destroy_context()


if __name__ == '__main__':
    freeze_support()
    q: Any = Queue()
    q_task: Any = Queue()
    p1 = Process(target=main_com_loop, args=(q, q_task))
    p2 = Process(target=main_window, args=(q, q_task))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
