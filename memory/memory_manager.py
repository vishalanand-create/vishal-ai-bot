class MemoryManager:
    """
    A simple memory manager for storing and retrieving conversation history.
    """
    
    def __init__(self, max_memory_size=100):
        """
        Initialize the memory manager.
        
        Args:
            max_memory_size (int): Maximum number of messages to store
        """
        self.max_memory_size = max_memory_size
        self.memory = []
    
    def add_message(self, role, content):
        """
        Add a message to memory.
        
        Args:
            role (str): The role of the message sender (e.g., 'user', 'assistant')
            content (str): The content of the message
        """
        message = {"role": role, "content": content}
        self.memory.append(message)
        
        # Trim memory if it exceeds max size
        if len(self.memory) > self.max_memory_size:
            self.memory = self.memory[-self.max_memory_size:]
    
    def get_messages(self, last_n=None):
        """
        Retrieve messages from memory.
        
        Args:
            last_n (int, optional): Number of recent messages to retrieve
        
        Returns:
            list: List of messages
        """
        if last_n:
            return self.memory[-last_n:]
        return self.memory
    
    def clear_memory(self):
        """
        Clear all messages from memory.
        """
        self.memory = []
    
    def get_memory_size(self):
        """
        Get the current number of messages in memory.
        
        Returns:
            int: Number of messages
        """
        return len(self.memory)
