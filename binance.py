'import websocket'
import json
from multiprocessing import Process, Value

# Define a shared Value to store the last price
last_price_binance = Value('d', 0.0)

# Define a function to handle incoming WebSocket messages and update last_price_binance
def on_message(ws, message):
    data = json.loads(message)
    if 'C' in data:
        last_price = data['C']
        last_price_binance.value = last_price
        print(f"Last Price (Binance): {last_price}")  # Print the last price

# Create a function that will run the WebSocket connection
def run_websocket():
    print("Establishing WebSocket connection...")
    
    # Define the WebSocket URL
    symbol = "btcusdt"  # Replace with your desired symbol
    websocket_url = f"wss://stream.binance.com:9443/ws/{symbol}@ticker"
    
    # Create a WebSocket connection and set the on_message callback
    ws = websocket.WebSocketApp(websocket_url, on_message=on_message)

    # Start the WebSocket connection
    ws.run_forever()

if __name__ == '__main__':
    # Start the WebSocket connection in a separate process
    process = Process(target=run_websocket)
    process.start()
