from src.agent.memory_adapter import DualMemoryAdapter

def test_chat_history_messages():
    """Test that the chat_history.messages attribute works correctly."""
    
    # Create a new adapter instance
    print("Creating DualMemoryAdapter...")
    adapter = DualMemoryAdapter()
    
    # Add some test messages
    print("\nAdding messages...")
    adapter.add_user_message("Hello, this is a test message")
    adapter.add_ai_message("Hi there! I'm responding to your test.")
    
    # Check if chat_history has a messages attribute
    print("\nTesting chat_history.messages access...")
    try:
        messages = adapter.chat_history.messages
        print(f"SUCCESS: chat_history.messages contains {len(messages)} messages")
        
        # Check the content of the messages
        for i, msg in enumerate(messages):
            print(f"  Message {i+1}: {type(msg).__name__} - {msg.content}")
        
    except AttributeError as e:
        print(f"ERROR: chat_history.messages failed - {str(e)}")
    
    # Also test direct access to the chat_history for backward compatibility
    print("\nTesting get_memory_variables...")
    try:
        variables = adapter.get_memory_variables()
        direct_messages = variables["chat_history"]
        print(f"SUCCESS: get_memory_variables() returns {len(direct_messages)} messages")
        
        # Check the content of the messages
        for i, msg in enumerate(direct_messages):
            print(f"  Message {i+1}: {type(msg).__name__} - {msg.content}")
    except Exception as e:
        print(f"ERROR: get_memory_variables() failed - {str(e)}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_chat_history_messages() 