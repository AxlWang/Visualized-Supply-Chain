import pandas as pd
import tkinter as tk
from tkinter import messagebox as msgbox
import tkinter.ttk as ttk
import random
import datetime
import spore


def sum13qty(store_id, date):
    date = pd.to_datetime(date)
    res = sales.loc[(sales["LOC_IDNT"] == store_id) & (sales["WORK_DATE"] < date) & (
                sales["WORK_DATE"] >= (date - datetime.timedelta(days=14))),
                    "SLS_QTY"].sum()
    return res


def transit(start, step, date):
    if (start.soh > sum13qty(start.store_id, date) * 2):
        for n in start.neighbors.keys():
            if ((store_list[n].soh + store_list[n].in_transit) == 0) & (start.soh > 2):
                start.consume(2)
                store_list[n].in_transit += 2
                start.trace[n] = (start.spaceX, start.spaceY)

    if len(start.trace) != 0:
        for i in start.trace.keys():
            if len(start.trace[i]) > 0:
                current_dist = ((store_list[i].spaceX - start.trace[i][0]) ** 2 + (
                            store_list[i].spaceY - start.trace[i][1]) ** 2) ** 0.5
                if current_dist <= step:
                    start.trace[i] = ()
                    store_list[i].absorb(2)
                    store_list[i].in_transit -= 2
                else:
                    ratio = step / start.neighbors[i]
                    start.trace[i] = (start.trace[i][0] + ratio * (store_list[i].spaceX - start.spaceX),
                                      start.trace[i][1] + ratio * (store_list[i].spaceY - start.spaceY))


def gen(date):
    global oos_by_type
    date_sales = sales.loc[sales["WORK_DATE"] == date]
    ttl_sales_qty = 0
    oos_count = 0
    oos_by_type = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    for i in store_list.keys():
        try:
            sls_qty = int(date_sales.loc[date_sales["LOC_IDNT"] == i, "SLS_QTY"])
        except:
            sls_qty = 0
        if sls_qty > store_list[i].soh:
            sls_qty = store_list[i].soh
        store_list[i].consume(sls_qty)
        store_list[i].record_sales(sls_qty)
        ttl_sales_qty += sls_qty
        transit(store_list[i], 60, date)
        if (store_list[i].soh == 0)&(store_list[i].rank != 6):
            oos_count += 1
            oos_by_type[store_list[i].rank] += 1
                
    sales_summary.append(ttl_sales_qty)
    oos_list.append(oos_count)


def show():
    for i, j in store_list.items():
        if len(j.trace) != 0:
            for s in j.trace.keys():
                if len(j.trace[s]) != 0:
                    canvas.create_line(j.spaceX, j.spaceY,
                                       j.trace[s][0], j.trace[s][1],
                                       fill="#C0D9D9", width=1)
                    canvas.create_oval(j.trace[s][0] - (store_list[s].in_transit)/2, j.trace[s][1] - (store_list[s].in_transit)/2,
                                       j.trace[s][0] + (store_list[s].in_transit)/2, j.trace[s][1] + (store_list[s].in_transit)/2,
                                       fill="#8F8FBD", width=0)
        canvas.create_oval(j.spaceX - j.soh/2, j.spaceY - j.soh/2,
                           j.spaceX + j.soh/2, j.spaceY + j.soh/2,
                           fill=color_map[j.rank], width=0)
        # 文字标签
        canvas.create_text(j.spaceX, j.spaceY,
                           text=j.soh, fill="steelblue", font=("Arial", 9))
        
def show_sales():
    if len(sales_summary) > 0:
        spacing = 290/(len(sales_summary)+1)
        step = 1
        max_h = max(sales_summary)
        for i in sales_summary:
            if max_h > 0:
                h = i/max_h*300
            elif max_h == 0:
                h = 0
            canvas2.create_line(spacing*step, 310-h, spacing*step, 310, fill="blue", width=1)
            canvas2.create_text(spacing*step, 305-h,
                        text=i, fill="steelblue", font=("Arial", 6))
            step += 1

def show_oos():
    if len(oos_list) > 0:
        spacing = 290/(len(oos_list)+1)
        step = 1
        max_h = max(oos_list)
        for i in oos_list:
            if max_h > 0:
                h = i/max_h*300
            elif max_h == 0:
                h = 0
            canvas3.create_line(spacing*step, 310-h, spacing*step, 310, fill="red", width=1)
            canvas3.create_text(spacing*step, 305-h,
                        text=i, fill="steelblue", font=("Arial", 6))
            step += 1
            
def show_oos_by_type():
    step = 1
    spacing = 290/(len(oos_by_type))
    max_h = max(oos_by_type.values())
    for i,j in oos_by_type.items():
        if i != 6:
            if max_h > 0:
                h = j/max_h*300
            elif max_h == 0:
                h = 0
            canvas4.create_line(spacing*step, 310-h, spacing*step, 310, fill="lightgreen", width=15)
            canvas4.create_text(spacing*step, 305-h, text=j, fill="steelblue", font=("Arial", 6))
            step+=1

        
