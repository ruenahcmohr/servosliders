import serial
import time
import threading

class ServoControllerSSC8:
    def __init__(self, port, baudrate=9600, timeout=1):
        """
        Initialize the servo controller.
        
        :param port: The serial port to connect to (e.g., 'COM3', '/dev/ttyUSB0').
        :param baudrate: The baud rate for communication (default: 9600).
        :param timeout: Serial read timeout in seconds (default: 1 second).
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.positions = [0] * 8  # Initial positions for all 8 servos
        self.updated = [0] * 8
        self.running = False     # Indicates if the retransmission loop is active
        
        # Initialize serial connection
        self.serial = serial.Serial(port, baudrate, timeout=timeout)
    
    def set_position(self, channel, position):
        """
        Set the position for a specific servo.
        
        :param channel: Servo channel (0-7).
        :param position: Servo position (0-255).
        """
        if ((0 <= channel < 8) and (0 <= position <= 48000)):
            self.positions[channel] = position
            self.updated[channel] = 1
        else:
            raise ValueError("Channel must be 0-7 and position must be 0-255")
    
    def build_command(self):
        """
        Build the SSC8 protocol command based on the current positions.
        
        :return: A bytes object representing the command.
        """
        command = []  # Start byte for SSC8
        for channel, position in enumerate(self.positions):
            if (self.updated[channel] != 0):
               command.append(0xFF)
               command.append(channel)
               #command.append(position)
               command.append((position >> 8) & 255)            
               command.append(position & 255)            
               self.updated[channel] = 0
        return bytes(command)
    
    def send_command(self):
        """
        Send the current positions to the servo controller.
        """
        command = self.build_command()
        self.serial.write(command)
        self.serial.flush()
    
    def start_stream(self, interval=0.025):
        """
        Start retransmitting positions every 16ms.
        
        :param interval: Time between transmissions in seconds (default: 0.016).
        """
        self.running = True
        threading.Thread(target=self._retransmit_loop, args=(interval,), daemon=True).start()
    
    def _retransmit_loop(self, interval):
        """
        Internal loop for retransmitting positions.
        
        :param interval: Time between transmissions in seconds.
        """
        while self.running:
            self.send_command()
            time.sleep(interval)
    
    def stop_stream(self):
        """
        Stop retransmitting positions.
        """
        self.running = False
    
    def close(self):
        """
        Close the serial connection.
        """
        self.stop_stream()
        self.serial.close()
