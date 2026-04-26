from gui.gui_controller import create_gui
import threading
from simulation import run_simulation
#test
# =======Helpervariables=======#
simulation_stop_event = threading.Event()
sim_thread = None

# ======= Main loop for GUI and simulation/restart =======
def main_loop():
    """
    Main loop for GUI and simulation/restart functionality.

    This function manages the GUI interface and handles simulation lifecycle:
    - Creates GUI and gets user input
    - Starts simulation in a separate thread
    - Handles simulation abort functionality
    - Restarts simulation when needed
    """
    global sim_thread
    def abort_simulation():
        """
        Aborts the current simulation by setting the stop event and joining the thread.
        """
        simulation_stop_event.set()
        if sim_thread is not None and sim_thread.is_alive():
            sim_thread.join()
        print("Simulation abgebrochen.")
    while True:
        user_input = create_gui(on_abort_simulation=abort_simulation)
        if not user_input:
            break
        simulation_stop_event.clear()
        sim_thread = threading.Thread(target=run_simulation, args=(user_input,))
        sim_thread.start()
        sim_thread.join()

# ======= Startpunkt =======
if __name__ == "__main__":
     main_loop()


