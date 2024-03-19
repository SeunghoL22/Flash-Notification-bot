import tkinter as tk
import threading
import time
import winsound

def countdown(n, label, seconds, event):
    i = seconds
    while i >= 0 and not event.is_set():
        if i == 0:
            label.config(text=f"{n} 종료!")
            winsound.Beep(1000, 1000)  # 1000Hz 주파수로 1초 동안 비프음을 재생합니다.
        else:
            label.config(text=f"{n}: {i//60}:{i%60} 남음")
        time.sleep(1)
        i -= 1

def create_timer_button(n, label, checkbox_vars, thread_event, thread, key):  # 'key' parameter added
    def start_timer_thread(event=None):  # Event parameter is added for bind method
        if thread[0] and thread[0].is_alive():
            thread_event[0].set()  # 이전 스레드를 종료합니다.
            thread[0].join()  # 스레드가 종료될 때까지 기다립니다.
        thread_event[0].clear()  # 새로운 스레드를 위해 이벤트를 초기화합니다.

        # 버튼이 눌릴 때마다 체크박스의 상태를 확인하고 타이머 시간을 계산합니다.
        seconds = 300
        checkbox_seconds = [15, 30, 75]
        for k in range(3):
            if checkbox_vars[k].get() == 1:
                seconds -= checkbox_seconds[k]
        
        thread[0] = threading.Thread(target=countdown, args=(n, label, seconds, thread_event[0]))
        thread[0].start()
    
    root.bind(key, start_timer_thread)  # Bind the shortcut key to the button function
    return start_timer_thread

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('800x435')  # 창 크기를 조절합니다.
    root.title('점멸 타이머 by 오엥')
    timer_names = ['탑', '정글', '미드', '원딜', '서폿']  # 타이머 이름을 바꿉니다.
    key_bindings = ['z', 'x', 'c', 'v', 'b']  # Add this line
    for i in range(5):  # 5개의 타이머를 만듭니다.
        frame = tk.Frame(root)
        frame.pack(pady=10)  # 위 아래로 10px의 간격을 추가합니다.
        entry = tk.Entry(frame, width=10)  # 빈칸의 크기를 줄입니다.
        entry.grid(row=0, column=0)  # Grid를 사용하여 빈칸을 왼쪽에 배치합니다.
        label = tk.Label(frame, text=f"{timer_names[i]}: 대기중", font=("Helvetica", 16))
        label.grid(row=0, column=1, padx=10)  # Grid를 사용하여 라벨을 빈칸의 오른쪽에 배치합니다.
        thread = [None]
        thread_event = [threading.Event()]
        
        checkbox_vars = [tk.IntVar() for _ in range(3)]
        checkbox_texts = ["우주", "쿨감신", "봉풀주"]
        for j in range(3):
            checkbox = tk.Checkbutton(frame, text=checkbox_texts[j], variable=checkbox_vars[j], font=("Helvetica", 16))
            checkbox.grid(row=0, column=j+2)  # Grid를 사용하여 체크박스를 배치합니다.
        
        button = tk.Button(frame, text="flash", command=create_timer_button(timer_names[i], label, checkbox_vars, thread_event, thread, key_bindings[i]), font=("Helvetica", 16))  # Add key_bindings[i] as a parameter
        button.grid(row=0, column=5)  # Grid를 사용하여 버튼을 체크박스의 오른쪽에 배치합니다.
    
    quit_button = tk.Button(root, text="프로그램 종료", command=root.destroy, font=("Helvetica", 16))
    quit_button.pack(pady=50)  # '프로그램 종료' 버튼을 프로그램의 가운데 아래에 배치합니다. 위치를 위로 조정합니다.
    
    root.mainloop()
