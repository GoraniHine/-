# 메뉴와 가격 설정
import os

menu = {
    "불고기버거": 5000,
    "치킨버거": 4500,
    "치즈버거": 5500
}

def kiosk():
    print("어서오세요! 키오스크를 이용하여 주문해주세요.")
    total_price = 0
    
    while True:
        print("\n[메뉴]")
        for item, price in menu.items():
            print(f"{item}: {price}원")
        
        choice = input("\n주문하실 메뉴를 선택하세요 (종료하려면 '종료' 입력): ")
        
        if choice == "종료":
            print(f"\n주문하신 내역의 총 가격은 {total_price}원 입니다. 결제해주시기 바랍니다.")
            #os.system('C:/Users/최민식/Desktop/0429종합설계/KKiosk.py')
            break
        
        if choice in menu:
            quantity = int(input("수량을 입력하세요: "))
            if quantity < 0:
                print("잘못된 수량입니다. 0 이상의 수를 입력하세요.")
                continue
            
            total_price += menu[choice] * quantity
            print(f"{choice} {quantity}개를 주문하셨습니다.")
        else:
            print("죄송합니다. 해당 메뉴는 없습니다.")
    




# 키오스크 실행
if __name__ == "__main__":
    kiosk()
