import pandas as pd
import networkx as nx
import numpy as np


def make_data(filename: str, skip_row:int):
    df = pd.read_csv(filename, encoding = "SHIFT_JIS", header = 0, skiprows = skip_row)
    ti = df.columns.get_loc('# DATE-TIME')
    fi = df.columns.get_loc('frame')
    ii = df.columns.get_loc('ID')
    ni = df.columns.get_loc('no')
    xi = df.columns.get_loc('px')
    yi = df.columns.get_loc('py')
    df = df.values
    index = 0
    time = []
    frame = []
    no = []
    h_id = []
    x = []
    y = []
    t = 0
    f = 0
    n = 0


    fff = []
    nnn = []
    ccc = []
    while index < len(df[:,ti]):
        if not np.isnan(df[:,ni][index]) and int(df[:,fi][index]) % 1 != 0: #約1秒
            index += int(df[:,ni][index] + 1)
            continue
        else:
            if df[:,ii][index] == 0:  #h_id
                index +=1
                continue
            if df[:,xi][index] is np.nan or df[:,yi][index] is np.nan:
                index+=1
                continue
            elif not np.isnan(df[:,ni][index]):
                t = df[:,ti][index]
                t = t.split("-")[1].split(':')
                t = t[0] + ':' + t[1] + ':' + t[2] + '.' + t[3]
                f = df[:,fi][index]
                n = df[:,ni][index]
                fff.append(f)
                nnn.append(n)

                # 色決める
                if f <= 36936*2:
                    ccc.append("red")
                elif f <= 36936*3:
                    ccc.append("yellow")
                elif f <= 36936*4:
                    ccc.append("green")
                else:
                    ccc.append("blue")

            else:
                time.append(t)
                frame.append(int(f))
                no.append(int(n))
                h_id.append(int(df[:,ii][index]))
                x.append(df[:,xi][index]+3.4)
                y.append(df[:,yi][index]+4.4)
        index += 1

    close_pair = {}
    now = 0
    index=0
    for index in range(len(frame)):
        for j in range(no[index] - now - 1):
            if frame[index] != frame[j + index+1]:
                break
            if ((x[index] - x[j + index+1]) * (x[index] - x[j + index+1]) + (y[index] - y[j + index+1]) * (y[index] - y[j + index+1])) <= 4: #1メートル以内
                id1 = int(max(h_id[index], h_id[j + index+1]))
                id2 = int(min(h_id[index], h_id[j + index+1]))
                close_pair[(id1, id2)] = close_pair.get((id1, id2), 0) + 1
        now += 1
        if index+1 < len(frame) and frame[index] != frame[index+1]:
            now = 0
    p1 = []
    p2 = []
    w = []
    closed_h_id = set()
    maxi_w = 0
    for (id1, id2), closed_time in close_pair.items(): #value+1 = time+1
        if closed_time >= 600:
            p1.append(id1)
            p2.append(id2)
            maxi_w = max(maxi_w, closed_time)
            w.append((closed_time/4293)*5)
            closed_h_id.add(id1)
            closed_h_id.add(id2)
    print("the longest closing time", maxi_w)
    close_pair_df = pd.DataFrame({"pair1":p1,"pair2":p2,"weight":w})
    close_pair_df.to_csv("data/close_pair_data.csv", encoding="shift_jis")

    appear_time = {}
    trajectory_x = []
    trajectory_y = []
    trajectory_h_id = []
    trajectory_time = []

    for i, id in enumerate(h_id):
        if id in closed_h_id:
            if id not in appear_time:
                appear_time[id] = (frame[i], 1)
            else:
                appear_time[id] = (appear_time[id][0] + frame[i], appear_time[id][1] + 1) 
            trajectory_x.append(x[i])
            trajectory_y.append(y[i])
            trajectory_h_id.append(id)
            trajectory_time.append(frame[i])

    node_color = []
    node_color_h_id = []
    for id, (appear_time, count) in appear_time.items():
        ave_time = appear_time / count
        node_color_h_id .append(id)
        if ave_time <= 36936*2:
            node_color.append("red")
        elif ave_time <= 36936*3:
            node_color.append("yellow")
        elif ave_time <= 36936*4:
            node_color.append("green")
        else:
            node_color.append("blue")

    network_df = pd.DataFrame({"index":node_color_h_id , "color":node_color})
    network_df.to_csv("data/network_color_data.csv", encoding="shift_jis")

    trajectory_df = pd.DataFrame({"index":trajectory_h_id, "time":trajectory_time, "x":trajectory_x, "y":trajectory_y})
    trajectory_df.to_csv("data/trajectory_data.csv", encoding="shift_jis")


    frame_and_no_df = pd.DataFrame({"frame":fff, "no": nnn, "color":ccc})
    frame_and_no_df.to_csv("data/frame_and_no_data.csv", encoding="shift_jis")