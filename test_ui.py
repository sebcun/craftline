from src.craftline.ui import Screen, Menu, MenuItem, read_key, Key, Theme

def show_main_menu() -> None:
    
    screen = Screen(
        title="Main Menu",
        subtitle="Craftline Launcher",
        footer_hint="↑↓ Navigate  Enter Select  Esc Quit"
    )
    
    def play(): print("Play")
    def settings(): print("Settings")
    
    menu = Menu(items=[
        MenuItem("Play", action=play),
        MenuItem("Instances", action=lambda: None),
        MenuItem("Settings", action=settings),
        MenuItem("Disabled", disabled=True),
        MenuItem("Exit", action=lambda: "exit")
    ])
    
    while True:
        content = [
            "",
            *menu.render(),
            "",
            f"  {Theme.MUTED('Select an option to continue')}"
        ]
        
        screen.render(content)
        
        event = read_key()
        
        if event.key == Key.ESCAPE:
            break
        
        result = menu.handle_input(event)
        if result == 'exit':
            break
        
if __name__ == "__main__":
    show_main_menu()