def setting_window(event):
    
    def set_up_dc():
        global max_qty
        max_qty = int(enter_dc_qty.get())
        current_dc.config(text=max_qty)

    
    def set_up_store(): 
        if store_box.get() == 'embryo':
            global embryo_qty
            embryo_qty = int(enter_store_qty.get())
            current_embryo.config(text=embryo_qty)
        elif store_box.get() == 'baby':
            global baby_qty
            baby_qty = int(enter_store_qty.get())
            current_baby.config(text=baby_qty)
        elif store_box.get() == 'basic':
            global basic_qty
            basic_qty = int(enter_store_qty.get())
            current_basic.config(text=basic_qty)
        elif store_box.get() == 'anchor':
            global anchor_qty
            anchor_qty = int(enter_store_qty.get())
            current_anchor.config(text=anchor_qty)
        elif store_box.get() == 'star':
            global star_qty
            star_qty = int(enter_store_qty.get())
            current_star.config(text=star_qty)
        elif store_box.get() == 'super star':
            global sstar_qty
            sstar_qty = int(enter_store_qty.get())
            current_sstar.config(text=sstar_qty)
    
    
    new_window =  tk.Tk()
    new_window.title("Set initial parameters.")
    
    # DC
    dc_qty = tk.IntVar()
    dc_label = tk.Label(new_window, text="DC")
    enter_dc_qty = tk.Entry(new_window, width = 24, textvariable=dc_qty)

    # Store
    store_var = tk.StringVar()
    store_qty = tk.IntVar()
    store_label = tk.Label(new_window, text="Store")
    enter_store_qty = tk.Entry(new_window, width = 24, textvariable=store_qty)
    store_box = ttk.Combobox(new_window, textvariable=store_var,
                             value=['embryo', 'baby', 'basic', 'anchor', 'star', 'super star'])
#     store_box.bind('<<ComboboxSelected>>', chose_store)
    confirm_dc_qty = tk.Button(new_window, text='Confirm', width = 24, command=set_up_dc)
    confirm_store_qty = tk.Button(new_window, text='Confirm', width = 24, command=set_up_store)
    
    label_dc = tk.Label(new_window, text='DC')
    current_dc = tk.Label(new_window, text=max_qty)
    label_embryo = tk.Label(new_window, text='Embryo')
    current_embryo = tk.Label(new_window, text=embryo_qty)
    label_baby = tk.Label(new_window, text='Baby')
    current_baby = tk.Label(new_window, text=baby_qty)
    label_basic = tk.Label(new_window, text='Basic')
    current_basic = tk.Label(new_window, text=basic_qty)
    label_anchor = tk.Label(new_window, text='Anchor')
    current_anchor = tk.Label(new_window, text=anchor_qty)
    label_star = tk.Label(new_window, text='Star')
    current_star = tk.Label(new_window, text=star_qty)
    label_sstar = tk.Label(new_window, text='Super Star')
    current_sstar = tk.Label(new_window, text=sstar_qty)
    
    # 布局
    dc_label.grid(row=0, column=0,padx=10, pady=10)
    enter_dc_qty.grid(row=0, column=1,padx=10, pady=10)
    confirm_dc_qty.grid(row=0, column=3, padx=10, pady=10)
    store_label.grid(row=1, column=0,padx=10, pady=10)
    enter_store_qty.grid(row=1, column=1,padx=10, pady=10)
    store_box.grid(row=1, column=2, padx=10, pady=10)
    confirm_store_qty.grid(row=1, column=3, padx=10, pady=10)
    
    label_dc.grid(row=2, column=0,padx=10, pady=10)
    current_dc.grid(row=2,column=1,padx=10, pady=10)
    label_embryo.grid(row=2, column=2,padx=10, pady=10)
    current_embryo.grid(row=2,column=3,padx=10, pady=10)
    label_baby.grid(row=3, column=0,padx=10, pady=10)
    current_baby.grid(row=3,column=1,padx=10, pady=10)
    label_basic.grid(row=3, column=2,padx=10, pady=10)
    current_basic.grid(row=3,column=3,padx=10, pady=10)
    label_anchor.grid(row=4, column=0,padx=10, pady=10)
    current_anchor.grid(row=4,column=1,padx=10, pady=10)
    label_star.grid(row=4, column=2,padx=10, pady=10)
    current_star.grid(row=4,column=3,padx=10, pady=10)
    label_sstar.grid(row=5, column=0,padx=10, pady=10)
    current_sstar.grid(row=5,column=1,padx=10, pady=10)
    
    new_window.mainloop()
    

# 创建字典，按照店号存储对象
def initialization():
    global day
    global store_list
    global sales_summary
    global oos_list
    global oos_by_type
    day = 0
    store_list = dict()
    sales_summary = list()
    oos_list = list()
    oos_by_type = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    # 单独初始化DC
    store_list[dc] = spore.Spore(max_qty, dc, 1000,  6)
    for s in sales["LOC_IDNT"].drop_duplicates():
        if rank[s] == 'Embryo':
            store_list[s] = spore.Spore(embryo_qty, s, 300, 0)
        elif rank[s] == 'Baby':
            store_list[s] = spore.Spore(baby_qty, s, 300, 1)
        elif rank[s] == 'Basic':
            store_list[s] = spore.Spore(basic_qty, s, 300, 2)
        elif rank[s] == 'Anchor':
            store_list[s] = spore.Spore(anchor_qty, s, 300, 3)
        elif rank[s] == 'Star':
            store_list[s] = spore.Spore(star_qty, s, 300, 4)
        elif rank[s] == 'Super Star':
            store_list[s] = spore.Spore(sstar_qty, s, 300, 5)
    


