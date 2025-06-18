
def error(err_id: str, exception=None):
    match err_id:
        case "FLIGHT_NOT_READY":
            print("Flight requirements not satisfied yet.\n Check Reservation __init__ class.")
        case "SEAT_TAKEN":
            print("Seat is already taken.")
        case "INVALID_MAIN_MENU":
            print("Invalid choice!\nChoose only 1 or 2.")
        case "INVALID_SEAT_INPUT":
            print("Invalid seat input!\nRange: 1A, 30F")
        case "ERROR_DB_SEAT":
            print()
        case _:
            print("Unknown Error.", end=" ")
            if exception is None:
                print("Exception: ", exception)

def sucess(message: str):
    print(message)


def show_main() -> int:
    print(r"""
            __________                                          _________              __               
            \______   \ ____   ______ ______________  __ ____  /   _____/ ____ _____ _/  |_   /\|\/\    
            |       _// __ \ /  ___// __ \_  __ \  \/ // __ \ \_____  \_/ __ \\__  \\   __\ _)    (__  
            |    |   \  ___/ \___ \\  ___/|  | \/\   /\  ___/ /        \  ___/ / __ \|  |   \_     _/  
            |____|_  /\___  >____  >\___  >__|    \_/  \___  >_______  /\___  >____  /__|     )    \   
                   \/     \/     \/     \/                 \/        \/     \/     \/         \/\|\/   
            1. New Flight
            2. Show Flight Records
            """)
    choice = int(input())
    if 0 > choice < 3:
        error("INVALID_MAIN_MENU")
        return -1
    else:
        return choice

def new_flight():
    print(r"""                                                                         
              ______   ______   ______   ______   ______   ______   ______   ______   ______   ______ 
             /_____/  /_____/  /_____/  /_____/  /_____/  /_____/  /_____/  /_____/  /_____/  /_____/                                                                                      
             _______  _____________      __  ___________.____    .___  ________  ___ ______________   
             \      \ \_   _____/  \    /  \ \_   _____/|    |   |   |/  _____/ /   |   \__    ___/   
             /   |   \ |    __)_\   \/\/   /  |    __)  |    |   |   /   \  ___/    ~    \|    |      
            /    |    \|        \\        /   |     \   |    |___|   \    \_\  \    Y    /|    |      
            \____|__  /_______  / \__/\  /    \___  /   |_______ \___|\______  /\___|_  / |____|                                                                                              
              ______   ______   ______   ______   ______   ______   ______   ______   ______   ______ 
             /_____/  /_____/  /_____/  /_____/  /_____/  /_____/  /_____/  /_____/  /_____/  /_____/ 
             
            What is the Flight ID for this flight?
    """)


def display_seatmap(flight_id: str, seats):
    print(r"""                                                                                                                      
              ______   ______   ______   ______   ______   ______ 
             /_____/  /_____/  /_____/  /_____/  /_____/  /_____/                                                                                                                     
                              __                              
              ______ ____ _____ _/  |_    _____ _____  ______     
             /  ___// __ \\__  \\   __\  /     \\__  \ \____ \    
             \___ \\  ___/ / __ \|  |   |  Y Y  \/ __ \|  |_> >   
            /____  >\___  >____  /__|   |__|_|  (____  /   __/    
                 \/     \/     \/             \/     \/|__|                                                         
              ______   ______   ______   ______   ______   ______ 
             /_____/  /_____/  /_____/  /_____/  /_____/  /_____/ 
                      
            FLIGHT ID:""", flight_id)
    print("A\tB\tC\tD\tE\tF")
    for row in range(1, 31):
        print(row, end="\t")
        for seat in seats:
            print("[X]" if seat.is_taken else "[ ]")
        print()
    print("1. Reserve Seat\n2. Seat Details")

def show_details(details: tuple):
    print(f"""
    -----------------------------------------
        ==================================
                FLIGHT DETAILS
        ==================================  
        SEAT POSITION: {details[0]}
        NAME: {details[1]} 
    -----------------------------------------
        
    """)