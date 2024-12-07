import tkinter as tk
import os
import sys
import RPi.GPIO as GPIO
from tkinter import *
from tkinter import messagebox

BUTTON_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class DrinkKiosk:
    def __init__(self, master):
        self.master = master
        self.master.title("햄버거 키오스크")
        
        self.drink_prices = {"불고기버거": 4000, "치킨버거": 5000, "모짜렐라 버거": 6000} # 햄버거 가격 설정
        
        self.orders = {}

        hamburger1 = PhotoImage(file = "/home/minschoi/Jong0602/Bulgogi.png")
        hamburger2 = PhotoImage(file = "/home/minschoi/Jong0602/Chicken.png")
        hamburger3 = PhotoImage(file = "/home/minschoi/Jong0602/Cheese.png")
        
        sys.stdout = open('/home/minschoi/Jong0602/output.txt','a')
        
        # 햄버거 선택 옵션 메뉴
        self.drink_label = tk.Label(master, text="햄버거 선택:")
        self.drink_label.grid(row=0, column=0, padx=10, pady=10)
        self.selected_drink = tk.StringVar()
        self.selected_drink.set("불고기버거") # 초기 선택: 불고기버거
        self.drink_option = tk.OptionMenu(master, self.selected_drink, *self.drink_prices.keys())
        self.drink_option.grid(row=0, column=1, padx=10, pady=10)
        
        # 햄버거 수량 입력
        self.quantity_label = tk.Label(master, text="수량:")
        self.quantity_label.grid(row=2, column=0, padx=10, pady=10)
        self.quantity = tk.IntVar()
        self.quantity.set(1) # 초기 수량: 1
        self.quantity_entry = tk.Entry(master, textvariable=self.quantity)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=10)
        
        #new
        self.pbtn1 = tk.Button(master, image = hamburger1, command=self.click_meat)
        self.pbtn1.image = hamburger1
        self.pbtn1.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.pbtn2 = tk.Button(master, image = hamburger2, command=self.click_chicken)
        self.pbtn2.image = hamburger2
        self.pbtn2.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.pbtn3 = tk.Button(master, image = hamburger3, command=self.click_cheese)
        self.pbtn3.image = hamburger3
        self.pbtn3.grid(row = 1, column = 2, padx = 10, pady = 10)

        # "+" 버튼
        self.plus_button = tk.Button(master, text="+", command=self.increase_quantity)
        self.plus_button.grid(row=3, column=0, padx=10, pady=(0, 10))

        # "-" 버튼
        self.minus_button = tk.Button(master, text="-", command=self.decrease_quantity)
        self.minus_button.grid(row=3, column=1, padx=10, pady=(0, 10))

        # 주문 추가 버튼 3행으로 바꿈
        self.add_order_button = tk.Button(master, text="주문 추가", command=self.add_order)
        self.add_order_button.grid(row=4, columnspan=3, padx=10, pady=10)
        
        # 주문 목록 표시
        self.order_list_label = tk.Label(master, text="주문 목록:")
        self.order_list_label.grid(row=5, column=1, padx=10, pady=10)
        self.order_listbox = tk.Listbox(master, width=30, height =3)
        self.order_listbox.grid(row=6, column=1, columnspan=1, padx=10, pady=10)
        
        # 주문 버튼
        self.order_button = tk.Button(master, text="주문", command=self.place_order)
        self.order_button.grid(row=7, columnspan=3, padx=10, pady=10)
        
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                print('tlqkf')
                os.system('/home/minschoi/Jong0602/STT.py')
        
    def add_order(self):
        selected_drink = self.selected_drink.get()
        price_per_drink = self.drink_prices[selected_drink]
        quantity = self.quantity.get()
        total_price = price_per_drink * quantity
        
        self.orders[selected_drink] = self.orders.get(selected_drink, 0) + quantity
        self.order_listbox.insert(tk.END, f"{selected_drink} - {quantity}개 ({total_price}원)")
    
    #버튼 누르면 메뉴 선택해주기
    def click_meat(self):
        self.selected_drink.set("불고기버거")
    
    def click_chicken(self):
        self.selected_drink.set("치킨버거")

    def click_cheese(self):
        self.selected_drink.set("모짜렐라 버거")

    # 수량 증가 메소드
    def increase_quantity(self):
        current_quantity = self.quantity.get()
        self.quantity.set(current_quantity + 1)

    # 수량 감소 메소드
    def decrease_quantity(self):
        current_quantity = self.quantity.get()
        # 최소 수량은 1로 설정
        if current_quantity > 1:
            self.quantity.set(current_quantity - 1)

    def place_order(self):
        total_price = sum(self.drink_prices[drink] * quantity for drink, quantity in self.orders.items())
        messagebox.showinfo("주문 완료", f"주문이 완료되었습니다. 총 가격은 {total_price}원 입니다.")
        print("%d" %total_price)
        self.clear_orders()
    
    def clear_orders(self):
        self.orders = {}
        self.order_listbox.delete(0, tk.END)
        self.selected_drink.set("불고기버거")
        self.quantity.set(1)
        

def main():
    root = tk.Tk()
    app = DrinkKiosk(root)
    root.mainloop()



    # 프로그램 종료 시 GPIO 리소스 해제
    GPIO.cleanup()

if __name__ == "__main__":
    main()