# 定义好每个店铺的邻居集合
def network():
    for i in store_list.keys():
        for j in store_list.keys():
            if i != j:
                dist = ((store_list[i].spaceX - store_list[j].spaceX) ** 2 + (
                            store_list[i].spaceY - store_list[j].spaceY) ** 2) ** 0.5
                if dist < store_list[i].scope:
                    store_list[i].neighbors[j] = dist


def chose_city(event):
    global sales
    start_button.config(state='normal')
    sales = TTL_sales.loc[TTL_sales["City"] == city_list[city_box.current()]]


def update():
    global day
    canvas.delete("all")
    canvas2.delete("all")
    canvas3.delete("all")
    canvas4.delete("all")
    show()
    show_sales()
    show_oos()
    show_oos_by_type()
    if day <= (len(date_list) - 1):
        gen(date_list[day])
        day += 1
        root.after(100, update)
    elif day > (len(date_list) - 1):
        label1.config(text="Simulation completed, click the start button to simulate again.")


def start_handler(event):
    if start_button['state'] == 'disabled':
        msgbox.showwarning('Tips', 'Please choose the city before start!')
    else:
        label1.config(text="Simulation in progress.")
        initialization()
        network()
        update()  
        

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Simulation of slime mold growth")

    dc = 999
    day = 0
    sales_summary = list()
    oos_list = list()
    oos_by_type = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

    color_map = ['#71ae46', '#96b744', '#c4cc38', '#ebe12a', '#eab026', '#e3852b', '#d85d2a', '#ce2626', '#ac2026']
    max_qty = 300
    embryo_qty = random.randint(3, 10)
    baby_qty = random.randint(10, 15)
    basic_qty = random.randint(15, 20)
    anchor_qty = random.randint(20, 25)
    star_qty = random.randint(25, 30)
    sstar_qty = random.randint(30, 40)
    store_list = dict()
    sales = pd.DataFrame()

    # 读取销售数据
    TTL_sales = pd.read_csv("sales_data.csv")
    city_list = list(TTL_sales["City"].drop_duplicates())
    TTL_sales["WORK_DATE"] = pd.to_datetime(TTL_sales["WORK_DATE"])
    TTL_sales = TTL_sales.groupby(["WORK_DATE", "LOC_IDNT", "City", "Type"], as_index=False).agg({
        'SLS_QTY': 'sum'
    })
    rank = TTL_sales[["LOC_IDNT", "Type"]].drop_duplicates()
    rank = rank.set_index("LOC_IDNT").to_dict()['Type']


    # date_list = pd.date_range(min(sales["WORK_DATE"]), max(sales["WORK_DATE"]), freq='D')
    date_list = pd.date_range(min(TTL_sales["WORK_DATE"]), max(TTL_sales["WORK_DATE"]), freq='D')


    canvas = tk.Canvas(root, width=1150, height=640, bg='white')
    # 创建选项卡容器
    tab_control = ttk.Notebook(root)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Tab 1")
    tab_control.add(tab2, text="Tab 2")

    # 在选项卡容器的Tab中创建数据可视化的画布
    canvas2 = tk.Canvas(tab1, width=300, height=310, bg='white')
    canvas2.grid(row=0,column=0)
    canvas3 = tk.Canvas(tab1, width=300, height=310, bg='white')
    canvas3.grid(row=1,column=0)
    canvas4 = tk.Canvas(tab2, width=300, height=310, bg='white')
    canvas4.grid(row=0,column=0)

    label1 = tk.Label(root, text="Please choose the city before you start.")
    label2 = tk.Label(root, text="Data Board")


    # 设置下拉选项框
    var = tk.StringVar()
    city_box = ttk.Combobox(root, textvariable=var, value=city_list)
    # current设置默认显示的值，即传入的下标
    city_box.current(36)
    city_box.bind('<<ComboboxSelected>>', chose_city)

    start_button = tk.Button(root, text='Start', state='disabled', width=12)
    start_button.bind('<Button-1>', start_handler)

    set_button = tk.Button(root, text="Settings", width=12)
    set_button.bind('<Button-1>', setting_window)

    # 主窗口布局
    label1.grid(row=0, column=0, padx=10)
    city_box.grid(row=0, column=1, padx=10, pady=10)
    label2.grid(row=0, column=2, padx=10)
    canvas.grid(row=1, columnspan=2, rowspan=2)
    tab_control.grid(row=1, column=2,rowspan=2)
    start_button.grid(row=3, column=0, padx=10, pady=10)
    set_button.grid(row=3, column=1, padx=10, pady=10)

    root.mainloop()