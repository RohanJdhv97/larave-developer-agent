from src.agent.memory_adapter import DualMemoryAdapter, ChatHistoryAdapter
from src.cli.memory_ui import memory_ui
from langchain_core.messages import AIMessage, HumanMessage

def main():
    print("Initializing DualMemoryAdapter...")
    # Create a new adapter instance
    adapter = DualMemoryAdapter()
    
    print("Testing the chat_history_adapter...")
    # Verify the chat_history_adapter was created correctly
    if not hasattr(adapter, 'chat_history_adapter') or adapter.chat_history_adapter is None:
        print("ERROR: chat_history_adapter is missing or None")
    else:
        print("chat_history_adapter is properly initialized")
        
    print("\nTesting the chat_history property...")
    # Verify the chat_history property
    if not hasattr(adapter, 'chat_history'):
        print("ERROR: chat_history property is missing")
    else:
        print(f"chat_history exists and has {len(adapter.chat_history)} messages")
    
    # Test adding messages
    print("\nAdding messages to memory...")
    adapter.add_user_message("Hello, AI assistant!")
    adapter.add_ai_message("Hello! How can I help you today?")
    adapter.add_user_message("Tell me about the dual memory system.")
    adapter.add_ai_message("The dual memory system has temporary and permanent memory components.")
    
    # Check chat_history property
    print("\nChecking chat_history property...")
    chat_history = adapter.chat_history
    print(f"Number of messages in chat_history: {len(chat_history)}")
    for i, msg in enumerate(chat_history):
        print(f"  Message {i+1} - Type: {type(msg).__name__}, Content: {msg.content[:30]}...")
    
    # Check chat_history_adapter property
    print("\nChecking chat_history_adapter property...")
    adapter_messages = adapter.chat_history_adapter.messages
    print(f"Number of messages in chat_history_adapter: {len(adapter_messages)}")
    for i, msg in enumerate(adapter_messages):
        print(f"  Message {i+1} - Type: {type(msg).__name__}, Content: {msg.content[:30]}...")
    
    # Display memory state using memory_ui
    print("\nDisplaying memory state...")
    memory_ui.show_memory_state(adapter)
    
    # Get memory variables
    print("\nGetting memory variables...")
    variables = adapter.get_memory_variables()
    print(f"Variables contain {len(variables['chat_history'])} messages in chat_history")
    print(f"Chat summary: {variables['chat_summary']}")
    
    # Test error handling
    print("\nTesting error handling...")
    try:
        # Intentionally cause an error
        original_dual_memory = adapter.dual_memory
        adapter.dual_memory = None
        
        # This should be handled
        adapter.add_user_message("This should be handled gracefully.")
        print("Error was handled successfully.")
        
        # Restore for further testing
        adapter.dual_memory = original_dual_memory
    except Exception as e:
        print(f"Error handling failed: {str(e)}")
    
    # Test save and load
    print("\nTesting save and load functionality...")
    try:
        adapter.save("test_memory.json")
        
        # Create a new adapter and load the saved memory
        loaded_adapter = DualMemoryAdapter.load("test_memory.json")
        
        # Verify the loaded adapter
        print(f"Loaded adapter has {len(loaded_adapter.chat_history)} messages")
        
        # Display loaded memory state
        memory_ui.show_memory_state(loaded_adapter)
    except Exception as e:
        print(f"Save/load failed: {str(e)}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    main() 